OntCversion = '2.0.0'
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.App import DynamicAppCall
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, state, append
from ontology.libont import AddressFromVmCode

ONTAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')

Admin = Base58ToAddress("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")
SelfContractAddress = GetExecutingScriptHash()
# GP means gift package
GP_PREFIX = "GPContent"
PROPERTY_REVERSED_HASH_KEY = "PropertyHash"
PRESALE_PAUSED_KEY = "Pause"


def Main(operation, args):
    ############# Methods for Admin account only defination Starts  ################
    if operation == "setPropertyHash":
        assert (len(args) == 1)
        propertyReversedHash = args[0]
        return setPropertyHash(propertyReversedHash)
    if operation == "setGP":
        assert (len(args) == 3)
        gpId = args[0]
        price = args[1]
        gpContent = args[2]
        return setGP(gpId, price, gpContent)
    if operation == "withdraw":
        assert (len(args) == 22)
        toAcct = args[0]
        amount = args[1]
        return withdraw(toAcct, amount)
    if operation == "pause":
        return pause()
    if operation == "unpause":
        return unpause()
    if operation == "migrateContract":
        assert (len(args) == 7)
        code = args[0]
        needStorage = args[1]
        name = args[2]
        version = args[3]
        author = args[4]
        email = args[5]
        description = args[6]
        return migrateContract(code, needStorage, name, version, author, email, description)
    ############# Methods for Admin account only defination Ends  ################
    #################### Purchase method for player Starts  ######################
    if operation == "purchase":
        assert (len(args) == 2)
        account = args[0]
        gpId = args[1]
        return purchase(account, gpId)
    #################### Purchase method for player Ends  ######################
    #################### Pre-execute methods defination Starts  ######################
    if operation == "getPropertyReversedHash":
        return getPropertyReversedHash()
    if operation == "getGP":
        assert (len(args) == 1)
        gpId = args[0]
        return getGP(gpId)
    #################### Pre-execute methods defination Ends  ######################
    return False

############# Methods for Admin account only defination Starts  ################
def setPropertyHash(propertyReversedHash):
    assert (CheckWitness(Admin))
    Put(GetContext(), PROPERTY_REVERSED_HASH_KEY, propertyReversedHash)
    Notify(["setPropertyHash", propertyReversedHash])
    return True


def setGP(gpId, price, gpContent):
    """
    :param gpId: token as the identity of gift package
    :param price: how much ong does this gpId will be sold
    :param gpContent: [[tokenId1, amount1], [tokenId2, amount2], ..., [tokenIdN, amountN]]
    :return:
    """
    assert (CheckWitness(Admin))
    gpKey = _concatkey(GP_PREFIX, gpId)
    assert (not Get(GetContext(), gpKey))
    gpMap = {"price":price}
    content = []
    # ta means [tokenId_n, amount_n]
    for ta in gpContent:
        tokenId = ta[0]
        amount = ta[1]
        # make sure the tokenId is legal
        assert (tokenId >= 1001 and tokenId <= 999999)
        # make sure the tokenId has been created in property contract
        res = DynamicAppCall(getPropertyReversedHash(), "_tokenExist", [tokenId])
        assert (res)
        assert (amount > 0)
        content.append([tokenId, amount])
    contentInfo = Serialize(content)
    gpMap["content"] = contentInfo
    # put the gp info into the storage
    Put(GetContext(), _concatkey(GP_PREFIX, gpId), Serialize(gpMap))

    Notify(["setGP", gpId, price, gpContent])
    return True


def withdraw(toAcct, amount):
    """
    :param toAcct: the account that will receive the asset coming from preSale
    :param amount: the amount of asset will be withdrawn to toAcct
    :return:
    """
    assert (CheckWitness(Admin))
    assert (_tranferNativeAsset(ONGAddress, SelfContractAddress, toAcct, amount))
    Notify(["withdraw", toAcct, amount])
    return True

def pause():
    assert (CheckWitness(Admin))
    Put(GetContext(), PRESALE_PAUSED_KEY, "T")
    Notify(["pause"])
    return True

def unpause():
    assert (CheckWitness(Admin))
    Put(GetContext(), PRESALE_PAUSED_KEY, "F")
    Notify(["unpause"])
    return True

def migrateContract(code, needStorage, name, version, author, email, description):
    assert (CheckWitness(Admin))
    assert (_whenNotPaused() == False)
    param = state(SelfContractAddress)
    totalOngAmount = Invoke(0, ONGAddress, 'balanceOf', param)

    # Option1: TODO
    newContractHash = AddressFromVmCode(code)
    res = _tranferNativeAsset(ONGAddress, SelfContractAddress, newContractHash, totalOngAmount)
    assert (res)

    # Option2: make sure there is no ong left
    assert (totalOngAmount == 0)

    res = Migrate(code, needStorage, name, version, author, email, description)
    assert (res)
    Notify(["migreate"])
    return True
############# Methods for Admin account only defination Ends  ################



#################### Purchase method for player Starts  ######################
def purchase(account, gpId):
    """
    Before purchase, make sure
    1. CEO in Property contract has make the preSaleProperty.py contract as the authorized account
    2. Admin has run setGP() to store the package info within preSaleProperty contract.
    :param account:
    :param gpId:
    :return:
    """
    assert (_whenNotPaused())
    assert (CheckWitness(account))
    # get the gift package info
    priceContent = getGP(gpId)
    assert (len(priceContent) == 2)
    price = priceContent[0]
    content = priceContent[1]
    # transfer ONG from account to the contract
    assert (_tranferNativeAsset(ONGAddress, account, SelfContractAddress, price))
    # mint all the tokens within the gpId gift package.
    argsForMultiMintToken = []
    for ta in content:
        tokenId = ta[0]
        amount = ta[1]
        argsForMultiMintToken.append([account, tokenId, amount])

    assert (DynamicAppCall(getPropertyReversedHash(), "multiMintToken", argsForMultiMintToken))
    Notify(["purchase", account, gpId, price])
    return True
#################### Purchase method for player Ends  ######################


#################### Pre-execute methods defination Starts  ######################
def getPropertyReversedHash():
    return Get(GetContext(), PROPERTY_REVERSED_HASH_KEY)


def getGP(gpId):
    gpMapInfo = Get(GetContext(), _concatkey(GP_PREFIX, gpId))
    if not gpMapInfo:
        return False
    gpMap = Deserialize(gpMapInfo)
    price = gpMap["price"]
    contentInfo = gpMap["content"]
    content = Deserialize(contentInfo)
    return [price, content]
#################### Pre-execute methods defination Ends  ######################


#################### Private methods defination starts ######################
def _whenNotPaused():
    isPaused = Get(GetContext(), PRESALE_PAUSED_KEY)
    if isPaused == "T":
        return False
    elif isPaused == "F":
        return True


def _tranferNativeAsset(_nativeAssetAddress, _from, _to, _amount):
    param = state(_from, _to, _amount)
    res = Invoke(0, _nativeAssetAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False


def _concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)
#################### Private methods defination Ends ######################