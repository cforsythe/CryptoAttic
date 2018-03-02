import json
import grequests
import requests
def getCoins():
    coins = {}
    requestaddress = 'https://www.cryptocompare.com/api/data/coinlist/'
    try:
        response = requests.get(requestaddress)
        allcoins = response.json()['Data']
        for coin in allcoins:
            coin_abrv = allcoins[coin]['Name']
            coin_name = allcoins[coin]['CoinName']
            coins[coin_abrv] = coin_name
        print('Retrieved all coins')
        with open("coinnames.json", "w") as outfile:
            json.dump(coins, outfile)
    except:
        print("I didn't retrieve anything")

def generateCalls():
    urls = []
    iteration = 0
    api_call = 1
    coins_to_search = ""
    with open("coinnames.json", "r") as infile:
        coins = json.load(infile);
    for coin in coins:
        iteration += 1
        if(iteration > (60 * api_call)):
            urls.append(getUrl(coins_to_search))
            api_call += 1
            coins_to_search = ""
        if(iteration == len(coins)):
            coins_to_search += coin
            urls.append(getUrl(coins_to_search))
            break;
        coins_to_search += (coin + ',')
    with open("apicalls.json", "w") as outfile:
        json.dump(urls, outfile);

def getUrl(coins):
    return 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(coins) 

def getCoinInfo():
    all_prices = {}
    with open("apicalls.json", "r") as infile: 
        urls = json.load(infile)
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    for response in responses:
        response = response.json()
        for coin in response:
            all_prices[coin] = response[coin]["USD"]
    with open("coinprices.json", "w") as outfile:
        json.dump(all_prices, outfile)
def main():
    generateCalls()
    getCoinInfo()
main()
