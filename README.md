# Multicall

fork from https://github.com/banteg/multicall.py, but implements the multicall in client's side.

## Install

```bash
pip install multicall-py
```

## Example

```python

from decimal import Decimal
from multicall import Multicall, Call

mc = Multicall("https://mainnet.infura.io/v3/xyz")

def from_wad(value):
    return Decimal(value) / 10 ** 18


def from_ray(value):
    return Decimal(value) / 10 ** 27


def from_rad(value):
    return Decimal(value) / 10 ** 45


def from_ilk(values):
    print(values)
    return {
        "Art": from_wad(values[0]),
        "rate": from_ray(values[1]),
        "spot": from_ray(values[2]),
        "line": from_rad(values[3]),
        "dust": from_rad(values[4]),
    }


result = mc.aggrate(
    [
        Call(
            target="0xdac17f958d2ee523a2206206994597c13d831ec7",
            function="balanceOf(address)(uint256)",
            args=("0xa929022c9107643515f5c777ce9a910f0d1e490c",),
            returns=[],
        ),
        Call(
            target="0xdac17f958d2ee523a2206206994597c13d831ec7",
            function="balanceOf(address)(uint256)",
            args=("0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",),
            request_id="0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",
        ),
        Call(
            "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b",
            "ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))",
            args=[b"ETH-A"],
            request_id="ETH-A",
            returns=[
                ["Art", from_wad],
                ["rate", from_ray],
                ["spot", from_ray],
                ["line", from_rad],
                ["dust", None],
            ],
        ),
    ]
)

print(result)
```

> response as below:

```python
[{'request_id': '5a7bd54c680592746135b37a6476eb6c',
  'result': 1701108488000000},
 {'request_id': '0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503',
  'result': 1350000115495224},
 {'request_id': 'ETH-A',
  'Art': Decimal('2789424592.115625600914086111'),
  'rate': Decimal('1.059237159709500809006237604'),
  'spot': Decimal('3001.379310344827586206896552'),
  'line': Decimal('3090847838.001970634131021155'),
  'dust': 10000000000000000000000000000000000000000000000000}]
```
