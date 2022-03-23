import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, render_template
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
VERSA_COMP = os.getenv('VERSA_COMP')
VERSA_EVO = os.getenv('VERSA_EVO')

def get_stock_values(bike) -> dict:
    res = requests.get(bike)
    soup = BeautifulSoup(res.content, 'html.parser')

    stock_rows = soup.findAll('td', class_='hidden-xs')
    stock_obj = {
        0 : {'size':'49', 'qtd': None },
        1: {'size':'52', 'qtd': None},
        2: {'size':'55', 'qtd': None},
        3: {'size':'58', 'qtd': None}
    }

    for index, item in enumerate(stock_rows):
        in_stock = item.find('span', class_='td_stock in-stock')

        if in_stock:
            amount = int(in_stock.find('span').contents[0])
            stock_obj[index]['qtd'] = amount
    return stock_obj.values()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
    )

    @app.route('/')
    def comp() -> dict:
        data = get_stock_values(VERSA_COMP)
        return render_template('comp.html', data=data, url=VERSA_COMP)

    @app.route('/evo')
    def evo() -> dict:
        data = get_stock_values(VERSA_EVO)
        return render_template('evo.html', data=data, url=VERSA_EVO)

    return app
