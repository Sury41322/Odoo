# -*- coding: utf-8 -*-
from . import controllers
from . import models


def post_install_hook(env):
    """function to set-up the payment provider"""
    env['payment.provider']._setup_provider('paytrail')

def uninstall_hook(env):
    """while uninstalling delete the record in account payment method"""
    installed_providers = env['payment.provider'].search([('code', '=', 'paytrail')])
    installed_providers.state = "disabled"
    installed_providers.write({'redirect_form_view_id': False})
    env['account.payment.method.line'].search([
        ('code', 'in', installed_providers.mapped('code')),
    ]).unlink()
