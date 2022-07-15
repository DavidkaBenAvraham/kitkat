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
              



