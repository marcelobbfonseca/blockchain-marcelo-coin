import time
import hashlib


class Block:
    def __init__(self, index, data, previous_hash=''):
        # Block id
        self.index = index

        # stores the hash of the previous block
        self.previous_hash = previous_hash

        # Stores data
        self.data = data

        # Incremented for mining blocks
        self.nonce = 0

        # Block creation date
        self.timestamp = time.time()

        # Calculates a new hash for the current block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        params = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return str(hashlib.sha256(params.encode("ascii")).hexdigest())

    #   print a blocks attributes
    def show_block(self):
        print("index: ", self.index)
        print("timestamp: ", self.timestamp)
        print("data: ", self.data)
        print("hash: ", self.hash)
        print("previous_hash", self.previous_hash)

    #   Generates hashes until a hash is found respecting the dificulty condition
    def mine_block(self, dificulty):
        print("mining...")

        # Condition: The first 'dificulty' digits must be 0's
        dificulty_digits = '0' * dificulty

        # keep looking while the generated hash is diferent from the dificulty condition
        while self.hash[0:dificulty] != dificulty_digits:

            # Variable nonce is increment for each attempt.
            # This way the next hash calculation is garanteed to not be the same.
            self.nonce = self.nonce + 1

            # After a fail generates a new hash and try again.
            self.hash = self.calculate_hash()

        # Return hash when condition is match.
        print("Found hash: ", self.hash)
        return self.hash

class BlockChain:
    def __init__(self):

        # Initialise the Genesis Block of our BlockChain
        # Genesis Block is the first Block and have no previous block
        # and doesn't have a previous hash.
        self.chain = [Block(0, "Genesis Block")]

        # Set a dificulty limitation level for each hash.
        # The dificulty will set the number of 0's that must appear as begining character in a hash.
        # Ex: If dificulty=4, the first 4 characters of a hash must be 0's. "0000..."
        # Currently bitcoin dificulty is 18.
        self.dificulty = 2

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block):
        # get and add previous block to current block
        new_block.previous_hash = self.get_latest_block().hash

        # discover a hash for this current block
        new_block.mine_block(self.dificulty)

        # Add the new block to the BlockChain
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
    # creates BlockChain
    marcelo_coin = BlockChain()

    # Creates new blocks
    b1 = Block(1, {"amount": 20, "Sender": "Marcelo", "Receiver": "Pedro"})
    b2 = Block(1, {"amount": 15, "Sender": "Matheus", "Receiver": "Filipe"})

    # Add created blocks to my BlockChain
    marcelo_coin.add_block(b1)
    marcelo_coin.add_block(b2)

    # Print extisting blocks in BlockChain
    # marcelo_coin.show_chain()

    # Validates BlockChain, consists on checking the hash and previous hash on each block
    # print("is chain valid?", marcelo_coin.is_chain_valid())


if __name__ == "__main__":
    main()
