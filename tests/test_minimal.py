from ape import convert, reverts


def test_stake_updates_balances(accounts, minimal_staking_contract):
    account = accounts[0]
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    assert minimal_staking_contract.balances(account) == convert("1 ether", int)

def test_stake_emits_stake_event_with_right_params(accounts, minimal_staking_contract):
    account = accounts[0]
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    for log in minimal_staking_contract.Stake.from_receipt(stake_transaction):
        assert log.staker == account.address
        assert log.amount_staked == convert("1 ether", int)
        assert log.on_behalf == account.address

def test_unstake(accounts, minimal_staking_contract):
    account = accounts[0]
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    unstake_transaction = minimal_staking_contract.unstake(convert("0.5 ether", int), sender=account)
    assert minimal_staking_contract.balances(account) == convert("0.5 ether", int)

def test_unstake_emits_unstake_event_with_right_params(accounts, minimal_staking_contract):
    account = accounts[0]
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    unstake_transaction = minimal_staking_contract.unstake(convert("0.5 ether", int), sender=account)
    for log in minimal_staking_contract.Unstake.from_receipt(unstake_transaction):
        assert log.unstaker == account.address
        assert log.amount_unstaked == convert("1 ether", int)
        assert log.to == account.address
    

def test_unstake_fails_on_insufficient_balance(accounts, minimal_staking_contract):
    account = accounts[0]
    #no stake
    with reverts("balance < amount"):
        minimal_staking_contract.unstake(convert("0.5 ether", int), sender=account)

def test_stake_for(accounts, minimal_staking_contract):
    account = accounts[0]
    account_one = accounts[1]
    stake_transaction = minimal_staking_contract.stake_for(account_one.address, value="1 ether", sender=account)
    assert minimal_staking_contract.balances(account_one) == convert("1 ether", int)

def test_stake_for_emits_stake_event_with_right_params(accounts, minimal_staking_contract):
    account = accounts[0]
    account_one = accounts[1]
    stake_transaction = minimal_staking_contract.stake_for(account_one.address, value="1 ether", sender=account)
    for log in minimal_staking_contract.Stake.from_receipt(stake_transaction):
        assert log.staker == account.address
        assert log.amount_staked == convert("1 ether", int)
        assert log.on_behalf == account_one.address

def test_unstake_to(accounts, minimal_staking_contract):
    account = accounts[0]
    account_one = accounts[1]
    prev_account_one_balance = account_one.balance
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    unstake_transaction = minimal_staking_contract.unstake_to(account_one.address, convert("0.4 ether", int), sender=account)
    assert minimal_staking_contract.balances(account) == convert("0.6 ether", int)
    assert account_one.balance == prev_account_one_balance + convert("0.4 ether", int)


def test_unstake_emits_unstake_event_with_right_params(accounts, minimal_staking_contract):
    account = accounts[0]
    account_one = accounts[1]
    stake_transaction = minimal_staking_contract.stake(value="1 ether", sender=account)
    unstake_transaction = minimal_staking_contract.unstake_to(account_one.address, convert("0.4 ether", int), sender=account)
    for log in minimal_staking_contract.Stake.from_receipt(unstake_transaction):
        assert log.unstaker == account.address
        assert log.amount_unstaked == convert("1 ether", int)
        assert log.to == account_one.address