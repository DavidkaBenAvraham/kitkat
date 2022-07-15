# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module

import sqlite3
''' пока пусть будет  так
import mysql
import mysql.connector
'''
import sys
import ExceptionsHandler
from os.path import abspath
from sqlalchemy import create_engine
import pandas as pd
import pandas.io.sql as psql
#import ExceptionsHandler
#from os.path import abspath заменить на Path()
import datetime
import time
#import json  
from ini_files_dir import Ini
import execute_json as json

 

def connection(connection_type = 'mysql' , server = "davidka.net", trying = 3):
    connection_string = {
    "user": "u177424397_aluf",
    "password": "hB6dyTJ6aikJcbeuSKHZ",
    "host": "141.136.34.4",
    "port": "3306",
    "database": "u177424397_aluf",
    "raise_on_warnings": True
  }

    return mysql.connector.connect(**connection_string)
    try:
        if connection_type == 'mysql'  :return mysql.connector.connect(**connection_string[server])
        if connection_type == 'sqlite3': return sqlite3.connect(**Ini.db_file)
    except:
        
        if trying > 0:
            try: #пиздец, какой костыль! Потому что не только для объектов!!!
                self.log(str(f'''{trying} попытка подключения к бд {conn}'''))
            except: pass
            time.sleep(3)
            trying -=1
            connection(connection_type ,server, trying )
        else:
            try: #пиздец, какой костыль! Потому что не только для объектов!!!
                self.log(str(f'''Не удалось подключиться к бд - {db_connect_strings} '''))
            except: pass
            return False

def execute(query, connection_type = 'mysql' , server = "davidka.net", executemany = False ,  do = 'select'  , return_as_dataframe = True):
    '''
    определяем подключение к базе данных
    можем работать с
    MySql       mysql.connector.connect и с
    sqlite3     sqlite3.connect
    query может быть список комманд
    do : select;insert;update;delete;create
    '''

    '''
     json.dumps(query) используется для экранирования кавычек
     https://ru.stackoverflow.com/questions/944817/%D0%95%D1%81%D1%82%D1%8C-%D0%BB%D0%B8-%D0%B2-python-%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8F-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-%D0%BA%D0%B0%D0%B2%D1%8B%D1%87%D0%B5%D0%BA
    '''

    conn = connection(connection_type,server)
    if conn.is_connected():

        if return_as_dataframe and do == 'select': 
            return get_df_from_query(query , conn)
  
        cursor = conn.cursor()

        if executemany: cursor.executemany(query)
        else: cursor.execute(query)

        if  do == 'select' :
            try:
                out = cursor.fetchall()
            except:
                '''
                не вернулся результат

                лучше проверять на количество записей в курсоре
                '''

   
        try: 
            conn.commit()
        except: 
            pass  # нет надобности в коммите 
        
        conn.close()
    return True

def get_df_from_query(query , conn) -> pd.DataFrame :
    '''
    conn - подключение к бд
    '''
    df = psql.read_sql(query, con = conn)
    conn.close()
    return df


