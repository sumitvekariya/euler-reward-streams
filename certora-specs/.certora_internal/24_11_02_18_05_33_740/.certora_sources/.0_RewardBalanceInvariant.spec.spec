rule RewardBalanceInvariant {
    BaseRewardStreams stream;
    invariant stream.totalRewardBalance <= MAX_UINT;
}
