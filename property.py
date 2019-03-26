OntCversion = '2.0.0'
"""
This is the property smart contract of OEP-8 type
"""
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, Notify, Deserialize, Serialize
from ontology.interop.System.Action import RegisterAction

from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, len, append, remove



TransferEvent = RegisterAction("transfer", "fromAcct", "toAcct", "tokenId", "amount")
ApprovalEvent = RegisterAction("approval", "owner", "spender", "tokenId", "amount")

# modify to the admin address
CEO_ADDRESS_KEY = "CEO"
CTO_ADDRESS_KEY = "CTO"
COO_ADDRESS_KEY = "COO"
AUTHORIZED_ADDRESS_LIST_KEY = "AuthorizedAddress"
CEOAddress = Base58ToAddress('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p')


CONTRACT_PAUSED_KEY = "Pause"
# NAME_PREFIX + tokenId --- to store the name of the tokenId token
NAME_PREFIX = 'Name'
# SYMBOL_PREFIX + tokenId --- to store the symbol of the tokenId token
SYMBOL_PREFIX = 'Symbol'
#  BALANCE_PREFIX + tokenId + address --- to store the balance of address in terms of the TOKEN_ID token
BALANCE_PREFIX = 'Balance'
# APPROVE_PREFIX + tokenId + owner + spender -- to store the approved TOKEN_ID amount to the spender by the owner
APPROVE_PREFIX = 'Approve'
# TOTAL_SUPPLY + tokenId  --- to store the total supply of the TOKEN_ID token
TOTAL_SUPPLY_PREFIX = 'TotalSupply'


def Main(operation, args):
    ########################## Methods that meet the OEP8 protocal Starts ############################
    if operation == "name":
        assert (len(args) == 1)
        tokenId = args[0]
        return name(tokenId)
    if operation == "symbol":
        assert (len(args) == 1)
        tokenId = args[0]
        return symbol(tokenId)
    if operation == "totalSupply":
        assert (len(args) == 1)
        tokenId = args[0]
        return totalSupply(tokenId)
    if operation == "balanceOf":
        assert (len(args) == 2)
        acct = args[0]
        tokenId = args[1]
        return balanceOf(acct, tokenId)
    if operation == "transfer":
        assert (len(args) == 4)
        fromAcct = args[0]
        toAcct = args[1]
        tokenId = args[2]
        amount = args[3]
        return transfer(fromAcct, toAcct, tokenId, amount)
    if operation == "transferMulti":
        return transferMulti(args)
    if operation == "approve":
        assert (len(args) == 4)
        owner = args[0]
        spender = args[1]
        tokenId = args[2]
        amount = args[3]
        return approve(owner, spender, tokenId, amount)
    if operation == "approveMulti":
        return approveMulti(args)
    if operation == "allowance":
        assert (len(args) == 3)
        owner = args[0]
        spender = args[1]
        tokenId = args[2]
        return allowance(owner, spender, tokenId)
    if operation == "transferFrom":
        assert (len(args) == 5)
        spender = args[0]
        fromAcct = args[1]
        toAcct = args[2]
        tokenId = args[3]
        amount = args[4]
        return transferFrom(spender, fromAcct, toAcct, tokenId, amount)
    if operation == "transferFromMulti":
        return transferFromMulti(args)
    ########################## Methods that meet the OEP8 protocal Ends ############################
    #################### Special methods for CEO only defination starts  ######################
    if operation == "setCLevel":
        assert (len(args) == 2)
        option = args[0]
        account = args[1]
        return setCLevel(option, account)
    if operation == "setAuthorizedLevel":
        assert (len(args) == 1)
        account = args[0]
        return setAuthorizedLevel(account)
    if operation == "removeAuthorizedLevel":
        assert (len(args) == 1)
        account = args[0]
        return removeAuthorizedLevel(account)
    if operation == "createToken":
        assert (len(args) == 3)
        tokenId = args[0]
        name = args[1]
        symbol = args[2]
        return createToken(tokenId, name, symbol)
    if operation == "multiCreateToken":
        return multiCreateToken(args)
    #################### Special methods for CEO only defination Ends  ######################
    ############# Special methods for C Level accounts only defination Starts  ################
    if operation == "pause":
        return pause()
    if operation == "unpause":
        return unpause()
    ############# Special methods for C Level accounts only defination Ends  ################
    ############# Special methods for C Level and authorized level defination Starts  ################
    if operation == "mintToken":
        assert (len(args) == 3)
        toAcct = args[0]
        tokenId = args[1]
        amount = args[2]
        return mintToken(toAcct, tokenId, amount)
    if operation == "multiMintToken":
        return multiMintToken(args)
    if operation == "burnToken":
        assert (len(args) == 3)
        account = args[0]
        tokenId = args[1]
        amount = args[2]
        return burnToken(account, tokenId, amount)
    if operation == "multiBurnToken":
        return multiBurnToken(args)
    ############# Special methods for C Level and authorized level defination Ends  ################
    #################### Optional methods defination starts  ######################
    if operation == "getCTO":
        return getCTO()
    if operation == "getCOO":
        return getCOO()
    if operation == "getAuthorizedLevel":
        return getAuthorizedLevel()
    #################### Optional methods defination Ends ######################
    if operation == "_tokenExist":
        assert (len(args) == 1)
        tokenId = args[0]
        return _tokenExist(tokenId)
    return False

########################## Methods that meet the OEP8 protocal Starts ############################
def name(tokenId):
    """
    :param tokenId: helps to format name key = NAME_PREFIX + tokenId
    :return: name of the token with tokenId
    """
    return Get(GetContext(), _concatkey(NAME_PREFIX, tokenId))


def symbol(tokenId):
    """
    :param tokenId: helps to format symbol key = SYMBOL_PREFIX + tokenId
    :return: symbol of token with tokenId
    """
    return Get(GetContext(), _concatkey(SYMBOL_PREFIX, tokenId))


def totalSupply(tokenId):
    """
    :param tokenId:  helps to format totalSupply key = TOTAL_SUPPLY + tokenId
    :return: total supply of token with tokenId
    """
    return Get(GetContext(), _concatkey(TOTAL_SUPPLY_PREFIX, tokenId))


def balanceOf(acct, tokenId):
    """
    get balance of account in terms of token with the tokenId
    :param acct: used to check the acct balance
    :param tokenId: the tokenId determines which token balance of acct needs to be checked
    :return: the balance of acct in terms of tokenId tokens
    """
    return Get(GetContext(), _concatkey(_concatkey(BALANCE_PREFIX, tokenId), acct))

def transfer(fromAcct, toAcct, tokenId, amount):
    """
    transfer amount of tokens in terms of tokenId token from fromAcct to the toAcct
    :param fromAcct:
    :param toAcct:
    :param tokenId:
    :param amount:
    :return:
    """
    assert (_whenNotPaused())
    assert (CheckWitness(fromAcct))
    assert (_tokenExist(tokenId))
    assert (len(fromAcct) == 20)
    assert (len(toAcct) == 20)

    balanceKey = _concatkey(BALANCE_PREFIX, tokenId)
    fromKey = _concatkey(balanceKey, fromAcct)
    fromBalance = Get(GetContext(), fromKey)
    if amount > fromBalance or amount <= 0:
        return False
    if amount == fromBalance:
        Delete(GetContext(), fromKey)
    else:
        Put(GetContext(), fromKey, fromBalance - amount)

    toKey = _concatkey(balanceKey, toAcct)
    toBalance = Get(GetContext(), toKey)
    Put(GetContext(), toKey, toBalance + amount)

    TransferEvent(fromAcct, toAcct, tokenId, amount)

    return True


def transferMulti(args):
    """
    multi transfer
    :param args:[[fromAccount1, toAccount1, tokenId1, amount1],[fromAccount2, toAccount2, tokenId2, amount2]]
    :return: True or raise exception
    """
    for p in args:
        assert (len(p) == 4)
        assert (transfer(p[0], p[1], p[2], p[3]))
    return True


def approve(owner, spender, tokenId, amount):
    """
    approve amount of the tokenId token to toAcct address, it can overwrite older approved amount
    :param owner:
    :param spender:
    :param tokenId:
    :param amount:
    :return:
    """
    assert (_whenNotPaused())
    # make sure the invoker is the owner address
    assert (CheckWitness(owner))
    # make sure the address is legal
    assert (len(spender))
    assert (_tokenExist(tokenId))

    ownerBalance = balanceOf(owner, tokenId)
    # you can use "if" to notify the corresponding message, or use assert to raise exception
    assert (ownerBalance >= amount)
    assert (amount > 0)
    key = _concatkey(_concatkey(_concatkey(APPROVE_PREFIX, tokenId), owner), spender)
    Put(GetContext(), key, amount)

    ApprovalEvent(owner, spender, tokenId, amount)

    return True



def approveMulti(args):
    """
    multi approve
    :param args: args:[[owner1, spender1, tokenId1, amount1],[owner2, spender2, tokenId2, amount2]]
    :return:
    """
    for p in args:
        assert (len(p) == 4)
        assert (approve(p[0], p[1], p[2], p[3]))
    return True


def allowance(owner, spender, tokenId):
    """
    :param owner:
    :param spender:
    :param tokenId:
    :return:
    """
    key = _concatkey(_concatkey(_concatkey(APPROVE_PREFIX, tokenId), owner), spender)
    return Get(GetContext(), key)



def transferFrom(spender, fromAcct, toAcct, tokenId, amount):
    """
    :param tokenId: this tokenId token should be approved by its owner to toAcct
    :param toAcct: spender
    :param amount: False or True
    :return:
    """
    assert (_whenNotPaused())
    assert (CheckWitness(spender))
    assert (len(fromAcct) == 20)
    assert (len(toAcct) == 20)
    assert (_tokenExist(tokenId))

    fromKey = _concatkey(_concatkey(BALANCE_PREFIX, tokenId), fromAcct)
    fromBalance = Get(GetContext(), fromKey)
    assert (fromBalance >= amount)
    assert (amount > 0)
    toKey = _concatkey(_concatkey(tokenId, BALANCE_PREFIX), toAcct)


    approvedKey = _concatkey(_concatkey(_concatkey(APPROVE_PREFIX, tokenId), fromAcct), spender)
    approvedAmount = Get(GetContext(), approvedKey)

    assert (approvedAmount >= amount)
    if amount == approvedAmount:
        Delete(GetContext(), approvedKey)
        Put(GetContext(), fromKey, fromBalance - amount)
    else:
        Put(GetContext(), approvedKey, approvedAmount - amount)
        Put(GetContext(), fromKey, fromBalance - amount)

    toBalance = Get(GetContext(), toKey)
    Put(GetContext(), toKey, toBalance + amount)

    TransferEvent(fromAcct, toAcct, tokenId, amount)

    return True


def transferFromMulti(args):
    """
    multiple transferFrom
    :param args: args:[[spender1, fromAcct1, toAcct1, tokenId1, amount1],[spender2, fromAcct2, toAcct2, tokenId2, amount2]]
    :return:
    """
    for p in args:
        assert (len(p) == 5)
        assert (transferFrom(p[0], p[1], p[2], p[3], p[4]))
    return True
########################## Methods that meet the OEP8 protocal Ends ############################



#################### Special methods for CEO only defination starts  ######################
def setCLevel(option, account):
    """

    :param option: can be "CTO", "COO"
    :param account: the account to be set as the CLevel account
    :return:
    """
    assert (CheckWitness(CEOAddress))
    CLevelKey = None
    if option == "CTO":
        CLevelKey = CTO_ADDRESS_KEY
    elif option == "COO":
        CLevelKey = COO_ADDRESS_KEY
    Put(GetContext(), CLevelKey, account)
    Notify(["setCLevel", option, account])
    return True

def setAuthorizedLevel(account):
    assert (CheckWitness(CEOAddress))
    assert (len(account) == 20)
    authorizedAddressList = []
    authorizedAddressListInfo = Get(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY)
    if not authorizedAddressListInfo:
        authorizedAddressList.append(account)
    else:
        authorizedAddressList = Deserialize(authorizedAddressListInfo)
        if _checkInList(account, authorizedAddressList):
            Notify(["alreadyInAuthorizedLevel", account])
            return True
        else:
            authorizedAddressList.append(account)
    Put(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY, Serialize(authorizedAddressList))
    Notify(["setAuthorizedLevel", account])
    return True

def removeAuthorizedLevel(account):
    assert (CheckWitness(CEOAddress))
    assert (len(account) == 20)
    authorizedAddressListInfo = Get(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY)
    assert (authorizedAddressListInfo)
    authorizedAddressList = Deserialize(authorizedAddressListInfo)
    assert (_checkInList(account, authorizedAddressList))
    index = _findInList(account, authorizedAddressList)
    # make sure index did exist in authorizedAddressList
    assert (index < len(authorizedAddressList) - 1)
    authorizedAddressList.remove(index)
    Put(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY, Serialize(authorizedAddressList))
    Notify(["removeAuthorizedLevel", account])
    return True


def createToken(tokenId, name, symbol):
    assert (_whenNotPaused())
    assert (CheckWitness(CEOAddress))
    assert (not name(tokenId))
    assert (_checkLegalTokenId(tokenId))
    # Put name and symbol in storage
    Put(GetContext(), _concatkey(NAME_PREFIX, tokenId), name)
    Put(GetContext(), _concatkey(SYMBOL_PREFIX, tokenId), symbol)
    # By default, the total supply is zero

    Notify(["createToken", tokenId, name, symbol])
    return True

def multiCreateToken(args):
    """
    :param tokenIdList:
    :param nameList:
    :param symbolList:
    :return:
    """
    for p in args:
        assert (len(p) == 3)
        assert (createToken(p[0], p[1], p[2]))
    return True

#################### Special methods for CEO only defination Ends  ######################


############# Special methods for C Level accounts only defination Starts  ################
def pause():
    assert (_onlyCLevel())
    Put(GetContext(), CONTRACT_PAUSED_KEY, "T")
    Notify(["pause"])
    return True

def unpause():
    assert (_onlyCLevel())
    Put(GetContext(), CONTRACT_PAUSED_KEY, "F")
    Notify(["unpause"])
    return True
############# Special methods for C Level accounts only defination Ends  ################



############# Special methods for C Level and authorized level defination Starts  ################
def mintToken(toAcct, tokenId, amount):
    assert (_whenNotPaused())
    assert (_onlyCLevel() or _onlyAuthorizedLevel())
    # make sure the to address is legal
    assert (len(toAcct) == 20)
    # make sure the tokenId has been created already
    assert (_tokenExist(tokenId))
    # make sure the amount is legal, which is greater than ZERO
    assert (amount > 0)
    # update the to account balance
    Put(GetContext(), _concatkey(_concatkey(BALANCE_PREFIX, tokenId), toAcct), balanceOf(toAcct, tokenId) + amount)
    # update the total supply
    Put(GetContext(), _concatkey(TOTAL_SUPPLY_PREFIX, tokenId), totalSupply(tokenId) + amount)
    # make sure the total supply is not greater than 1 billion
    assert (totalSupply(tokenId) <= 10000000000)
    # Notify the event to the block chain
    TransferEvent("", toAcct, tokenId, amount)
    return True

def multiMintToken(args):
    for p in args:
        assert (len(p) == 3)
        assert (mintToken(p[0], p[1], p[2]))
    return True

def burnToken(account, tokenId, amount):
    assert (_whenNotPaused())
    assert (_onlyCLevel())
    # make sure the tokenId has been created already
    assert (_tokenExist(tokenId))
    # make sure the amount is legal, which is greater than ZERO
    balance = balanceOf(account, tokenId)
    assert (amount > 0 and amount < balance)
    # update the to account balance
    Put(GetContext(), _concatkey(_concatkey(BALANCE_PREFIX, tokenId), account), balance - amount)
    # update the total supply
    Put(GetContext(), _concatkey(TOTAL_SUPPLY_PREFIX, tokenId), totalSupply(tokenId) - amount)
    # Notify the event to the block chain
    TransferEvent(account, "", tokenId, amount)
    return True

def multiBurnToken(args):
    for p in args:
        assert (len(p) == 3)
        assert (burnToken(p[0], p[1], p[2]))
    return True
############# Special methods for C Level and authorized level defination Ends  ################



#################### Optional methods defination starts  ######################
def getCTO():
    """
    :return: the CTO address
    """
    return Get(GetContext(), CTO_ADDRESS_KEY)

def getCOO():
    """
    :return: the COO address
    """
    return Get(GetContext(), COO_ADDRESS_KEY)

def getAuthorizedLevel():
    authorizedAddressListInfo = Get(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY)
    if  authorizedAddressListInfo:
        return Deserialize(authorizedAddressListInfo)
    else:
        return []
#################### Optional methods defination Ends ######################



#################### Private methods defination starts ######################
def _onlyCLevel():
    isCEO = CheckWitness(CEOAddress)
    isCTO = CheckWitness(getCTO())
    isCOO = CheckWitness(getCOO())
    return isCEO or isCTO or isCOO

def _onlyAuthorizedLevel():
    authorizedAddressListInfo = Get(GetContext(), AUTHORIZED_ADDRESS_LIST_KEY)
    if not authorizedAddressListInfo:
        return False
    authorizedAddressList = Deserialize(authorizedAddressListInfo)
    for authorizedAddress in authorizedAddressList:
        if CheckWitness(authorizedAddress):
            return True
    return False

def _whenNotPaused():
    isPaused = Get(GetContext(), CONTRACT_PAUSED_KEY)
    if isPaused == "T":
        return False
    elif isPaused == "F":
        return True

def _checkLegalTokenId(tokenId):
    """
    AAA,BBB
    :param tokenId: integer AAA = 001, 002, 003, ..., 999; BBB = 001, 002, 003, ..., 999
    :return: True or False
    """
    return tokenId >= 1001 and tokenId <= 999999

def _tokenExist(tokenId):
    if name(tokenId):
        return True
    else:
        return False

def _checkInList(e, l):
    for eInl in l:
        if eInl == e:
            return True
    return False

def _findInList(e, l):
    index = 0
    for eInl in l:
        if eInl == e:
            return index
        index = index + 1
    return index


def _concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)
#################### Private methods defination Ends ######################