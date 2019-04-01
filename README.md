## property.py 
 This is the OEP8 smart contract for property. The usage of methods that meet the OEP8 protocal can be referred [here](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-8.mediawiki). 

The other methods are the following.
#### methods for CEO account to be invoked:

1. ```setCLevel(option, account)``` 

The CEO account can set(reset) CTO and COO account. 

The option should be "CTO" or "COO".

2 ```setAuthorizedLevel(account)```

The CEO account can set the ```account``` as the authorized level.

3 ```removeAuthorizedLevel(account)```

The CEO account can delete the ```account``` from the authorized level accounts.

4. ```createToken(tokenId, name, symbol)``` 

The CEO account can create a type of token.

tokenId should be Integer type and the range should be no less than 1001 and no more than 999999.

name should be the name of this type of token.

symbol should be the symbol of this type of token.

5. ```multiCreateToken(args)```

The CEO account can create multiple types of tokens.

#### methods for C Level accounts only

6. ```pause()```

7. ```unpause()```

These two methods are for C level accounts(CEO, CTO, COO) to pause the property contract. Once the contract is paused, all the asset transaction will be frozen.

#### Methods for C Level and authorized level 

8. ```mintToken(toAcct, tokenId, amount)```

C level and authorized level accounts have the right to mint token (make sure the ```tokenId``` type of token has been created before).

```toAcct``` is the account  that will received ```amount``` of tokens of ```tokenId``` type.

9. ```multiMintToken(args)```

C level and authorized level accounts can mint multiple types of tokens simultaneously.

10. ```burnToken(account, tokenId, amount)```

C level and authorized level accounts have the right to burn token.

11. ```multiBurnToken(args)```

C level and authorized level accounts can burn multiple types of tokens simultaneously.

#### Other methods can be pre-execute by everybody

12. ```getCTO()```

Return the CTO address


13. ```getCOO()```

Return the COO address

14. ```isAuthorizedLevel(account)```

Return True or False to check if account is the authorized account.

Return the authorized account in a list

#### Property Contract Instruction
```markdown
a. Before transfer any asset, make sure the contract is in unpause sttus. The default status of property contract is neither "pause" nor "unpause" after the deployment of contract.

b. Make sure CEO has created the token with tokenId before mint, burn or make any transaction of this type of token.

c. If we want to make another contract as the authorized level account, we need to reverse another contract hash first, then invoke "setAuthorizedLevel(reversedContractHash)".
    Note: the account corresponding with a contract is the reversed contract hash.
    Say, the contract hash is cc76b7ac2839fd5937c50fa0317af6337c1c4e07,
    then, the corresponding account is 074e1c7c33f67a31a00fc53759fd3928acb776cc (little endian) or AGSVx7BLruproBK5sRc7yKvfp9EBFs4CHN (base58).

```

## preSaleProperty.py

This is the pre sale smart contract for property tokens.

####  Methods for Admin account only
1. ```setPropertyHash(propertyReversedHash)``` 

```Admin``` account can set the reversed property contract hash in the pre sale contract.

2. ```setGP(gpId, gpLimit, price, gpContent)```

```Admin``` account can set(or add) the gift package.

```gpId``` is can be anything, as long as we keep the format next time we need to pass in gpId.

```gpLimit``` is the available amount of gift package

```price``` should be the ONG amount for gpId gift package. Say, if we mean 2 ONG, we should set the price as 2000000000.

```gpContent``` should be a list(or an array). Say, ```[[tokenId1, amount1], [tokenId2, amount2], ..., [tokenIdN, amountN]]```



3. ```withdraw()```

```Admin``` account can withdraw all the ONT/ONG asset within the contract to ```PreSaleReceiver```.

In case someone transfers ong or ont into this contract by accident, Admin can withdraw all the money left in the contract.

Note the usage of amount is the same as gpContent in 2.

5. ```pause()```
6. ```unpause()```

These two methods are for ```Admin``` to pause the property contract. Once the contract is paused, the ```purchase``` function will be frozen.

7. ```purchase(account, gpId)``` is for players to buy gift package.
```account``` is the buyer
```gpId``` is the type of gift package.

8. ```getPropertyReversedHash()```

Return the reversed property smart contract hash

9. ```getGP(gpId)```

```gpId``` refers to a specific gift package.

Return ```[price, [[tokenId1, amount1], [tokenId2, amount2], ..., [tokenIdN, amountN]]]```

10. ```getGPLeft(gpId)```

```gpId``` refers to a specific gift package.

Return the number of gift packages left available for sale.

11. ```setGPMaxPerTx(limit)```

Admin can invoke this method to set the maximum number of GP every time the user purchase gift packages. 

```limit``` is the maximum number of gift packages every time the user can purchase within ONE transaction.

12. ```getGPMaxPerTx()```

Return the maximum number of gift packages every time the user can purchase within ONE transaction.

#### preSale Property Contract Instruction
```markdown
a. "setPropertyHash(propertyReversedHash)" method helps to connect the preSale contract with the property contract. 
    propertyReversedHash should be the reversed contract hash of property contract.
    Say, if the property contract hash is cc76b7ac2839fd5937c50fa0317af6337c1c4e07,
    then, the propertyReversedHash should be 074e1c7c33f67a31a00fc53759fd3928acb776cc.
    This helps preSaleProperty contract dynamically call Property contract to mint tokens and transfer the tokens to the buyer. 


b. "setGP" method helps to create multiple different gift package for the pre sale.
    b.1 make sure the same gpId has not been set before.
    b.2 make sure the tokenIds within the gpId gift package should be created within Property contract.

c. Before invoking "purchase", make sure 
    c.1 the contract is in unpause status. The default status of property contract is neither "pause" nor "unpause" after the deployment of contract.
    c.2 the tokenIds within the gpId gift package should be created within Property contract.
    c.3 the Property contract is in unpause status.
    c.4 the account corresponding with the preSale Property contract has been set as the authorized level account so as to it can mint token in property contract.
    
```