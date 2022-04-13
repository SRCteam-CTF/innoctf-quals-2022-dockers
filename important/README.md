# Important

* Category: Reverse, Blockchain
* Difficulty: Middle
* Flag: `Ararat{L00k_At_tH3_V3ry_Imp0rtant_C0ntr4ct}`

**Description**

We have important news! Our agents found out that the creator of this smart contract is hiding some secret information that can be made public at any time. It is urgent to find out what this information is and take appropriate measures to mitigate the possible consequences.

Contract address: `0x92dF986e7B002fA9Eb2eDd04125204CACDb36f30`

### Idea

A smart contract that takes a secret key as an argument to the constructor during its creation and has a function for taking already encrypted data. Also, there is a function to decrypt the data using secret key, then it will be publicly sent in the transaction. All functions can be called by contract owner only, no source code, no abi for Decryptor contract. Need to reverse the bytecode and decrypt information from transactions, where will be the flag

### Run

`ganache -i 1337 --wallet.seed 1337`

To run test:

```
truffle test test/important.js --network ganache
```

To deploy in ganache:

```
truffle migrate --network ganache --reset
```

To deploy in bsc_testnet:

```
truffle migrate --network bsc_testnet --reset
```
