<!DOCTYPE html>
<html>
<head>
  <title>Smart Contract Interaction</title>
  <script src="https://cdn.jsdelivr.net/npm/web3@1.7.3/dist/web3.min.js"></script>
</head>
<body>
  <h1>Smart Contract Interaction</h1>

  <label for="policyholderName">Policyholder Name:</label>
  <input type="text" id="policyholderName" placeholder="Enter policyholder name">
  <br><br>

  <button onclick="deployContract()">Deploy Contract</button>
  <button onclick="callContractFunction()">Call Contract Function</button>
  <br><br>

  <div id="output"></div>

  <script>
    // Initialize Web3.js
    const web3 = new Web3(Web3.givenProvider || "http://localhost:8545");

    // Replace with your smart contract ABI and bytecode
    const contractABI = [/* Your contract ABI */];
    const contractBytecode = "0x/* Your contract bytecode */";

    // Deployed contract instance
    let contractInstance;

    // Deploy the smart contract
    async function deployContract() {
      const accounts = await web3.eth.getAccounts();
      const deployedContract = new web3.eth.Contract(contractABI);

      const hashedName = web3.utils.keccak256(web3.utils.toUtf8Bytes(document.getElementById("policyholderName").value));

      const deployTx = deployedContract.deploy({
        data: contractBytecode,
        arguments: [hashedName]
      });

      const newContractInstance = await deployTx.send({
        from: accounts[0],
        gas: 4000000,
        gasPrice: web3.utils.toWei("10", "gwei")
      });

      contractInstance = newContractInstance;
      document.getElementById("output").textContent = "Contract deployed!";
    }

    // Call a function on the deployed contract
    async function callContractFunction() {
      if (!contractInstance) {
        document.getElementById("output").textContent = "Contract not deployed yet.";
        return;
      }

      const result = await contractInstance.methods.someContractFunction().call();
      document.getElementById("output").textContent = `Contract function result: ${result}`;
    }
  </script>
</body>
</html>
