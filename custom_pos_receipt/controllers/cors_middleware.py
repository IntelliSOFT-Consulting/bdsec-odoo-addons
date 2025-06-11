from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home

class HomeWithCORS(Home):
    def dispatch(self, *args, **kwargs):
        response = super(HomeWithCORS, self).dispatch(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
