# -*- coding: utf-8 -*-
from requests.exceptions import ConnectTimeout

from odoo import http
import requests
api_key = 'bf7f47035f7368c80c714e8a263691b1'

class Weather(http.Controller):
    @http.route('/weather/status', auth='public' , type='json')
    def index(self, **kw):
        if kw.get('place'):
            try:
                res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={kw.get('place')}&appid=bf7f47035f7368c80c714e8a263691b1&units=metric")
            except requests.exceptions.ConnectionError as E:
                return None
            except TimeoutError as E:
                return None
            except requests.exceptions.ReadTimeout as e:
                return None
            else:
                return res.json()
        else:
            try :
                res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={kw.get('lat')}&lon={kw.get('long')}&appid=bf7f47035f7368c80c714e8a263691b1&units=metric")
            except requests.exceptions.ConnectionError as E:
                return None
            except TimeoutError as E:
                return None
            except requests.exceptions.ReadTimeout as e:
                return None
            else:
                return res.json()
