from pqc.keygen import generate_keypair

seed = bytes.fromhex("e8ba10dd213a4b681257d0c716bca7b2718f4bd3c2e697326a5fb0e277fbf15d")

pub1, priv1 = generate_keypair(seed)
pub2, priv2 = generate_keypair(seed)

print("Public keys identical:", pub1 == pub2)
print("Private keys identical:", priv1 == priv2)