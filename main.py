# -*- coding: utf-8 -*-
#!/usr/bin/env python
## @package Katia
## обертка для работы с aliexpress API
## отсюда https://github.com/sergioteula/python-aliexpress-api/  
## обертка для selenium
## с поддержкой request, request.responce 
## и др, хз как подружить с kora
## отсюда https://github.com/DavidkaBenAvraham/selenium-wire  
## обертка для google colab
## двигалка мыши по экрану
## отсюда https://itproger.com/news/programma-na-python-dlya-upravleniya-kompyuterom-pyautogui

import time
from pathlib import Path
from threading import Thread
''' Работа с потоками описана в https://python-scripts.com/threading '''

from suppliers import Supplier

import GLOBAL_SETTINGS
import execute_json as json
logger = GLOBAL_SETTINGS.logger


threads : list = []
''' потоки '''


## Документация для класса
# класс для запуска каждый сценарий в отдельном потоке
# получаю имя постащика - открываю для его класса поток
# идея в том, чтобы открывать  приложения в новом потоке.
class Thread_for_supplier(Thread):
    supplier : Supplier = None
    ''' здесь рождается класс поставщика в собственном потоке '''

    def __init__(self, supplier_prefics:str):
        ''' в классе Ini() происходит раскрытие launcher.json
        supplier_prefics : str - поставщик из класса ini.suppliers, 
        lang : list - язык/и  из launcher.json ???? нахуя?
        '''

        Thread.__init__(self)
        ### Здесь создался поток. ОСТОРОЖНО! Может повесить малоядерные цпу
        # 
        self.supplier  = Supplier(supplier_prefics = supplier_prefics)
        ### Здесь родился Supplier() в потоке 
        
    def run(self):

        threads.append(self.supplier)
        '''  Старт программы  в потоке'''
        self.supplier.run()
        ## try - except ОБЯЗАТЕЛЬНО !!! зависнет нахуй '''    
        self.supplier.driver.close()
        ''' Финиш '''

## Отсюда я запускаю всю программу 
def start_script() -> bool:  
    
    # по умолчанию список suppliers для скрапинга
    # находится в launcher.json, но я могу спросить их при запуске

    counter = 0
    timeout = False
    suppliers = ''

    ####
    #print(f''' supplier / suppliers prefics.
    #for list of suppliers use [suppl1,suppl2]''', end = ': ')
    #suppliers = input()


    if suppliers == '': suppliers = GLOBAL_SETTINGS.SUPPLIERS_LIST_FOR_SCRAPPING
    # если я получил одного поставщика
    # я кладу его в список, 
    # если пришли несколько через запятую - 
    # я строю из них список через .join(',')
    if isinstance(suppliers , str):
        if str(suppliers).find(',')>-1:
            suppliers = suppliers.split(',')
        else: 
            suppliers = [suppliers]
    elif isinstance(suppliers , list):pass # всё заебись



    for supplier_prefics in suppliers: 
            
        if GLOBAL_SETTINGS.THREADS:
            # с потоками -> 
            thread = Thread_for_supplier(supplier_prefics)
            thread.start()

        else:
            # Без потоков ->
            supplier  = Supplier(supplier_prefics = supplier_prefics)
            ### Здесь родился Supplier() в ОДНОМ потоке
            # программа будет перелопачивать их один за другим
            supplier.run()
            logger.info(f''' 
            ЗАВЕРШЕНИЕ 
            supplier {supplier.supplier_prefics} 
            ''')
            supplier.driver.quit()


if __name__ == "__main__":
    start_script()