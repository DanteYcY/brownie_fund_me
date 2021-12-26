from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # use deploy_mocks function to deploy on the local chain with mocking information
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        # this address will be passed to fundme contract and as constructor's first input
        price_feed_address,
        {"from": account},
        # publish_source is used to verify the deployment
        # if true, the whole contract details can be seen on chain
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()