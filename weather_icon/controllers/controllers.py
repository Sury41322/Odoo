# -*- coding: utf-8 -*-
from odoo import http
import requests
api_key = 'bf7f47035f7368c80c714e8a263691b1'

class Weather(http.Controller):
    @http.route('/weather/status', auth='public' , type='json')
    def index(self, **kw):
        if kw.get('place'):
            res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={kw.get('place')}&appid=bf7f47035f7368c80c714e8a263691b1&units=metric")
        else:
            res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={kw.get('lat')}&lon={kw.get('long')}&appid=bf7f47035f7368c80c714e8a263691b1&units=metric")
        return res.json()
