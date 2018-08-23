import json
import grequests
import requests
import celery

APP_NAME = 'cryptoattic' 
FIATS = 'USD'
'''
Uses cryptocompare api to retrieve json of ALL coins 
Stores all coins in json as
coin_abbreviation : coin_name
'''

@celery.task
def get_coin_list():
    coins = {}
    request_address = 'https://min-api.cryptocompare.com/data/all/coinlist?extraParams={}'.format(APP_NAME)
    logger = get_coin_list.get_logger()
    try:
        response = requests.get(request_address)
        all_coins = response.json()['Data']
        for coin in all_coins:
            coin_abrv = all_coins[coin]['Name']
            coin_name = all_coins[coin]['CoinName']
            coins[coin_abrv] = coin_name
        if(len(all_coins) > 0):
            with open("coin_data/coinnames.json", "w") as outfile:
                json.dump(coins, outfile)
        logger.info("Retrieved coin list")

    except:
        logger.info("I didn't retrieve any coins")


@celery.task
def generate_calls():
    urls = []
    coins_to_search = ""
    with open("coin_data/coinnames.json", "r") as infile:
        coins = json.load(infile);
    for i, coin in enumerate(coins):
        last_added = False
        if((len(coins_to_search) + len(coin)) > 300):
            urls.append(gen_url(coins_to_search[:-1], FIATS))
            coins_to_search = ""
            if(i == len(coins) - 1): 
                coins_to_search += coin
                last_added = True
            else:
                coins_to_search += (coin + ",")
        if(i == (len(coins) - 1)):
            if(not last_added):
                coins_to_search += coin
            urls.append(gen_url(coins_to_search, FIATS))
        else:
            coins_to_search += (coin + ",")

    with open("coin_data/apicalls.json", "w") as outfile:
        json.dump(urls, outfile);

    logger = generate_calls.get_logger()
    logger.info("Generated api calls")

def gen_url(coins, fiats):
    return 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}&extraParams={}'.format(coins, fiats, APP_NAME) 


@celery.task
def get_coin_info():
    with open("coin_data/apicalls.json", "r") as infile: 
        urls = json.load(infile)
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    all_prices = {}
    for response in responses:
        response = response.json()
        if('Response' not in response):
            for coin, data in response.items():
                all_prices[coin] = data["USD"]
    with open("coin_data/coinprices.json", "w") as outfile:
        json.dump(all_prices, outfile)

    logger = get_coin_info.get_logger()
    logger.info("Retrieved coin prices")
    

