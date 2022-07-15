# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module
def log_in(self):
    self.print(f"Залогиниваюсь")
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
    self.log('Гранд logged in')
    return True


