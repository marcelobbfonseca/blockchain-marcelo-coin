import time
import hashlib


class Transaction:
    def __init__(self, sender_address, receiver_address, amount):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount


class Block:
    def __init__(self, transactions, previous_hash=''):

        # stores the hash of the previous block
        self.previous_hash = previous_hash

        # Stores data
        self.transactions = transactions

        # Incremented for mining blocks
        self.nonce = 0

        # Block creation date
        self.timestamp = time.time()

        # Calculates a new hash for the current block
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        # Concatenate all attributes to build the block's hash
        params = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)

        # All attributes are hashed in sha256 and
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
        self.chain = [Block([], 0)]  # "Genesis Block"

        # Set a difficulty limitation level for each hash.
        # The difficulty will set the number of 0's that must appear as begining character in a hash.
        # Ex: If dificulty=4, the first 4 characters of a hash must be 0's. "0000..."
        # Currently bitcoin difficulty is 18.
        self.dificulty = 3

        # Stores an array of transactions to add in the next block
        self.pending_transactions = []

        # miner reward for each block
        self.mining_reward = 100.00

    # Get the last block from blockchain
    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_transactions(self, miner_address):

        # Creates a new block and add's pending_transactions array to be mined and previous block hash
        block = Block(self.pending_transactions, self.get_latest_block().hash)

        # mine appropriate hash with the blockchain difficulty
        block.mine_block(self.dificulty)
        print("Block successfully mined!")

        # Add block to the blockchain
        self.chain.append(block)

        # Reset pending transactions and add transaction with miner reward to next transaction array
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]

    # Adds a new transaction to pending_transaction array
    def create_transactions(self, transaction):
        self.pending_transactions.append(transaction)

    # Print all block in the blockchain
    def show_chain(self):

        for block in self.chain:
            print("{")
            print("index: ", block.index)
            print("timestamp: ", block.timestamp)
            print("transactions: ", block.transactions)
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

    def get_balance_of_address(self, address):
        # Address balance are not stored in the blockchain so it was to be calculated.
        balance = 0

        # To access your amount you must go trough all transactions in the blockchain
        for block in self.chain:
            for transaction in block.transactions:

                if transaction.sender_address == address:
                    balance = balance - transaction.amount

                if transaction.receiver_address == address:
                    balance = balance + transaction.amount

        return balance


def main():

    print("Block Chain")
    # creates BlockChain
    marcelo_coin = BlockChain()

    # Creates transactions
    marcelo_coin.create_transactions(Transaction("marcelo_pub_key", "pedro_pub_key", 150))
    marcelo_coin.create_transactions(Transaction("matheus_pub_key", "fijo_pub_key", 24))

    # All transactions are stored in pending_transactions array
    # To process these transactions it's necessary to mine a block to process them

    # Starting the miner
    marcelo_coin.mine_pending_transactions("mendigo_pub_key")

    # Print fijo's balance
    amount = marcelo_coin.get_balance_of_address("fijo_pub_key")
    print("Fijo's balance: ", amount)

    # Print extisting blocks in BlockChain
    # marcelo_coin.show_chain()

    # Validates BlockChain, consists on checking the hash and previous hash on each block
    # print("is chain valid?", marcelo_coin.is_chain_valid())


if __name__ == "__main__":
    main()
