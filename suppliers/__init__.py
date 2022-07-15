# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Supplier
##<p>
#
#Все классы поставщиков строятся на базе класса Supplier
#Каждый выполняет свой сценарий из файлов <префикс поставщика>.json
#
#Инициализация класса конкретного поставщика товара:
#s = Supplier(lang : list = [] , supplier : str = <имя поставщика>) 
#</p>


import inspect
import pandas as pd
import importlib
from pathlib import Path
from loguru import logger
from web_driver import Driver 
from strings_formatter import StringFormatter as SF
#formatter = StringFormatter()
import execute_json as json
import suppliers.execute_scenaries as execute_scenaries
from attr import attrs, attrib, Factory


#import xml.etree.ElementTree as ET



@attrs
## Supplier - класс поставщика
# <h3> при инициализации передаются три обязательных параметра <h3>
#<ul>
#<li> supplier_prefics : str <i> f.e. 'ksp','aliexpress' </i></li>
#<li> lang : [str , str] <i> f.e. ['en','he'] </i></li>
#<li> ini : Ini() </li>
#</ul>
#<cite> s = Supplier(supplier_prefics = supplier_prefics, lang = lang , ini = ini) </cite>
class Supplier:


    
    supplier_prefics    : str  = attrib(kw_only = True, default = None)                         
    '''  Обязательные ключи запуска - имя поставщика    '''
  
    ini                 : ini = attrib(kw_only = True, default = None)
    ''' Параметры из лончера '''

    settings :dict  = attrib(init = False, default = None)
    
    paths               : paths  = attrib(init = False, default = None)
    ''' класс с путями всяких разных директорий '''

    price_rule          : str = attrib(init = False, default = None)                         
    ''' правило пересчета цены от поставщика, заложеное в сценарии.
                        в будущем правило есть смысл разложить по клиентам , 
                        категориям и магазинам '''





    ''' с локаторами как-то нелогично 
    их много
    '''
    locators            : dict  =  attrib(init = False, default = None)                         
    ''' локаторы элементов страницы              '''

    categories_locator  : dict = attrib(init = False, default = None)  
    ''' локаторы элементов категорий. Сейчас я нахожусь в 
        раздумывании вынести категории в отдельный объект'''

    banners_locator     : dict  = attrib(init = False, default = None) 
    ''' локаторы элементов категорий. Сейчас я нахожусь в 
        раздумывании вынести категории в отдельный объект'''



    current_scenario    : dict = attrib(init = False , default = None) 
    '''Исполняемый в данный момент сценарий в формате dict{}'''
    
    current_scenario_category   : str =  attrib(init=False , default = None)
    '''Категория товаров в исполяемом сценарии 
                                    название категории заложено в третье слово имени сценария'''

    current_scenario_current_url : str =  attrib(init = False, default = None)                         
    '''     url адрес сценария  '''

    current_node        : dict =  attrib(init=False, default = None)  
    '''  исполняемый узел сценария '''

    current_nodename    : str =  attrib(init=False, default = None) 
    ''' Имя испоняемого узла сценария'''
    export_file_name    : str =  attrib(init=False, default = None) 


    related_functions = attrib(init = False , default = None)
    ''' функции, присущие конкретному постащику '''

    driver  : Driver = attrib(init = False , default = None)
    ''' вебдрайвер - мотор всей системы '''

    d = driver
    
    p : Factory(list) = attrib(init = False , default = [])
    ''' товары '''

    c : Factory(list) = attrib(init = False , default = [])
    ''' категории '''



    ## Установки запуска  класса поставщика передаются через обязательные ключи
    # self.supplier_prefics = supplier_prefics
    # self.lang = lang 
    # которые задяются при инициализации класса Supplier в виде парамтров:  
    # attrib(kw_only = True)  
    def __attrs_post_init__(self, *args, **kwards):
        _ini = self.ini


        self.settings : dict  = json.loads(Path(_ini.paths.ini_files_dir , f'''{self.supplier_prefics}.json'''))

        self.start_time = _ini.get_now()

        self.driver = Driver().set_driver(_ini)

        self.locators : dict = json.loads(Path(_ini.paths.ini_files_dir , f'''{self.supplier_prefics}_locators.json'''))
        ''' локаторы элементов страницы '''
        
        self.related_functions = importlib.import_module(f'''suppliers.{self.supplier_prefics}''')
        ''' подгружаю релевантные функции для конкретного поствщика '''

        
        
        if self.settings['if_login']: self.related_functions.login(self)
        ''' логин '''

        logger.info(f'''Родился объект supplier {self.supplier_prefics}''')

    ''' ------------------ КОНЕЦ  -------------------------- '''


    ## пуск
    def run(self):
        ''' Запуск кода сценариев   '''
        execute_scenaries.execute_list_of_scenaries(self)
        
        #self.related_functions.run_local_scenario()

        #self.related_functions.run_shops(self)

        #C = self.related_functions.categories()

        #C.build_ALIEXPRESS_categories_table(self)
        #''' собираю дерево каталогов'''
        #self.SHOP.build_SHOP_categories_table()

        #self.run()
        ''' собираю товары по сценариям'''

        #self.export_file()
    ''' ------------------ КОНЕЦ  -------------------------- '''



   