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




---------------------------------------------------------------------------------------------------------------------------------------------
pragma solidity ^0.8.0;

contract InsurancePolicy {

// The address of the policyholder
address public policyholder;

// The address of the insurance company
address public insuranceCompany;

// The start date of the policy
uint256 public startDate;

// The end date of the policy
uint256 public endDate;

// The amount of the policy
uint256 public amount;

// The status of the policy
enum Status { ACTIVE, INACTIVE, EXPIRED }
Status public status;

// An event to emit when the policy is created
event PolicyCreated(address policyholder, address insuranceCompany, uint256 amount);

// An event to emit when the policy is cancelled
event PolicyCancelled(address policyholder, address insuranceCompany);

// An event to emit when the policy is paid out
event PolicyPaidOut(address policyholder, address insuranceCompany, uint256 amount);

// Constructor function
constructor(address _policyholder, address _insuranceCompany, uint256 _amount) {
    policyholder = _policyholder;
    insuranceCompany = _insuranceCompany;
    amount = _amount;
    startDate = block.timestamp;
    endDate = startDate + 5 years;
    status = Status.ACTIVE;
    emit PolicyCreated(policyholder, insuranceCompany, amount);
}

// Function to cancel the policy
function cancelPolicy() public {
    require(msg.sender == policyholder, "Only the policyholder can cancel the policy");
    require(status == Status.ACTIVE, "Policy is not active");
    status = Status.INACTIVE;
    emit PolicyCancelled(policyholder, insuranceCompany);
}

// Function to pay out the policy
function payOutPolicy() public {
    require(msg.sender == insuranceCompany, "Only the insurance company can pay out the policy");
    require(status == Status.ACTIVE, "Policy is not active");
    require(block.timestamp >= endDate, "Policy has not expired");
    status = Status.EXPIRED;
    insuranceCompany.transfer(amount);
    emit PolicyPaidOut(policyholder, insuranceCompany, amount);
}
}
