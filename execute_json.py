# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @package Katia.Tools

from pathlib import Path
import json as json
import csv
import pandas as pd

## Сохраняю установки в файл поставщика
def dump_supplier_settings(supplier):
    file_path = Path(f'''{supplier.SCENARIES_DIRECTORY}''',f'''{supplier.supplier_prefics}.json''')
    dump(supplier.settings , file_path)

## Читаю файл из внешнего источника .
# path: путь к файлу 
def loads(path:Path)-> dict :
    ''' получаю объект Path - не str! '''
    with path.open(encoding='utf-8') as f:
        data = json.loads(f.read())
    return data

## Документация для функции.
def html2json(html:str)->json:
    pass


## конвертация сложных объектов в список
# @param extract_keys_only
#   если True:
#       берется только правая часть словаря
#   если False:
#       выводится 2 списка - [[k],[v]]
def convert_to_list(json, extract_keys_only:bool=True, _l:list=[])->list:

    
    if isinstance(json, str):
        ''' 
        если в списке сценариев есть 
        всего один файл 
        '''
        _l.append(json)

    elif isinstance(json, list):
        for j in json: 
            ''' может попасться список 
            или словарь в списке. Гоню рекурсию
            '''
            if isinstance(j,dict) or isinstance(j,list):
                convert_to_list(j, extract_keys_only, _l)
            else:
                _l.append(j)


    elif isinstance(json, dict):
        for scenario in json.keys(): 
            for j in json[scenario]: 
                ''' если есть вложенный словарь - 
               я его рекурсивно обрабатываю'''
                if isinstance(j, dict) or isinstance(j,list):
                    convert_to_list(j, extract_keys_only, _l)
                else:_l.append(j)


    return _l

def dump(data, path:Path):
        with path.absolute().open('w',encoding='utf-8') as f:
            json.dump(data, f)

### экспортирую данные в файл.
# функция позволяет экспортировать словарь в файл 
# из всех точек выполнения сценариев 
def export(supplier, data, filename:str = None, format:list = ['json','csv','txt'])->bool:


    if filename == None:
        filename = f'''{supplier.supplier_prefics}'''


    for frmt in format:
        export_file_path = Path(f'''{supplier.EXPORT_DIRECTORY}''' , f'''{filename}.{frmt}''')
        if frmt == 'json':
            dump(data, export_file_path)

        if frmt == 'csv':
            df = pd.DataFrame(data)
            try:
                df.to_csv(export_file_path, sep = ';', index=False,  encoding='utf-8')
            except Exception as ex:
                logger.error(ex)
        if frmt == 'txt': 
            with open(export_file_path, 'w')as txtfile:
                txtfile.write(str(data))
              



