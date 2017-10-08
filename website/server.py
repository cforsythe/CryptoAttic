from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template('index.html') 

@app.route("/fun")
def fun():
	return "Oh, so you want to have fun eh?"

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')