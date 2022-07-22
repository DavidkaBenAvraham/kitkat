# -*- coding: utf-8 -*-
#!/usr/bin/env python
#@package katia.suppliers.grandadvance

import execute_json as json
from strings_formatter import StringFormatter as SF
from suppliers.product import Product 
from script_logger import logger

# Documentation for this module
def login(self):


    logger.info(f"Залогиниваюсь")
    email = self.locators['login']['email']
    password = self.locators['login']['password']

    open_login_dialog_locator = (self.locators['login']['open_login_dialog_locator']['by'],
                                  self.locators['login']['open_login_dialog_locator']['selector'])

    email_locator = (self.locators['login']['email_selector']['by'], 
                     self.locators['login']['email_selector']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                         self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                             self.locators['login']['loginbutton_locator']['selector'])


    elements = self.find(open_login_dialog_locator)
    ''' получаю див с кнопками Логин и Регистер
    мне нужна первая'''
    elements[0].click()


    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    self.wait(1)
    elements = self.find(loginbutton_locator)
    ''' получаю див с кнопками Отмена и Войти
    мне нужна вторая'''
    elements[1].click()
    logger.info('Гранд logged in')
    return True


