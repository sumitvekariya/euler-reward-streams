rule DistributionCorrectness {
    BaseRewardStreams stream;
    uint initialBalance = stream.totalRewardBalance;
    uint distributedAmount = distributeRewards(stream, amount);
    invariant stream.totalRewardBalance == initialBalance - distributedAmount;
}
