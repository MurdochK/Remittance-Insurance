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
