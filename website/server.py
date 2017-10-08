from flask import Flask, render_template, request, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)

allprices = {}

def getPrices():
	global allprices
	requestaddress = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC&tsyms=USD'
	try: 
		response = requests.get(requestaddress)
		allprices['BTC'] = response.json()['BTC']['USD']
		print('gettingprices')
	except:
		print("I didn't recieve any information for this coin")

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(getPrices, 'interval', seconds=5)
atexit.register(lambda: scheduler.shutdown())
@app.route("/")
def mainpage():
    return render_template('index.html') 

@app.route("/fun")
def fun():
	return "Oh, so you want to have fun eh?"

@app.route("/prices", methods=['GET', 'POST'])
def prices(coinname='BTC'):
	global allprices
	if(request.method == 'POST'):
		requestInfo = request.form
		coins = requestInfo['coins']
	else:
		return jsonify(BTC=allprices[coinname])

@manager.command
def runserver():
	getPrices()
	app.run(debug=True, host='0.0.0.0', use_reloader=False)

if __name__ == "__main__":
	manager.run(runserver())
	

