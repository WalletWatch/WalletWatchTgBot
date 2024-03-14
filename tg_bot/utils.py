import requests

host = "3f9215732d0c.vps.myjino.ru"
# host = "127.0.0.1:8000"

def wallet_list():
    r = requests.get(f'http://{host}/api/wallet/')

    return r.json()['data']

def balance_list():
    r = requests.get(f'http://{host}/api/balance/')

    return r.json()['data']

def create_wallet(wallet):
    r = requests.post(f'http://{host}/api/wallet/', data=wallet)

    return r

def create_balance(balance):
    r = requests.post(f'http://{host}/api/balance/', data=balance)

    return r 

def delete_wallet(id):
    r = requests.delete(f'http://{host}/api/wallet/{id}/')

    return r.status_code

def delete_balance(id):
    r = requests.delete(f'http://{host}/api/balance/{id}/')

    return r.status_code

def wallet_detail(id):
    r = requests.get(f'http://{host}/api/wallet/' + str(id) +'/')

    return r.json()

def balance_detail(id):
    r = requests.get(f'http://{host}/api/balance/' + str(id) +'/')

    return r.json()

def network_list():
    r = requests.get(f'http://{host}/api/network/')

    return r.json()['data']
