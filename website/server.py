from flask import Flask, render_template, request, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from flask_script import Manager
import json

app = Flask(__name__)
manager = Manager(app)

all_prices = {}
coins = {}

def coinCompile():
	global coins
	iteration = 0
	api_call = 1
	coins_to_search = ""
	for coin in coins:
		iteration += 1
		if(iteration > (60 * api_call)):
			getPrices(coins_to_search)
			api_call += 1
			coins_to_search = ""
		if(iteration == len(coins)):
			coins_to_search += coin
			getPrices(coins_to_search)
			break;
		coins_to_search += (coin + ',')
	print("I got all the coins")
def getPrices(coin_list):
	global all_prices
	requestaddress = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(coin_list)
	try: 
		response = requests.get(requestaddress)
		response = response.json()
		for coin in response:
			all_prices[coin] = response[coin]['USD']
		print("Getting the prices")
	except:
		print("I didn't recieve any information for this coin")

def getCoins():
	requestaddress = 'https://www.cryptocompare.com/api/data/coinlist/'
	try:
		response = requests.get(requestaddress)
		allcoins = response.json()['Data']
		for coin in allcoins:
			coin_abrv = allcoins[coin]['Name']
			coin_name = allcoins[coin]['CoinName']
			coins[coin_abrv] = coin_name
		print('Retrieved all coins')
	except:
		print("I didn't retrieve anything")

def scheduleProcess():
	scheduler = BackgroundScheduler()
	scheduler.start()
	scheduler.add_job(coinCompile, 'interval', seconds=10)
	atexit.register(lambda: scheduler.shutdown())
@app.route("/")
def mainpage():
    return render_template('index.html') 

@app.route("/fun")
def fun():
	return "Oh, so you want to have fun eh?"

@app.route("/prices", methods=['GET', 'POST'])
def prices(coinname='BTC'):
	global all_prices
	coinstosend = {}
	if(bool(all_prices) == False):
		return "I have no prices yet"
	if(request.method == 'POST'):
		coinsneeded = json.loads(request.form['coins'])
		for coin in coinsneeded:
			coinstosend[coin] = all_prices[coin]
		return jsonify(coins=coinstosend)
	else:
		return jsonify(BTC=all_prices[coinname])

@manager.command
def runserver():
	getCoins()
	scheduleProcess()
	app.run(debug=True, host='0.0.0.0', use_reloader=False)

if __name__ == "__main__":
	manager.run()
	

