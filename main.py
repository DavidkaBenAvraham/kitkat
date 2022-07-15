# -*- coding: utf-8 -*-
#!/usr/bin/env python
## @package Katia
# main() - запуск программы
# !pip install conda
# !pip install selenium
# !pip install google
# !pip install aliyun-python-sdk-core-v3
# !pip install aliexpress-sdk
# !pip install python-aliexpress-api
## обертка для работы с aliexpress API
## отсюда https://github.com/sergioteula/python-aliexpress-api/  
# !pip install selenium-wire
## обертка для selenium
## с поддержкой request, request.responce 
## и др, хз как подружить с kora
## отсюда https://github.com/DavidkaBenAvraham/selenium-wire  
# !pip install kora
## обертка для google colab
# !pip install pyautogui
## двигалка мыши по экрану
## отсюда https://itproger.com/news/programma-na-python-dlya-upravleniya-kompyuterom-pyautogui


from pathlib import Path
from threading import Thread
''' Работа с потоками описана в https://python-scripts.com/threading '''
from pathlib import Path
from loguru import logger

import execute_json as json
from ini_files_dir import Ini
ini = Ini()
from suppliers import Supplier

''' инициализация '''

threads : list = []
''' потоки '''


## Документация для класса
# класс для запуска каждый сценарий в отдельном потоке
# получаю имя постащика - открываю для его класса поток
# идея в том, чтобы открывать  приложения в новом потоке.
class Thread_for_supplier(Thread):
    supplier : Supplier = None
    ''' здесь рождается класс поставщика в собственном потоке '''

    def __init__(self, supplier_prefics:str ,  ini : Ini):
        ''' в классе Ini() происходит раскрытие launcher.json
        supplier_prefics : str - поставщик из класса ini.suppliers, 
        lang : list - язык/и  из launcher.json ???? нахуя?
        '''

        Thread.__init__(self)
        ### Здесь создался поток. ОСТОРОЖНО! Может повесить малоядерные цпу
        # 
        self.supplier  = Supplier(supplier_prefics = supplier_prefics, ini = ini)
        ### Здесь родился Supplier() в потоке 
        
    def run(self):

        threads.append(self.supplier)
        '''  Старт программы  в потоке'''
        self.supplier.run()
        ## try - except ОБЯЗАТЕЛЬНО !!! зависнет нахуй '''    
        self.supplier.driver.close()
        ''' Финиш '''


def start_script() -> bool:  
    ## Отсюда я запускаю всю программу 
    # ini : Ini = Ini() 
    # Класс инициализации приложения 
    # строится на основе файла launch.json 
    _ = ini.launcher
    for supplier_prefics in _['suppliers']: 
            
        if _['threads']:
            # с потоками -> 
            thread  = thread_for_supplier(supplier_prefics ,  ini)
            thread.start()

        else:
            # Без потоков ->
            supplier  = Supplier(supplier_prefics = supplier_prefics, ini = ini)
            ### Здесь родился Supplier() в ОДНОМ потоке
            # программа будет перелопачивать их один за другим
            supplier.run()


if __name__ == "__main__":
    start_script()