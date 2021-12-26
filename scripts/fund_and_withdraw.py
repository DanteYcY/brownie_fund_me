from brownie import FundMe
from scripts.helpful_scripts import get_account, deploy_mocks


def fund():
    # because we already deploy FundMe contracts to the blockchain
    # here we get the last contract deployed
    fund_me = FundMe[-1]
    # get our account information
    account = get_account()
    # use the getEntranceFee function from the deployed contract
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    # from our address, use the fund function in the deployed contract to send eth to that contract
    fund_me.fund({"from": account, "value": entrance_fee + 100})


def withdraw():
    # again we get the last deployed fundme contract
    fund_me = FundMe[-1]
    # get the account information
    account = get_account()
    # we use the withdraw function in the deployed contract to get all the stored money back to our account
    fund_me.withdraw({"from": account})


def main():
    # here's a good example how main() function is used to set the sequence
    fund()
    withdraw()