from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("base.html")
@app.route('/datacleaning')
def datacleaning():
    return render_template("datacleaning.html")
@app.route('/chart-view')
def chartView():
    return render_template("chart-view.html")



if __name__ == '__main__':
    app.run()
