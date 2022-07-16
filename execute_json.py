# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Tools
# execute_json.py
# всякие полезности для работы с JSON


from pathlib import Path
import json as json
import csv
from loguru import logger
import pandas as pd

## Читаю файл из внешнего источника .
# path: путь к файлу 
def loads(path:Path )-> dict :
    ''' получаю объект Path - не str! '''
    with path.absolute().open(encoding='utf-8') as f:
        data = json.loads(f.read())
    return data




## Документация для функции.
def html2json(html:str)->json:
    pass


## конвертация сложных объектов в список
# @param dict_interpreter_vаlues_only
#   если True:
#       берется только правая часть словаря
#   если False:
#       выводится 2 списка - [[k],[v]]
def convert_to_list(json, dict_interpreter_vаlues_only:bool = True, _l:list=[]) -> list:

    
    if isinstance(json, str):
        ''' если в списке сценариев есть 
        всего один файл '''
        _l.append(json)

    elif isinstance(json, list):
        for json_file in scenario_files: _l.append(json)


    elif isinstance(json, dict):
        for scenario in json.keys(): 
            for json_files in json[scenario]: 
                ''' если есть вложенный словарь - 
               я его рекурсивно обрабатываю'''
                if isinstance(json_files, dict):
                    convert_to_list(json_files, dict_interpreter_vаlues_only, _l)
                else:_l.append(json_files)


    return _l



### экспортирую данные в файл .
# функция позволяет экспортировать словарь в файл 
# из всех точек выполнения сценариев 
def export(supplier, data, filename:str = None, format:list = ['json','csv','txt'])->bool:

    def dumps(data , path:Path):
        with path.absolute().open('w',encoding='utf-8') as f:
            f.write(json.dumps(data))



    if filename == None:
        filename = f'''{supplier.supplier_prefics}'''


    for frmt in format:
        export_file_path = Path(f'''{supplier.ini.paths.export_dir}''' , f'''{filename}.{frmt}''')
        if frmt == 'json':
            dumps(data, export_file_path)

        if frmt == 'csv':
            df = pd.DataFrame(data)
            try:
                df.to_csv(export_file_path , sep = ';' , index=False ,  encoding='utf-8')
            except Exception as ex:
                logger.error(ex)
        if frmt == 'txt': 
            with open(export_file_path, 'w')as txtfile:
                txtfile.write(str(data))
              



