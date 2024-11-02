rule BalanceTrackingAccuracy {
    TrackingRewardStreams stream;
    address user;
    uint initialBalance = stream.trackedBalances[user];
    uint rewardAmount = 10;
    stream.trackReward(user, rewardAmount);
    invariant stream.trackedBalances[user] == initialBalance + rewardAmount;
}
