import hashlib
import datetime
import json


# 🔐 Hash Identity
def hash_identity(data):
    """
    Hash user identity securely using SHA-256
    """
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()


# 🧠 Generate Proof (ZKP Logic)
def generate_proof(age, kyc_verified):
    """
    Simulated Zero-Knowledge Proof logic
    """
    if age >= 18 and kyc_verified:
        return "VALID_USER"
    return "INVALID"


# ✅ Verify Proof
def verify_proof(proof):
    """
    Validate proof result
    """
    return proof == "VALID_USER"


# 🔗 Block Class
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.utcnow().isoformat()  # ✅ ISO format
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Generate SHA-256 hash of full block contents
        """
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": json.loads(json.dumps(self.data)),  # ✅ safe copy
            "previous_hash": self.previous_hash
        }

        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


# ⛓️ Blockchain Class
class Blockchain:
    """
    Simple blockchain implementation with genesis block
    """

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        Create the first block (Genesis Block)
        """
        return Block(0, {"info": "Genesis Block"}, "0")  # ✅ consistent format

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        """
        Add a new block to the blockchain
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


# 🛡️ Tampering Detection
def is_chain_valid(chain):
    """
    Verify blockchain integrity
    """
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        # Check hash integrity
        if current.hash != current.calculate_hash():
            return False

        # Check linkage
        if current.previous_hash != previous.hash:
            return False

    return True


# 🧪 TESTING (optional)
if __name__ == "__main__":
    my_blockchain = Blockchain()

    user1 = {"user": "Priscilla", "age": 22}
    hashed_user1 = hash_identity(user1)
    proof1 = generate_proof(user1["age"], True)
    my_blockchain.add_block(Block(1, {"hash": hashed_user1, "proof": proof1}, ""))

    user2 = {"user": "John", "age": 16}
    hashed_user2 = hash_identity(user2)
    proof2 = generate_proof(user2["age"], False)
    my_blockchain.add_block(Block(2, {"hash": hashed_user2, "proof": proof2}, ""))

    print("\nBlockchain Data:")
    for block in my_blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print("-" * 30)

    print("\nVerification Results:")
    for block in my_blockchain.chain[1:]:
        result = verify_proof(block.data["proof"])
        print(f"Block {block.index}: {result}")

    print("\nBlockchain Valid:", is_chain_valid(my_blockchain.chain))