# @version ^0.3.0

# @dev minimal Staking contract.
# @author Egboluche Francis

balances: public(HashMap[address, uint256])

event Stake:
    staker: indexed(address)
    amount_staked: indexed(uint256)
    on_behalf: indexed(address)

event Unstake:
    unstaker: indexed(address)
    amount_unstaked: indexed(uint256)
    to: indexed(address)

@external
@payable
def stake():
    # @dev user deposits some native asset into contract for themselves
    assert msg.value > 0
    self.balances[msg.sender] += msg.value
    log Stake(msg.sender, msg.value, msg.sender)

@external
@payable
def stake_for(_addr: address):
    # @dev sender stakes some native assets into contract for another address
    # @param _addr the address balance being updated
    assert msg.value > 0
    self.balances[_addr] += msg.value
    log Stake(msg.sender, msg.value, _addr)

@external
def unstake(_amount: uint256):
    # @dev sender removes staked asset from contract for themselves
    # @param _amount the amount of asset being unstaked
    if self.balances[msg.sender] < _amount:
        raise "balance < amount"
    self.balances[msg.sender] -= _amount
    send(msg.sender, _amount)
    log Unstake(msg.sender, _amount, msg.sender)

@external
def unstake_to(_to: address, _amount: uint256):
    # @dev sender removes staked asset from contract for themselves
    # @param _to the address receiving the unstaked asset
    # @param _amount the amount being removed from senders balance
    if self.balances[msg.sender] < _amount:
        raise "balance < amount"
    self.balances[msg.sender] -= _amount
    send(_to, _amount)
    log Unstake(msg.sender, _amount, _to)

