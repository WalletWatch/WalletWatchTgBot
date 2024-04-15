import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="tg_bot", host="psql", user="postgres", password="2608", port="5432")
        self.cursor = self.conn.cursor()
    
    def initaialTables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS networks( \
            id SERIAL PRIMARY KEY, \
            network TEXT, \
            network_url TEXT, \
            network_abi TEXT, \
            network_chain TEXT \
        )")

        self.cursor.execute('''INSERT INTO networks(network, network_url,network_abi, network_chain) \
            VALUES ('ERC20', 'https://mainnet.infura.io/v3/3c7ba8ecf29b439ab0cb11ddc4b70989','[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]', 'eth'), \
            ('BEP20', 'https://bsc-dataseed.binance.org/','[{\"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_sender","type":"address"},{"indexed":true,"internalType":"bytes32","name":"_to","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"to","type":"bytes32"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]', 'bsc')''')

        self.cursor.execute("CREATE TABLE IF NOT EXISTS  wallets( \
	            id SERIAL PRIMARY KEY, \
                name TEXT, \
                adress TEXT, \
                sum REAL, \
                user_id INT \
            );")
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tokens( \
                            id SERIAL PRIMARY KEY, \
                            asset TEXT, \
                            address TEXT, \
                            balance REAL, \
                            price REAL, \
                            value REAL, \
                            track BOOl, \
                            delta REAL, \
                            network_id INT, \
                            user_id INT, \
                            wallet_id INT \
                        )")

    def add_balance(self, asset, address, balance, price, user_id, network_id, wallet_id):
        value = balance * price
        self.cursor.execute(f"INSERT INTO tokens ( \
                asset, \
                address, \
                balance, \
                price, \
                value, \
                track, \
                delta, \
                network_id, \
                user_id, \
                wallet_id \
            ) \
            VALUES ('{asset}', '{address}', {balance}, {price}, {value}, {True}, {0.01}, {network_id}, {user_id}, {wallet_id}) RETURNING id")        
        self.conn.commit()

    def add_wallet(self, user_id, wallet_name, wallet_adress):
        self.cursor.execute(f"INSERT INTO wallets (user_id, name, adress, sum) \
                            VALUES ({user_id}, '{wallet_name}', '{wallet_adress}', {0}) RETURNING id")
        
        wallet_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return wallet_id

    def check_wallet(self, wallet_address, user_id):
        self.cursor.execute(f"SELECT * FROM wallets WHERE adress = '{wallet_address}' AND user_id = {user_id}")
        if len(self.cursor.fetchall()) == 0:
            return True
        else: return False

    def get_networks(self):
        self.cursor.execute("SELECT * FROM networks")
        return self.cursor.fetchall()
    
    def get_network(self, network_id):
        self.cursor.execute(f"SELECT * FROM networks WHERE id = {network_id}")
        return self.cursor.fetchall()[0]

    def get_user_wallets(self, user):
        self.cursor.execute(f"SELECT * FROM wallets WHERE user_id = {user}")
        return self.cursor.fetchall()
    
    def get_wallet(self, id):
        self.cursor.execute(f"SELECT * FROM wallets WHERE id = {id}")
        return self.cursor.fetchall()[0]
    
    def get_all_balances(self):
        self.cursor.execute(f"SELECT * FROM tokens")
        return self.cursor.fetchall()
    
    def get_all_wallets(self):
        self.cursor.execute(f"SELECT * FROM wallets")
        return self.cursor.fetchall()

    def get_wallet_balances(self, wallet_id):
        self.cursor.execute(f"SELECT * FROM tokens WHERE wallet_id = {wallet_id}")
        return self.cursor.fetchall()
    
    def get_balance(self, id):
        self.cursor.execute(f"SELECT * FROM tokens WHERE id = {id}")
        return self.cursor.fetchall()[0]
    
    def get_sum_wallet(self, wallet_id):
        self.cursor.execute(f"SELECT sum FROM wallets WHERE  id = {wallet_id}")
    
    def update_last_known_sum(self, wallet_id):
        self.cursor.execute(f"SELECT sum(value) as sum_wallet FROM tokens WHERE wallet_id = {wallet_id} ")
        new_sum = self.cursor.fetchone()
        self.cursor.execute(f"UPDATE wallets SET sum = {new_sum[0]} WHERE id = {wallet_id}")
        self.conn.commit()

        return new_sum[0]

    def update_last_known_balance(self, token_id, new_balance, new_price):
        value = new_balance * new_price
        self.cursor.execute(f"UPDATE tokens SET balance = {new_balance}, price = {new_price}, value = {value} WHERE id = {token_id}")
        self.conn.commit()
        self.cursor.execute(f"SELECT * FROM tokens WHERE id = {token_id}")
        return self.cursor.fetchone()

    def update_track_balance(self, token_id, track):
        self.cursor.execute(f"UPDATE tokens SET track = {track} WHERE id = {token_id}")
        self.conn.commit()

    def update_delta_balance(self, token_id, delta):
        self.cursor.execute(f"UPDATE tokens SET track = {delta} WHERE id = {token_id}")
        self.conn.commit()

    def delete_wallet(self, user_id, wallet_id):
        self.cursor.execute(f"DELETE FROM wallets WHERE id = {wallet_id} AND user_id = {user_id}")
        self.cursor.execute(f"DELETE FROM tokens WHERE wallet_id = {wallet_id} AND user_id = {user_id}")
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
