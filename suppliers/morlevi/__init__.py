# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module
from logger import Log

def log_in(self):
    if __login(self): return True
    else: 
        try:
            #'''
            #закрываю модальные окна сайта
            #выпадающие до входа
            #'''
            self.log( f''' Ошибка, пытаюсь закрыть popup''')
            self.page_refresh()
            if __login(self): return True


            close_popup_locator = (self.locators['login']['close_popup_locator']['by'], self.locators['login']['close_popup_locator']['selector'])

            close_popup_btn = self.find(close_popup_locator)
            self.wait(5)
            if str(type(close_popup_btn)).find("class 'list'") >-1:  # Если появилось несколько
                for b in close_popup_btn:
                    try:
                        b.click()
                        if __login(self) : 
                            
                            return True
                            break
                    except: pass
            if str(type(close_popup_btn)).find("webelement") >-1:  # нашелся только один элемент
                close_popup_btn.click()
                return __login(self)
        except Exception as ex:
            self.print(f''' 
            Не удалось залогиниться 
            {self.supplier}
            ''')
            return False
#@print_f
def __login(self):
    self.log( f''' Собссно, логин Морлеви''')
    self.driver.refresh()
    #self.driver.switch_to_active_element()
    email = self.locators['login']['email']
    password = self.locators['login']['password']

    open_login_dialog_locator = (self.locators['login']['open_login_dialog_locator']['by'],
                                self.locators['login']['open_login_dialog_locator']['selector'])

    email_locator = (self.locators['login']['email_locator']['by'], 
                    self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                        self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                            self.locators['login']['loginbutton_locator']['selector'])
    try:
        #self.log( f''' ищу open_login_dialog_locator {open_login_dialog_locator}''')
        self.find(open_login_dialog_locator).click()
        #self.log( f''' нашел ищу email_locator {email_locator}''')
        self.find(email_locator).send_keys(email)
        #self.log( f''' нашел ищу password_locator''')
        self.find(password_locator).send_keys(password)
        #self.log( f''' нашел делаю клик''')
        self.find(loginbutton_locator).click()
        self.log('Mor logged in')
        return True
    except Exception as ex:
        self.print(f'''Мор логин - ошибка:
        {ex}''')
        return False

