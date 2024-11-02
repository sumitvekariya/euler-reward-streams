rule OnlyOwnerCanAddRewards {
    BaseRewardStreams stream;
    requires msg.sender == OWNER;
    addRewards(stream, amount);
}
