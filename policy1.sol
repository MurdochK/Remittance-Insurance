// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "@openzeppelin/contracts@4.5.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.5.0/access/Ownable.sol";
import "@openzeppelin/contracts@4.5.0/utils/Counters.sol";
contract CarInsurance is Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _policyIds;

    struct PolicyDetails {
        uint256 policyId;
        address insured;
        uint256 age;
        uint256 premiumAmount;
        uint256 averageSpeed;
        string drivingLocation;
        bool hasTelematics;
        bool drinkingHistory;
        bool healthStatus;
        bool isActuary;
    }

    mapping(uint256 => PolicyDetails) public policies;

    function createPolicy(
        address _insured,
        uint256 _age,
        uint256 _premiumAmount,
        uint256 _averageSpeed,
        string memory _drivingLocation,
        bool _hasTelematics,
        bool _drinkingHistory,
        bool _healthStatus,
        bool _isActuary
    ) public onlyOwner {
        _policyIds.increment();
        uint256 policyId = _policyIds.current();

        PolicyDetails memory policyDetails = PolicyDetails(
            policyId,
            _insured,
            _age,
            _premiumAmount,
            _averageSpeed,
            _drivingLocation,
            _hasTelematics,
            _drinkingHistory,
            _healthStatus,
            _isActuary
        );

        policies[policyId] = policyDetails;
    }

    function getPolicy(uint256 _policyId) public view returns (PolicyDetails memory) {
        return policies[_policyId];
    }
}
