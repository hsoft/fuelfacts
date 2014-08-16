from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

from . import facts

app = Flask(__name__)
Bootstrap(app)
Markdown(app)

def consumption(method, lmkm):
    ratio = facts.freight[method]['liter-per-liter-km']
    return lmkm * ratio

def meansupplydist(region):
    supplies = facts.supply[region]
    totratio = sum(s['ratio'] for s in supplies)
    return sum(s['distance'] * (s['ratio'] / totratio) for s in supplies)

def fmtnumber(n):
    if n < 100:
        return '{:0.3f}'.format(n)
    else:
        return '{:,}'.format(int(n))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        liters = int(request.form['liters'])
        dist_refinery = int(request.form['km-from-distrib-point'])
        dist_supply = int(meansupplydist('quebec'))
        fuel1 = consumption('ship', liters * dist_supply)
        fuel2 = facts.refinery['gasoline']['liter-consumed-per-liter-produced'] * liters
        fuel3 = consumption('truck', liters * dist_refinery)
        consumption_data = [
            [
                "From the oil fields to the refinery",
                dist_supply,
                "Ship",
                '%0.2f' % fuel1,
                None,
            ],
            [
                "Refinery's energy consumption",
                "-",
                "-",
                '%0.2f' % fuel2,
                '/refining',
            ],
            [
                "From the refinery to the gas station",
                dist_refinery,
                "Truck",
                '%0.2f' % fuel3,
                None,
            ],
        ]
    else:
        consumption_data = None

    return render_template('index.html', consumption_data=consumption_data)

@app.route('/refining')
def refining():
    lines = facts.calculation['refinery-energy-consumption']
    lines = [(desc, link, fmtnumber(value)) for desc, link, value in lines]
    title = "Calculation details for refinery energy consumption"
    return render_template('calc_details.html', title=title, calculation_lines=lines)

@app.route('/about')
def about():
    return render_template('about.html')

