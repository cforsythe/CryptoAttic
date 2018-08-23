from flask import Flask, render_template, request, jsonify
import json
from celery import Celery
import celeryconfig

app = Flask(__name__)
app.config.from_object('config')


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['BROKER_URL'])
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)


@app.route("/")
def mainpage():
    return render_template('index.html')

@app.route("/fun")
def fun():
	return "Oh, so you want to have fun eh?"

##TODO the reading in this function needs to be setup to read from a database
@app.route("/prices", methods=['GET', 'POST'])
def prices(coinname='BTC'):
    with open('coin_data/coinprices.json') as f:
        all_prices = json.load(f)
    coinstosend = {}
    if(request.method == 'POST'):
        coinsneeded = json.loads(request.form['coins'])
        for coin in coinsneeded:
            coinstosend[coin] = all_prices[coin]
        return jsonify(coins=coinstosend)
    else:
        return jsonify(BTC=all_prices[coinname])


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', use_reloader=False, threaded=True)
