rule RewardBalanceInvariant {
    BaseRewardStreams stream;
    invariant stream.totalRewardBalance() <= type(uint160).max;
}
