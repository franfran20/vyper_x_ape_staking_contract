import pytest

@pytest.fixture
def minimal_staking_contract(accounts, project):
    account = accounts[0]
    return project.minimalStaking.deploy(sender=account)