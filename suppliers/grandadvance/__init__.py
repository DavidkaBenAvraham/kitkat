# -*- coding: utf-8 -*-
#!/usr/bin/env python
#@package katia.suppliers.grandadvance

import execute_json as json
from strings_formatter import StringFormatter as SF
from suppliers.product import Product 
from script_logger import logger

# Documentation for this module
def login(supplier):

    _s = supplier
    _l = supplier.locators['login']
    _d = supplier.driver

    _d.get_url(_s.settings['login_url'])
    logger.info(f"Залогиниваюсь")
    email = _l['email']
    password = _l['password']

    open_login_dialog_locator =_l['open_login_dialog_locator']
    email_locator = _l['email_selector']
    password_locator = _l['password_locator']
    loginbutton_locator =  _l['loginbutton_locator']


    elements = _d.find(open_login_dialog_locator)
    ''' получаю див с кнопками Логин и Регистер
    мне нужна первая'''
    elements[0].click()


    _d.find(email_locator).send_keys(email)
    _d.find(password_locator).send_keys(password)
    _d.wait(1)
    elements = _d.find(loginbutton_locator)
    ''' получаю див с кнопками Отмена и Войти
    мне нужна вторая'''
    elements[1].click()
    logger.info('Гранд logged in')
    return True


