from flask import Flask, render_template, send_file
from flask import jsonify
from database import init_data
from statistics import compute_means

app = Flask(__name__)
app.logger.setLevel("INFO")
df = init_data()[['date', 'close', 'volume', 'high', 'low', 'open', 'symbol']].dropna()

print(df)

from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("plot_market.html")


@app.route("/bitcoin")
def bitcoin():
    return render_template("bitcoin_value.html")


@app.route("/average")
def average():
    return render_template("average.html")


@app.route("/candlestick")
def candlestick():
    return render_template("candlestick.html")



@app.route("/data")
def get_data():
    # Sample stock market data
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': str(row['date'])[:10],
            'price': row['close'],
            'volume': row['volume'],
            'high': row['high'],
            'low': row['low'],
            'open': row['open'],
        })
    return jsonify(data)


@app.route('/templates/<filename>')
def templates(filename):
    return send_file('templates/' + filename)


@app.route('/lvmh')
def show_data():
    d = compute_means(df).fillna(0)[["close", "mean_30", "neg_30", "2_pos_30", "2_neg_30", "pos_30"]]
    d['time'] = [x for x in range(len(d))]
    payload = d.to_dict(orient='records')
    app.logger.info(payload)
    return jsonify(payload)


@app.route('/visu')
def visu():
    return render_template('visu.html')

@app.route('/graph.js')
def graph():
    return render_template('graph.js')


import requests


@app.route("/bitcoin/data")
def get_bitcoins():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    if response.status_code == 200:
        price = response.json()["bitcoin"]["usd"]
        return jsonify({"date": "now", "price": price})
    else:
        return jsonify({"error": "Failed to fetch data"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
