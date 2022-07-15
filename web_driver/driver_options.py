# -*- coding: utf-8 -*-
#!/usr/bin/env python
##
# @package Katia.Driver.driver_options
# 
#   ## Опции запуска ведрайвера(ов)
#   
#   - В разработке я использую FireFox 
#       Для работы в goggle research (collab.google) можно посмотреть на 
#       библиотеку kora, она вроде под него заточена
#
#   - в качестве вебдрайвера неплох seleniumwire
#
# Documentation for module driver_options
#   https://stackoverflow.com/questions/12211781/how-to-maximize-window-in-chrome-using-webdriver-python

from selenium.webdriver.firefox.options import Options

from loguru import logger
##@package Katia.Driver.Options
# doc for chrome_options()
def chrome_options(self):
    options = Options()
    
    options.add_argument("--start-maximized")
    return options


##@package Katia.Driver.Options
# doc for firefox_options()
def firefox_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options
##@package Katia.Driver.Options
# doc for opera_options()
def opera_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options
##@package Katia.Driver.Options
# doc for edge_options()
def edge_options(self):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")
    return options