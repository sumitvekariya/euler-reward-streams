// SPDX-License-Identifier: GPL-2.0-or-later
methods {
    // View functions
    function balanceOf(address, address) external returns (uint256) envfree;
    function currentEpoch() external returns (uint48) envfree;
    function totalRewardRegistered(address, address) external returns (uint256) envfree;
    function totalRewardClaimed(address, address) external returns (uint256) envfree;
    function totalRewardedEligible(address, address) external returns (uint256) envfree;
    function EPOCH_DURATION() external returns (uint256) envfree;
    
    // Constants
    function MAX_EPOCHS_AHEAD() external returns (uint256) envfree;
    function MAX_DISTRIBUTION_LENGTH() external returns (uint256) envfree;
    function MAX_REWARDS_ENABLED() external returns (uint256) envfree;
}

// Basic invariants
invariant totalClaimedLessThanRegistered(address rewarded, address reward)
    totalRewardClaimed(rewarded, reward) <= totalRewardRegistered(rewarded, reward);

// Rule to verify reward registration constraints
rule registerRewardRules(address rewarded, address reward, uint48 startEpoch, uint128[] amounts) {
    env e;
    
    require amounts.length <= MAX_DISTRIBUTION_LENGTH();
    require startEpoch <= currentEpoch() + MAX_EPOCHS_AHEAD();
    
    registerReward(e, rewarded, reward, startEpoch, amounts);
    
    assert totalRewardRegistered(rewarded, reward) > 0, 
        "Total registered rewards should be positive after registration";
}

// Rule to verify reward claiming
rule claimRewardRules(address rewarded, address reward, address recipient) {
    env e;
    
    uint256 balanceBefore = balanceOf(e.msg.sender, rewarded);
    uint256 totalClaimedBefore = totalRewardClaimed(rewarded, reward);
    
    claimReward(e, rewarded, reward, recipient, false);
    
    uint256 totalClaimedAfter = totalRewardClaimed(rewarded, reward);
    
    assert totalClaimedAfter >= totalClaimedBefore, 
        "Total claimed should not decrease";
    assert totalClaimedAfter <= totalRewardRegistered(rewarded, reward),
        "Cannot claim more than registered";
}

// Rule to verify reward enabling constraints
rule enableRewardRules(address rewarded, address reward) {
    env e;
    
    enableReward(e, rewarded, reward);
    
    address[] rewards = enabledRewards(e.msg.sender, rewarded);
    assert rewards.length <= MAX_REWARDS_ENABLED(),
        "Cannot enable more than MAX_REWARDS_ENABLED rewards";
}

// Rule to verify total eligible amount updates correctly
rule totalEligibleUpdateRules(method f) {
    env e;
    
    address rewarded;
    address reward;
    
    uint256 eligibleBefore = totalRewardedEligible(rewarded, reward);
    
    calldataarg args;
    f(e, args);
    
    uint256 eligibleAfter = totalRewardedEligible(rewarded, reward);
    
    assert eligibleAfter != eligibleBefore => 
        (f.selector == sig:enableReward(address,address).selector ||
         f.selector == sig:disableReward(address,address,bool).selector),
        "Total eligible should only change on enable/disable";
}