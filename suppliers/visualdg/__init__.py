# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module
def log_in(self):
    self.get_url('https://www.visualdg.co.il/customer_login')
        
    email = self.locators['login']['email']
    password = self.locators['login']['password']

    email_locator = (self.locators['login']['email_locator']['by'], 
                        self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                            self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                self.locators['login']['loginbutton_locator']['selector'])



    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    self.wait(1)
    self.find(loginbutton_locator).click()
    self.wait(1)
    self.log('VDG logged in')
   
    return True


