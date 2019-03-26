property.py is the OEP8 smart contract for property. The usage of methods that meet the OEP8 protocal can be referred [here](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-8.mediawiki). 

The other methods are the following.
## methods for CEO account to be invoked:

1. ```setCLevel(option, account)``` 

The CEO account can set(reset) CTO and COO account. 

The option should be "CTO" or "COO".

2. ```createToken(tokenId, name, symbol)``` 

The CEO account can create a type of token.

tokenId should be Integer type and the range should be no less than 1001 and no more than 999999.

name should be the name of this type of token.

symbol should be the symbol of this type of token.

3. ```multiCreateToken(args)```

The CEO account can create multiple types of tokens.

## methods for C Level accounts only

4. ```pause()```

5. ```unpause()```

These two methods are for C level accounts(CEO, CTO, COO) to pause the property contract. Once the contract is paused, all the asset transaction will be frozen.

## Methods for C Level and authorized level 

6. ```mintToken(toAcct, tokenId, amount)```

C level and authorized level accounts have the right to mint token (make sure the ```tokenId``` type of token has been created before).

```toAcct``` is the account  that will received ```amount``` of tokens of ```tokenId``` type.

7. ```multiMintToken(args)```

C level and authorized level accounts can mint multiple types of tokens simultaneously.

8. ```burnToken(account, tokenId, amount)```

C level and authorized level accounts have the right to burn token.

9. ```multiBurnToken(args)```

C level and authorized level accounts can burn multiple types of tokens simultaneously.

## Other methods can be pre-execute by everybody

10. ```getCTO()```

Return the CTO address


11. ```getCOO()```

Return the COO address
