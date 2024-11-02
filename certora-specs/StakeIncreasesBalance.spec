rule StakeIncreasesBalance {
    StakingRewardStreams stream;
    address user;
    uint initialStake = stream.stakes[user];
    uint stakeAmount = 10;
    stream.stake(user, stakeAmount);
    invariant stream.stakes[user] == initialStake + stakeAmount;
}
