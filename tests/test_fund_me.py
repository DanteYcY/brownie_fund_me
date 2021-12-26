from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest
import time


def test_can_fund_and_withdraw():
    # Arrange
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    # Act
    # to avoid the transaction to be reverted, add extra 100 to the transaction
    tx = fund_me.fund({"from": account, "value": entrance_fee + 100})
    # when test on fork mainnet, please wait for more time for the chain to react
    tx.wait(1)
    time.sleep(5)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee + 100
    # Act
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    time.sleep(5)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # if the test is not local, pytest will skip the test and return a message
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # exceptions mean we want a result that cannot be passed
    # we can use the exact error information here to let pytest know what mistake we want to see
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})