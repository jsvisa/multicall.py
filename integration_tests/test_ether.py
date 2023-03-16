import os
from multicall.service import EtherService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestEther:
    def test_get_balance(self):
        e = EtherService(os.environ["ETHEREUM_PROVIDER_URI"])
        expected = [
            {
                "token": "0x0000000000000000000000000000000000000000",
                "asset": "ETH",
                "account": "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
                "value": 609857489633125806178,
            },
            {
                "token": "0x0000000000000000000000000000000000000000",
                "asset": "ETH",
                "account": "0x72a53cdbbcc1b9efa39c834a540550e23463aacb",
                "value": 29999993290335600000000,
            },
        ]

        result = e.get_balance(
            accounts=[
                "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
                "0x72a53cdbbcc1b9efa39c834a540550e23463aacb",
            ],
            block_id=11953815,
        )
        assert sorted(result, key=lambda x: x["value"]) == expected

    def test_get_balance_in_multi_process(self):
        e = EtherService(os.environ["ETHEREUM_PROVIDER_URI"])
        expected = {
            "0xea674fdde714fd979de3edf0f56aa9716b898ec8": 609857489633125806178,
            "0x72a53cdbbcc1b9efa39c834a540550e23463aacb": 29999993290335600000000,
            "0x000000007c49a78bf26806c1c0141b3dfd30a42d": 1495716565473301780,
            "0x00000000c9916569fd7b3ce71a9d1a169a57e4a0": 1471671113513070280,
            "0x0000000003370b0ee6afe7a56b151f9b81cb62fc": 1834575898568745107,
            "0x00000000759c3c0d892478960244b4dfca4ac0a7": 7672027151194688064,
            "0x0001966cbeecdb86b70f0c1c53d3ac0ade30ed91": 371347902531537632,
            "0x001a181ab8c41045e26dd2245ffcc12818ea742f": 18301790927121192,
            "0x0000000fac3c36158a6e9d42b99998d4f35bd64b": 8850942004402550,
            "0x00000000fbd83b24f02d3197ad03bbed123647fd": 1406130733177165864,
            "0x00000000e003f922f52dc2d1466bcdf38b099c6d": 8192386877782964562,
        }

        result = e.get_balance(
            accounts=list(expected.keys()),
            block_id=11953815,
            max_workers=10,
            batch_size=1,
        )
        balances = {e["account"]: e["value"] for e in result}
        assert balances == expected

    def test_erc20_balance_of_suicided_token(self):
        e = EtherService(os.environ["ETHEREUM_PROVIDER_URI"])
        expected = [
            {
                "token": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                "account": "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
                "value": 2000000,
            },
            {
                "token": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                "account": "0x72a53cdbbcc1b9efa39c834a540550e23463aacb",
                "value": 9000000,
            },
        ]
        # token 0x285 suicided in block 11953816,
        # ref https://cn.etherscan.com/tx/0x2e6dd9c94a4e3880db014e1b753ab87e1b491d1b48651b1845fea0537b8fe198#internal # noqa: E501
        for block_id in (11953815, 11953816, 11953817):
            # get batch token-account balance returns unordered data
            result = e.get_token_balance(
                tokens=[
                    "0x2859021ee7f2cb10162e67f33af2d22764b31aff",
                    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                    "0xdac17f958d2ee523a2206206994597c13d831ec7",
                ],
                accounts=[
                    "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
                    "0x72a53cdbbcc1b9efa39c834a540550e23463aacb",
                ],
                block_id=block_id,
            )
            assert sorted(result, key=lambda x: x["value"]) == expected

    def test_get_balance_with_2000_address(self):
        e = EtherService(os.environ["ETHEREUM_PROVIDER_URI"])

        with open(f"{TEST_DIR}/testdata/address.csv", "r") as fr:
            addresses = [e.strip() for e in fr.readlines()]
        assert len(addresses) == 2000

        for w, b in [(20, 100), (30, 100)]:
            e.get_balance(
                accounts=addresses,
                block_id=11953815,
                max_workers=w,
                batch_size=b,
            )
