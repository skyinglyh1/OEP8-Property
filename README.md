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

14. ```getAuthorizedLevel()```

Return the authorized account in a list


## preSaleProperty.py

This is the pre sale smart contract for property tokens.

####  Methods for Admin account only
1. ```setPropertyHash(propertyReversedHash)``` 

```Admin``` account can set the reversed property contract hash in the pre sale contract.

2. ```setGP(gpId, price, gpContent)```

```Admin``` account can set(or add) the gift package.

```gpId``` is can be anything, as long as we keep the format next time we need to pass in gpId.

```price``` should be the ONG amount for gpId gift package. Say, if we mean 2 ONG, we should set the price as 2000000000.

```gpContent``` should be a list(or an array). Say, ```[[tokenId1, amount1], [tokenId2, amount2], ..., [tokenIdN, amountN]]```

3. ```withdraw(toAcct, amount)```

```Admin``` account can withdraw the pre sale asset to ```toAcct``` with amount of ONG.

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
