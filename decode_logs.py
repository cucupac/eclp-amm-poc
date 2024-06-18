from eth_abi import abi
from eth_utils import decode_hex

# log_data = "0x0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000029881d0c1ebbdd0b2f000000000000000000000000000000000000000000000029881d0c1ebbdd0b2b00000000000000000000000000000000000000000000003ade7432a41d5c778800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000089d159fc1f1f611583dd000000000000000000000000000000000000000000009ebd2af4d46583f3b2d3"
# log_data = "0x00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000365c06ee96a6f826fa0000000000000000000000000000000000000000000000365c06ee96a6f826f600000000000000000000000000000000000000000000003633c4c37bd91fe2e0000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000efe93a10f3ad8846700000000000000000000000000000000000000000000000a63fa632758c93f7cb35"
log_data = "0x000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000002882ba36126496228400000000000000000000000000000000000000000000002882ba361264962280000000000000000000000000000000000000000000000036349efbc0fffc7933000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000930979644f3dbfa41ce0000000000000000000000000000000000000000000008e3a5ea48e28942a5fd5"

log_data_bytes = decode_hex(log_data[2:])

decodedABI = abi.decode(["uint256[]", "(uint256,uint256)", "uint256"], log_data_bytes)

balances, (invariant_x, invariant_y), amount = decodedABI

print("Balances:", balances)
print("Invariant:", {"x": invariant_x, "y": invariant_y})
print("Amount:", amount)
