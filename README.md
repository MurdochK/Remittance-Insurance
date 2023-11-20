# Remittance-

pragma solidity ^0.8.0;

contract InsuranceContract {

    enum PolicyStatus { ACTIVE, PENDING, CLAIMED }

    struct Policy {
        address policyholder;
        uint256 policyAmount;
        PolicyStatus status;
    }

    mapping(address => Policy) public policies;

    event PolicyCreated(address policyholder,


**********************************************


pragma solidity ^0.8.0;

contract InsuranceContract {

    enum PolicyStatus { ACTIVE, PENDING, CLAIMED, PAID }

    struct Policy {
        address policyholder;
        uint256 policyAmount;
        PolicyStatus status;
    }

    mapping(address => Policy) public policies;

    address public authorizedPayer;

    event PolicyCreated(address policyholder, uint256 policyAmount);
    event PolicyClaimed(address policyholder, uint256 payout);
    event PaymentAuthorized(address policyholder, uint256 payout);

    constructor(address _authorizedPayer) {
        authorizedPayer = _authorizedPayer;
    }

    function createPolicy(uint256 policyAmount) public {
        require(policyAmount > 0);

        Policy memory policy = Policy({
            policyholder: msg.sender,
            policyAmount: policyAmount,
            status: PolicyStatus.ACTIVE
        });

        policies[msg.sender] = policy;

        emit PolicyCreated(msg.sender, policyAmount);
    }

    function claimPolicy() public {
        require(policies[msg.sender].status == PolicyStatus.ACTIVE);

        policies[msg.sender].status = PolicyStatus.PENDING;

        emit PolicyClaimed(msg.sender, policies[msg.sender].policyAmount);
    }

    function authorizePayment(address policyholder) public {
        require(msg.sender == authorizedPayer);
        require(policies[policyholder].status == PolicyStatus.PENDING);

        // Calculate the payout amount.
        uint256 payoutAmount = policies[policyholder].policyAmount;

        // Transfer the payout amount to the policyholder.
        payable(policyholder).transfer(payoutAmount);

        // Update the policy status to `PAID`.
        policies[policyholder].status = PolicyStatus.PAID;

        // Emit the `PaymentAuthorized` event.
        emit PaymentAuthorized(policyholder, payoutAmount);
    }

    function getPolicy(address policyholder) public view returns (Policy memory) {
        return policies[policyholder];
    }
}

#try find the telematics code to integrate to this then run
