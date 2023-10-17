
# Ledger Web Application with EVM Smart Contract Integration

Created a web application using Flask that interacts with a pre-provided EVM smart contract to add and retrieve ledger entries.


## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    
## Deployment

To deploy this project first create a python vitural environment

```bash
  pip install flask
  pip install web3
  pip install py-solc
  pip install py-solc-x
```
Remember to change your 

```bash
  1 Web3 provider on line no 40 in deploy.py
  2.Change chain id accordingly
  3.Change your address and private key on line 42 and 43

```

Now you just have to run deploy.py file in your machine and go to the loacl host provided .
## Appendix

For web3 provider i have used ganache in my local machine.
You can use any test net or mainnet.
