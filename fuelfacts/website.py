from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from . import facts

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        liters = request.form['liters']
        distance = request.form['km-from-distrib-point']
        ratio = facts.transport_derived['truck']['mileage']['liter-per-thousand-liter-km']['value']
        extra_fuel = (int(liters) * int(distance) * ratio) / 1000
        msg = "Votre essence a nécessité %0.2f litres en plus pour arriver à votre réservoir" % extra_fuel
    else:
        msg = None

    return render_template('index.html', msg=msg)

