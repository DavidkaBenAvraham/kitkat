# -*- coding: utf-8 -*-
#!/usr/bin/env python
##@package Katia.Supplier
##Documentation for this module
#                                       
#           Скрипты выполнения сценариев
#
#       execute_list_of_scenaries(Supplier) -> bool
#       run_scenario(s , scenario) -> bool:
#       get_list_products_urls(s , scenario_node : dict ) ->list:


from pathlib import Path
import pandas as pd
from loguru import logger
from suppliers.product import Product
import execute_json as json
from strings_formatter import StringFormatter as SF
#from ini_files_dir import Ini
#ini = Ini()




#           по умолчанию все сценарии  прописаны в файлах <supplier>.json
#           Каждый сценарий поставщика - файл с именем 
#           <supplier>_categories_<category_name>_<model>_<brand>.json
#           при инициализации объекта он хранится в self.scenaries
#           -------------------------------
#           supplier - class Supplier  f.e.: mor, cdata, visual, 
#               aliexpress, ebay, amazon etc.
def execute_list_of_scenaries(supplier) -> bool :
    logger.debug(f''' 
    Старт 
    --------------------
    
    ''')

    s = supplier
    _d = s.driver
   
    
    ## 0. 
    if not _d.get_url(s.settings['start_url']):
        logger.error(f''' supplier not started in url:
            {s.settings['start_url']}''')
        return False

    ## конвертирую сложные объекты в просты списки
    scenario_files = json.convert_to_list(s.settings['scenaries'])

    for json_file in scenario_files:
        ''' запускаю json файлы один за другим '''
        run_scenario_file(s ,json_file)
        s.settings['last_runned_scenario']=json_file
    return True


## 1.
    # Запускаю каждый сценарий из из списка <supplier>.json["scenaries"]
    #   файл сценариев Алиэкспресс отличается тем, что в файл включены хедеры
    #   магазинов. Я это сделал, чтобы не плодить мелкие файлы по 
    #   каждому магазину.
def run_scenario_file(suppiler, json_file) -> bool:
    _s = suppiler
    _s.scenaries = json.loads(Path(_s.ini.paths.ini_files_dir , f'''{json_file}'''))
    _s.scenario_category = f'''{json_file.split('_')[-2]}{json_file.split('_')[-1]}'''
    _s.export_file_name = f'''{_s.settings['supplier_prefics']}-{_s.scenario_category}'''
    ''' третье слово в названии файла сценариев это категория товаров '''
    while len(_s.scenaries.items())>0:
        _scenario = _s.scenaries.popitem()[1]
        run_scenario(_s , _scenario) 
    json.export(_s, _s.p , _s.export_file_name  , ['csv'] )

def run_scenario(s , scenario) -> bool:
    '''
    -текущий сценарий исполнения состоит из узлов. Каждый узел состоит из:
    - <brand> 
    - [<model>] необязательное полеstore_id
    - <url> откуда собирать товары
    - <prestashop_categories> список id категорий 
    - <price_rule> пересчет для магазина по умолчанию установливается в self.price_rule

    '''
    
    ## бегунок
    def run(s, node):
        ''' бегунок '''

        '''# СОБИРАЮ ДАННЫЕ СО СТРАНИЦЫ '''
        def grab_product_page():
            product : Product = s.related_functions.grab_product_page(s , Product())
            
            if not product:
                return False
            ''' что-то не сработало при наполнении полей товара'''


            ''' получаю товар 
            заполняю все свойства товара в функции 
            grab_product_page() для каждого поставщика.

            c) Добавляю поля товара в список товаров поставщика 
            для их дальнейшей обработки
            '''
            product_fields : pd.DataFrame = product.fields
            s.p.append(product_fields)
            pass

        s.current_node = node

        '''              1                          '''
        ''' получаю список url на страницы товаров '''
        list_products_urls : list = get_list_products_urls(s , node)
        

        ''' в исполняемом узле может не оказаться товаров. 
        В этом случае возвращаю False 
        (перехожу к следующему узлу выполнения) '''
        if list_products_urls is None or len(list_products_urls) == 0 : return False 

        '''              2                          '''
        ''' driver вернул urls на страницы товаров ... '''


        ''' ... списком '''
        ''' перебираю список адресов товаров'''
        if isinstance(list_products_urls, list):      
            for product_url in list_products_urls :
                '''функция get_url('url') возвращает True, 
                если переход на страницу был успешен,
                иначе False.
                Исключения обрабатываются внутри самой get_url()'''
                if s.driver.get_url(product_url) : 
                    grab_product_page()
                    
                else: 
                    logger.error(f''' нет такой страницы товара {product_url} ''') 
                    continue

            export()

            ''' ... строкой '''
        else: 
            if s.driver.get_url(list_products_urls):
                '''функция get_url('url') возвращает True, 
                если переход на страницу был успешен,
                иначе False.
                Исключения обрабатываются внутри самой get_url()'''
                grab_product_page()
            else:
                logger.error(f''' нет такой страницы товара {list_products_urls} ''') 
        

            
    # экспорт файла
    def export():
        json.export(s, s.p  , f'''{s.export_file_name}''', ['csv'])
        pass


    ## aliexpress etc multitrade
    ###         имеем дело с магазином
        # текущий сценарий в формате dict сдвинут  вправо 
        # и находится в узле  scenaries:{} 
    if 'store_id' in scenario.keys():
        while len(scenario['scenaries'].items())>0:
            run(s , scenario['scenaries'].popitem()[1])
            #json.export(s, s.p  , f'''{s.export_file_name}''', ['csv'])
            export()

        
    ## ksp, morlevi etc alone trade
        ''' имею дело с узлом сценария как в ksp, mor, etc '''
    else:
        run(s , scenario)
        #json.export(s, s.p  , f'''{s.export_file_name}''', ['csv'])
        export()

    export()
    return True

## get_list_products_urls
# and ссылки на все товары в категории 
# по локатору self.locators['product']['link_to_product_locator']
def get_list_products_urls(s , scenario_node : dict ) ->list:


    ###############################################
    #
    #   Проверяю изменения чексбоксов на странице категории
    #   узнаю изменения после последнего посещения
    #   Собираю актуальные баннеры
    # 
    #########################################################
    def get_page_check_list(s):
        locator = {
                   'by': 'xpath', 
                   'selector': '//input'}

        elems = s.driver.find(locator)
        controls = []
        for e in elems:
            controls.append(e.id)

        filename = SF.convert_url_to_valid_string(s.driver.current_url)
        _out : dict = {filename:controls}
        logger.debug(f'''экспорт файла {filename} ''')
        json.export(s, _out, filename=filename, format=['json'])

    def get_top_banners(s):
        banners = s.driver.find(s.locators['top_banner_locator'])
        logger.debug(f'''Найдены баннеры {banners} ''')
        s.driver.save_images(banners)




    if not s.driver.get_url(scenario_node["url"]): 
        return [] , logger.error(f'''нет такой страницы! 
                {s.current_node["url"]}
                Возможно, 
                проверить категорию в файле сценария ? ''')

    _ = s.locators['product']['link_to_product_locator']
    ##''' на странице категории могут находится  чекбоксы    
    ## если их нет, в сценарии JSON они прописаны checkbox = false
    ##'''
    #json_checkboxes = scenario_node["checkbox"]
    #if json_checkboxes: 
    #    s.driver.click_checkboxes(s, json_checkboxes) 
    #    log.logger.error(f''' есть чекбоксы {json_checkboxes}''')
       

    


    ##                     Существует два вида показа товаров: 
    #                      переключение между страницами и бесконечная прокрутка 
    if s.locators['infinity_scroll'] == True: 
        logger.debug("infinity scroll")
        ''' А бесконечная прокрука '''
        s.driver.scroll()
        
        #get_page_check_list(s)
        #get_top_banners(s)


        list_product_urls : list = s.driver.find(_)
        return list_product_urls
    
    else:
        ''' Б переключение между страницами реализуется в каждом постащике '''
        list_product_urls = s.related_functions.pagination(s)
        get_page_check_list(s)
        get_top_banners(s)
        return list_product_urls



