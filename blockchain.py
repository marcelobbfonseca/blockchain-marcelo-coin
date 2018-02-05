import time
import hashlib


class Block:
    def __init__(self, index, data, previous_hash=''):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0

        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        params = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return str(hashlib.sha256(params.encode("ascii")).hexdigest())

    def show_block(self):
        print("index: ", self.index)
        print("timestamp: ", self.timestamp)
        print("data: ", self.data)
        print("hash: ", self.hash)
        print("previous_hash", self.previous_hash)

    def mine_block(self, dificulty):
        print("mining...")
        dificulty_digits = '0' * dificulty
        while self.hash[0:dificulty] != dificulty_digits:
            self.nonce = self.nonce + 1
            self.hash = self.calculate_hash()

        print("Found hash: ", self.hash)
        return self.hash

class BlockChain:
    def __init__(self):
        self.chain = [Block(0, "Genesis Block")]
        self.dificulty = 2

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block):
        # get previous block and add it previous block hash on current block
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.dificulty)
        self.chain.append(new_block)

    def show_chain(self):

        for block in self.chain:
            print("{")
            print("index: ", block.index)
            print("timestamp: ", block.timestamp)
            print("data: ", block.data)
            print("hash: ", block.hash)
            print("previous_hash", block.previous_hash)
            print("}\n",)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            previous_block = self.chain[i-1]

            if block.previous_hash != previous_block.hash:
                return False

            if block.hash != block.calculate_hash():
                return False

        return True


def main():
    print("Block Chain")
    marcelo_coin = BlockChain()
    b1 = Block(1, {"amount": 20, "Sender": "Marcelo", "Receiver": "Pedro"})
    b2 = Block(1, {"amount": 15, "Sender": "Matheus", "Receiver": "Filipe"})
    marcelo_coin.add_block(b1)
    marcelo_coin.add_block(b2)
    # marcelo_coin.show_chain()
    # print("is chain valid?", marcelo_coin.is_chain_valid())


if __name__ == "__main__":
    main()
