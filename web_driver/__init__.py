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
#   --  https://github.com/DavidkaBenAvraham/selenium-wire
#
#   - как работает driver_options
#   --  https://stackoverflow.com/questions/12211781/how-to-maximize-window-in-chrome-using-webdriver-python
#   
#   - как работает библиотека ast
#   -- #https://www.techiedelight.com/ru/parse-string-to-float-or-int-python/
#
#
# инерфейс самый простой - произвести команды поймав 
# локатором элемент
# 
##<h5>Типы поддерживаемых вебдрайверов (не все!) </h5>
#<ul>
#<li>        webdriver.Firefox</li>
#<li>        webdriver.Chrome</li>
#<li>        webdriver.Ie</li>
#<li>        webdriver.Opera</li>
#<li>        webdriver.PhantomJS</li>
#<li>        webdriver.Remote</li>
#</ul>
#<h5> Умеет в </h5>
#<ul>
#<li>        webdriver.DesiredCapabilities</li>
#<li>        webdriver.ActionChains</li>
#<li>        webdriver.TouchActions</li>
#<li>        webdriver.Proxy</li>
#<li>        https://selenium-python.readthedocs.io/api.html#desired-capabilities</li>
#</ul>

from cmath import log
from pathlib import Path
#from base64 import b64decode
import urllib
#import requests
#import codecs
from loguru import logger

import selenium


from strings_formatter import StringFormatter as SF


##############################################################
#
#           все перенесено в логику set_driver()
#
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
## from https://ru.stackoverflow.com/questions/1340290/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%BA%D0%BB%D0%B8%D0%BA-%D0%BF%D0%BE-%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D1%83-%D0%B2-selenium-python
#############################################################



import pickle


###############################################################
#
#               Подключение вебдрайвера
#                  WD = KWD | SWD | SWWD
#import kora
#from kora.selenium import wd as KWD
import seleniumwire
from selenium import webdriver as SWD
from seleniumwire import webdriver as SWWD
WD = SWWD


#import html5lib
#from urllib.request import urlopen

#import xml.etree.ElementTree as ET
#from lxml import etree 
#from xml.etree import ElementTree as ET


import ast


import os
import pandas as pd
import datetime
import time
from attr import attrs, attrib, Factory

from ini_files_dir import Ini as ini
import execute_json as json


@attrs
## класс <b>Driver()</b> 
# реализует функции selenium 
# в обертке 
# <a href="https://github.com/DavidkaBenAvraham/selenium-wire" target="_blank"
# style = "COLOR:#550000;FONT-SIZE:LARGE;FONT-DECORATION:BOLD" > 
# seleniumwire 
# </a>
# driver устанавливается из настроек в файле launcher.json, узел ['webdriver']
    # <h5>Например</h5>
    # <pre>
    #  "webdriver": {
    #    "name": "firefox",
    #    "arguments": [ "--no-sandbox", "--disable-dev-shm-usage" ],
    #    "disabled_arguments": [
    #      "--disable-dev-shm-usage",
    #      "--headless"
    #    ],
    #    "deafault_wait_time": 5,
    #    "maximize_window": true,
    #    "view_html_source_mode": false
    #}
    # </pre>
#<ul>
#<li>current_url : текущий url. Нужен мне для отслеживания переключений драйвера</li>
#<li>previous_url : прошлый url. Нужен мне для отслеживания переключений драйвера</li>
#<li>driver : webdriver </li>
#<li>get_parsed_google_search_result : время запуска скрипта</li>
#</ul>
class Driver:
   
    ### JS: Всякие javascrits полезности
    def unhide(driver,element) -> bool:
        script :str = f''' arguments[0].style.opacity=1;
                        arguments[0].style['transform']='translate(0px, 0px) scale(1)';
                        arguments[0].style['MozTransform']='translate(0px, 0px) scale(1)';
                        arguments[0].style['WebkitTransform']='translate(0px, 0px) scale(1)';
                        arguments[0].style['msTransform']='translate(0px, 0px) scale(1)';
                        arguments[0].style['OTransform']='translate(0px, 0px) scale(1)';
                        arguments[0].scrollIntoView(true);
                        return true; '''
        try:
            driver.execute_script(script, element)
            return True
        except Exception as ex:
            logger.error(f'''
           ошибка в driver.execute_script(script)
           script = {script}
           ------------------
           {ex}
            ''')
            return False
        return True
        
    def get_ready_state(self) -> str:
        ''' пока идет загрузка DOM дерева возвращает "loading", 
            а когда загрузился - "complete"             '''
        script = 'return document.readyState'
        try:
            return self.driver.execute_script(script)
        except Exception as ex:
            logger.error(f'''
           ошибка в driver.execute_script(script)
           script = {script}
           ----------------
           {ex}
            ''')
            return None


    ## текущий url. Нужен мне для отслеживания переключений драйвера
    current_url : str = attrib(init = False , default = None)

    ## прошлый url. Нужен мне для отслеживания переключений драйвера
    previous_url : str = attrib(init = False , default = None)
    

    #from web_drive.google_search import GoogleHtmlParser as GoogleHtmlParser

    #parsed_google_search_result : GoogleHtmlParser = attrib(init = False, default = GoogleHtmlParser)

    drivername : str = attrib(init = False , default = 'firefox')
    

    driver : WD =  attrib(init = False , default = WD)

    ################################################################
    #
    #       заголовки 
    #   https://stackoverflow.com/questions/15645093/setting-request-headers-in-selenium
    #
    ################################################################
    headers : dict = attrib(init = False , default = None)
    


    cookies = attrib(init = False , default = None)
    cookies_file_path : Path = attrib(init = False , default = Path('cookies.pkl'))
    
    
    ##############################################################
    #
    #        драйвер запускается через вызов set_driver(webdriver_settings)
    #           при инициализации класса s = Supplier()
    #
    #############################################################
    def __attrs_post_init__(self ,  *args, **kwrads):

        pass
    





    ## set_driver(webdriver_settings)
    # <pre>
    # webdriver_settings from launcher.json: 
    # --------------------------
    # f.e. FirefoxDriver
    #"firefox": {
    #     "arguments": [ "--no-sandbox" ],
    #     "disabled_arguments": [
    #       "--disable-dev-shm-usage",
    #       "--headless"
    #     ],
    #     "deafault_wait_time": 5,
    #     "about wait": "явное ожидание браузера в сек",
    #     "random": [ 0, 5 ],
    #     "view_html_source_mode": false,
    #     "maximize_window": true
    #   }
    # }
    # </pre>
    def set_driver(self , ini) -> WD:  

        ## set_chrome
        def set_chrome() -> bool:
            _settings = ini.launcher['webdriver']['chrome']
            options = self.driver.ChromeOptions()
            for argument in _settings['arguments']:
                    options.add_argument(argument)
            self.driver = self.driver.Chrome(options = options)
            return True

        ## set_firefox
        def set_firefox() -> bool:
            _settings = ini.launcher['webdriver']['chrome']
            options = self.driver.FirefoxOptions()
            for argument in _settings['arguments']:
                    options.add_argument(argument)
            self.driver = self.driver.Firefox(options = options)
            return True
         
        ## set_kora
        def set_kora() -> bool:
            _wd = kora.selenium.wd
            if not kora.IN_COLAB: 
                logger.debug(f''' Hello local from kora :) ''')
                set_chrome()
                
            else:
                set_chrome()
                logger.debug(f''' Hello colab  from kora :)''')
                #options = _wd.ChromeOptions()
                #for argument in webdriver_settings['kora']:
                #        options.add_argument(argument)
                #self.driver = _wd.Chrome(options = options)

            return True

        # Create a request interceptor
        def interceptor(request):
            ''' подставлаю headers '''
            self.headers = dict(ini.launcher['webdriver']['headers'])
            for k in self.headers:
                del request.headers[k]  # Delete the header first
                request.headers[k] = self.headers[k]

        


        set_firefox()
        #set_chrome()
        self.driver.maximize_window()
        # Set the interceptor on the driver
        #https://stackoverflow.com/questions/15645093/setting-request-headers-in-selenium
        self.driver.request_interceptor = interceptor


        self.driver.wait =                              self._wait
        self.driver.get_url =                           self._get_url
        self.driver.find =                              self._find
        self.driver.find_attributes_in_webelements =    self._find_attributes_in_webelements
        self.driver.parce_html_block =                  self._parce_html_block
        self.driver.click =                             self._click
        self.driver.page_refresh =                      self._page_refresh
        self.driver.close =                             self._close  
        self.driver.scroll =                            self._scroller
        self.driver.previous_url :str =                 self.previous_url
        self.driver.save_images  =                       self._save_images
        #self.driver.get_parsed_google_search_result =   GoogleHtmlParser
        self.driver.send_keys =                         self._send_keys
        
        
        self.driver.cookies =                           self.cookies
        self.driver.cookies_file_path :Path =           self.cookies_file_path
        self.driver.dump_cookies_to_file =              self._dump_cookies_to_file
        self.driver.load_cookies_from_file =            self._load_cookies_from_file


        self.driver.WebKitGTK =                         SWD.WebKitGTK
        self.driver.WebKitGTKOptions =                  SWD.WebKitGTKOptions
        self.driver.WPEWebKit =                         SWD.WPEWebKit
        self.driver.WPEWebKitOptions =                  SWD.WPEWebKitOptions
        

        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.WebDriverWait = WebDriverWait

        from selenium.webdriver.support import expected_conditions as EC
        self.driver.EC = EC

        from selenium.webdriver.common.by import By
        self.driver.By = By

        from selenium.webdriver.common.keys import Keys
        self.driver.Keys = Keys

        from selenium.webdriver.common.action_chains import ActionChains
        self.driver.ActionChains = ActionChains
        self.ini = ini
        return self.driver









    #########################################################
    #                                                       #
    #                                                       #
    #                       Ожидания                        #
    #                                                       #
    #                                                       #
    #########################################################

    ### _wait
    ## Явное ожидание через time.sleep
    def _wait(self , wait  = 0):
        if wait == 0 : wait = self._deafault_wait_time
        time.sleep(wait)
        pass


    ### _wait_to_precence_located 
    # ожидание 100% загрузки элемента
    def _wait_to_precence_located(self, locator : dict ) -> object :
        '''
        ожидание 100% загрузки элемента
        locator=(By.CSS_SELECTOR , selector)
        '''
        self.wait = 100
        _d = self.driver
        webelement =  _d.WebDriverWait(_d , self.wait).until(_d.EC.presence_of_element_located(locator))
        return webelement
    ## _wait_to_be_clickable 
    # ожидание кликабельности элемента
    def _wait_to_be_clickable(self, wait : int = 0 , locator : dict = {}) :
        '''
        ождание кликабельности элемента '''
        element_clickable = EC.element_to_be_clickable(locator)
        webelement =  WebDriverWait(self.driver , wait).until(element_clickable)
        return webelement
    















    #########################################################
    #                                                       #
    #                                                       #
    #                       Куки                            #
    #                                                       #
    #                                                       #
    #########################################################

    def _load_cookies_from_file(self, cookies_file_path : Path = None ) -> bool:
        cookies_file_path = self.cookies_file_path if cookies_file_path is None else cookies_file_path
        
        logger.debug(''' cookies_file_path
        ---------------------------
        cookies_file_path} ''')

        if not cookies_file_path.exists():
                return False , logger.error(f''' {cookies_file_path} не найден ''')
        
        self.cookies = pickle.load(open(cookies_file_path , 'rb'))
        for cookie in self.cookies:
                self.driver.add_cookie(cookie)  
                logger.debug(f''' скушал печеньки ''')
                return True


    ## После успешного события ведрайвера я бережно сохраню печеньку  в файл 
    #   @param
    # -------------
    #   cookies_file : Path('cookies.pkl')
    def _dump_cookies_to_file(self, cookies_file_path : Path = None):
        cookies_file_path = self.cookies_file_path if cookies_file_path is None else cookies_file_path
        _cookies = self.driver.get_cookies()
        for cookie in _cookies:
            if cookie.get('expiry', None) is not None:
                cookie['expires'] = cookie.pop('expiry')
        pickle.dump(_cookies, open(cookies_file_path, 'wb'))
        logger.debug(''' сохранил печеньку 
        {_cookies}
        ---------------------------
        в файл:
        {cookies_file_path} ''')





















####################   driver.get() ###########################



























    ## обертка для driver.get():
    # переход по указанному url
    # @param
    #   url:str 
    # @param
    #   view_html_source_mode : bool     возвращает код страницы
    def _get_url(self, url:str , 
                 wait_to_locator_be_loaded : dict = {} , 
                 retrieveies = 3, 
                 view_html_source_mode : bool = False
                 ):
        logger.debug(f''' url : {url}''')
        
        _d = self.driver
        json_files : str = ''
        _url = _d.current_url

        flag = False
        try:
            _d.get(f'''{url}''')
            flag = True

        except Exception as ex:
            return False , logger.error(f''' Ошибка в _get_url() :
            {ex}
            -------------------------------------
             url = {url}''')  

        #logger.debug(f''' Requests:
        #''')
        #for request in _d.requests:
        #    logger.debug(request)


        #logger.debug(f''' PERFOMANCE :
        #{_d.get_log(f'''performance''')}
        #-------------------------------------''')  

        ''' ожидание полной загрузки 
        страницы с проверкой JS document.readyState'''
        count = 1
        while self.get_ready_state() != 'complete':
            logger.debug(f''' {self.get_ready_state()} - {_d.current_url}''')
            self._wait(1)
            count +=1
            if count>3:break


        ## Здесь нерешенная проблема с coockies
        #if self.cookies is None : set_cookies()
        #_set_cookies()


        # запоминаю, где был
        _d.previous_url = _url if _d.previous_url != _url else _d.previous_url

        # запоминаю рабочее окно 
        try:
            main_window_handler = _d.current_window_handle
        # перезапускаю
        except Exception as ex:
            logger.error(f''' 
            потеряно окно!!!
            -------------------------------
                Следующая попытка через 15с
            -------------------------------
            ''')
            self._wait(15)
            if retrieveies > 0:
                retrieveies-=1

                self._get_url(url, 
                 wait_to_locator_be_loaded , 
                 retrieveies, 
                 view_html_source_mode
                 )
        return True







        #####################################################
        # 
        #                       experimental:
        #<pre>
        #try:
        #    # Access requests via the `requests` attribute
        #    for request in _d.requests:
        #        if request.response:
        #            if str(request.response.headers['Content-Type']) == 'application/json':
        #                json_files += f'''
        #                    {str(request.url)}
        #                    {str(request.response.status_code)}
        #                    {str(request.response.headers['Content-Type'])}
        #                    '''
        #except:pass
        #finally:return  json_files
        #</pre>
        ################################################


    def _save_images(self, src)->bool:
        def _w(img:dict)->bool:
            for i in img:
                file_path = Path(self.ini.paths.export_dir , i.split('/')[-1])
            
                # https://stackoverflow.com/questions/17361742/download-image-with-selenium-python
                # элегантно. По сути я храню скриншот элемента
                with open(file_path , 'wb') as file:
                    file.write(img[i].screenshot_as_png)


        if isinstance(src , list):
            for s in src:
                if isinstance(s , dict):_w(s)
        elif isinstance(src , dict):_w(src)


        elif src is not None:_w(src)

        else: logger.error(''' упс, а баннеров нет ''')
            






    ## scroller
    def _scroller(self, wait : int = 0 , prokrutok : int = 5, scroll_frame : int = 1800) -> bool:
        ''' скроллинг вниз '''
        for i in range(prokrutok):
            self.driver.execute_script(f'''window.scrollBy(0,{scroll_frame})''') 
            self._wait(0.6)
        ''' и вверх '''
        for i in range(prokrutok):
            self.driver.execute_script(f'''window.scrollBy(0,-{scroll_frame})''') 
            self._wait(0.6)
        
        return True
        #except Exception as ex: return  False , logger.error(f''' ошибка скроллинга {ex}''')
   

    ## parce_html_block
    def _parce_html_block(self , html_block , locator):
        _elements = html_block.find_elements(locator['by'] , locator['selector'])
        return self._find_attributes_in_webelements(_elements , locator)


    ## find_attributes_in_webelements
    def _find_attributes_in_webelements(self , elements , locator) -> list: 
        '''аттрибуты в locator['attribute'] 
        могут быть None, строкой,  словарем или списком 
         если аттрибут None - эта функция не должна вызываться,
         а вебэлемент отдается целиком '''


        _е : list = [] 
        _ = locator['attribute']

        # 1) если АТТРИБУТЫ в словаре {'href':'text'}
        if isinstance(_  , dict):
            if isinstance(elements , list):
                ''' ЭЛЕМЕНТЫ списком '''
                for el in elements: 
                    ''' если attr is None я получу весь элемент '''
                    for i in _.items():
                        if i[0] is None: 
                            k = el
                        else:
                            k = el.get_attribute(i[0])
                        if i[1] is None:
                            v = el
                        else:
                            v = el.get_attribute(i[1])
                        _е.append({k:v})
            else:                     
                for k,v in _.popitem():
                    _е.append({elements.get_attribute(k):elements.get_attribute(v)})


        #2) АТТРИБУТЫ списоком ['href','text']
        elif isinstance(_  , list):
            if isinstance(elements , list):
                ''' ЭЛЕМЕНТЫ списком '''
                for el in elements:
                    for attr in _:
                        ''' если attr is None я получу весь элемент
                        '''
                        if attr is None:_е.append(el) 
                        else: _е.append(el.get_attribute(attr))
            else: 
                for attr in _:
                    ''' если attr is None я получу весь элемент
                    '''
                    if attr is None:_е.append(el) 
                    else: _е.append(elements.get_attribute(attr))


        #3) если один 
        # Самый часто используемый аттрибут
        # он получает единственный аттрибут элемента/ов
        #f.e. 'innerHTML'
        else:
            if isinstance(elements , list):
                ''' элементы списком '''
                for el in elements:
                    _е.append(el.get_attribute(_))
            else: _е.append(elements.get_attribute(_))
               

        if len(_е) == 0:return None
        elif len(_е) == 1:return _е[0]
        else: return _е

    
    ## FIND
    def _find(self, locator:dict) :
        ''' поиск элементов на странице 
        и поиск аттрибута по локатору (если он нужен)
         есть секрет в аттрибуте локатора
         если он пустой возвращается ВЕСЬ! элемент
        ----------------------------------------
        types of locator['attribute']:  str, None , [] , {}


        search for elements on the page and search for an attribute in the locator (if needed) 
        there is a secret: if the locator attribute if it is None (null in JSON), 
        ALL  element is be  returned! 
        ----------------------------------------
        types of locator['attribute']:  str, None , [] , {}
        '''

        # 0)
        '''
        в случае, когда элемент мне не нужен, но требуется по структуре
        построения сценария я заполняю локатор элемента значениями null
        '''
        if not 'attribute' in locator.keys(): locator['attribute'] = None
        if locator['attribute'] == 'current_url': return self.current_url
        #if locator['by'] is None: return None




        ## 1) выуживаю элементы со страницы. 
        elements = self._get_webelments_from_page(locator)
        ## всегда получаю [] , но все равно проверяю 
        if isinstance(elements , list):
            if len(elements) == 1: 
                elements = elements[0]
                ''' все таки я решил единственный найденный элемент не передавать списком '''
            elif len(elements) == 0:  
                elements = None
                return None
                ''' пустой список - вебдрайвер  не нашел элемент
                Нет смысла продолжать функцию '''
            else: pass # все норм. Пришел список
           
        

        ## 2) Если локатор locator['attribute'] не установлен в None 
        # то я возвращаю аттрибуты полученные по этому локатору
        # иначе - возвращаю весь найденный webelement
        # херовенько возвращать разные типы данных из функции, но мне так удобно
        return elements if  locator['attribute'] is None else self._find_attributes_in_webelements(elements , locator)

    ### get_webelments_from_page
    #   возвращает найденные на странице элементы в списке элементы
    #    если элементы  не найдны -возвращает пустой список []
    def _get_webelments_from_page(self, locator) -> list:

        try: 
            elements = self.driver.find_elements(locator['by'] , locator['selector'])
            return elements 
        except Exception as ex: return None , logger.error(f'''
        _get_webelments_from_page() 
        locator['by'] , locator['selector']  {locator['by']} , {locator['selector']}
        ошибка: 
        ex: {ex} ''')
        
    ## CLICK
    ##  Обработчик события click()
    ## ОЧЕНЬ - ОЧЕНЬ ПЛОХО РЕАЛИЗОВАН!!!
    def _click(self, locator) ->bool:
        
        _url_before_click = self.current_url
        ''' Запоминаю url ДО клика '''

        def err_handler():
            pass

        def najimalka(e)->bool:
            try: 
                e.click()
                return True
            except Exception as ex: logger.error(f''' 
            Возникла ошибка  {ex} 
            ----------------------
            элемент:
            {e} ne обязательно должен нажиматься
            он часть списка 
            {_el}
            ''')
            return False

        if isinstance(locator['selector'] , list):
            ''' в локаторе может быть запрос на несколько нажатий 
            '''

            for i in range(len(locator['selector'])):

                # создаю подлокатор
                _ = {      
                    "attribute": None,
                    "by": "xpath",
                    "selector": locator['selector'][i]
                    }
                _el = self._find(_)
                ## Я могу получить несколько элементов
                # так устроена система: я жадно собираю со страницы 
                # ВСЕ элементы по локатору
                if isinstance(_el , list): 
                    ''' список '''
                    for e in _el:
                        if not najimalka(e):continue
                        ### убрал в функцию
                        #
                        #try: e.click()
                        #except Exception as ex: logger.error(f''' 
                        #Возникла ошибка  {ex} 
                        #----------------------
                        #элемент:
                        #{e} ne обязательно должен нажиматься
                        #он часть списка 
                        #{_el}
                        #''')
                        #continue
                else: 
                    ''' не список '''
                    _results : Factory(list) = []
                    if not najimalka(_el):
                        try:self._send_keys( _ , self.driver.Keys.RETURN)
                        except Exception as ex: return False, logger.error(f'''   ХУЙ! ''')


                    #try: 
                    #    _el.click()
                    #except Exception as ex: 
                    #    logger.error(f''' 
                    #        Возникла ошибка  {ex} 
                    #        ----------------------
                    #        элемент:
                    #        {_el} не нажался
                    #        --------
                    #        я попробую достучаться до него посылая Key.Return
                    #        ''')
                        #try:self._send_keys( _ , self.driver.Keys.RETURN)
                        #except Exception as ex: return False, logger.error(f'''   ХУЙ! ''')

                    _results.append(True)
                #except Exception as ex: 
                #            logger.error(f''' 
                #                Возникла ошибка  {ex} 
                #                ----------------------
                #                элемент:
                #                {_el} не нажался
                #                --------
                #                я попробую достучаться до него посылая Key.Return
                #                ''')
                #            try:self._send_keys( _ , self.driver.Keys.RETURN)
                #            except Exception as ex: logger.error(f'''   ХУЙ! ''')
            return True
        else:
            try: _e = self._find(locator)
            except Exception as ex:  return False , logger.error(f''' Возникла ошибка {ex} поиска элемента {locator} ''') 
        
        
            try:
                _e.click()
            except Exception as ex: 


                                logger.error(f''' 
                                    Возникла ошибка  {ex} 
                                    ----------------------
                                    элемент:
                                    {_e} не нажался
                                    --------
                                    я попробую достучаться до него посылая Key.Return
                                    ''')


            else:
                try:
                    self._send_keys( _ , self.driver.Keys.RETURN)
                except Exception as ex: 
                    return False, logger.error(f'''   ХУЙ! ''') 
                            

        #если после клика изменился url
        #    запоминаю изменения
        if _url_before_click != self.current_url:
            self.previous_url = _url_before_click

        
        return True
    ## SEND KEYS
    def _send_keys(self, keys , locator : dict ='' , el  = None) ->bool:
        _ = locator
        _url_before_send_keys = self.current_url
        ''' Запоминаю url ДО клика '''
        try:
            if isinstance(_['selector'] , dict):
                #пока не использую
                pass
            elif isinstance(_['selector'] , list):
                for i in range(len(_['selector'])):
                    _l : dict = {
                        "attribute": _['attribute'][i],
                        "by": _['by'],
                        "selector": _['selector'][i]}
                    _el = self._find(_l)
                    _el.send_keys(keys)
            else: self._find(_).send_keys(keys)

            #если после клика изменился url
            #    запоминаю изменения
            if _url_before_send_keys != self.current_url:
                self.previous_url = _url_before_send_keys


        except Exception as ex: return False , 
        logger.error(f''' при отправке 
        keys {keys} 
        в   
        locator {locator} 
       {ex} 
        
        при отправке {keys} в {locator} ''')
    ## PAGE REFRESH      
    def _page_refresh(self):
        ##Рефреш с ожиданием полной перезагрузки страницы
        self._get_url(self.driver.current_url)
        pass
    ## CLOSE
    def _close(self):
            if self.driver.close(): 
                logger.error(''' DRIVER CLOSED ''')
            pass

        
