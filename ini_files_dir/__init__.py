# -*- coding: utf-8 -*-
#!/usr/bin/env python
##@package Katia.Ini
#
#
#NB!
#                Я использую объектно ориентированный подход к работе с файлами
#                https://habr.com/ru/company/otus/blog/540380/
#По умолчанию относительные пути используют текущую директорию, поэтому явно вызывать os.getcwd() 
#редко нужно. 
#Например, <code>open('file.txt')</code>  открывает файл 'file.txt' в текущей директории. 
#Если необходимо передать полный путь в виде строки, то можно использовать 
#<code> os.path.abspath('file.txt')</code> — getcwd() снова явно не используется.
#<code>Path.cwd()</code> из pathlib модуля возвращает путь к текущей директории как 
#объект c разными полезными и удобными методами
#такими как .glob('**/*.py').
#Директория со скриптом
#Текущая рабочая директория может отличаться от директории с текущим Питон-скриптом. Часто, 
#но не всегда можно <code> os.path.dirname(os.path.abspath(__file__)) </code> использовать, чтобы получить директорию 
#с текущим Питон скриптом, но это не всегда работает. 
#Посмотрите на <code>get_script_dir()</code> функцию, которая поддерживает более общий случай.
#Если хочется получить данные из файла, расположенного относительно установленного Питон-модуля, 
#то используйте <code> pkgutil.get_data()</code> или setuptools' pkg_resources.resource_string() вместо построения путей c помощью 
#<code>__file__</code>. Это работает даже, если ваш пакет упакован в архив. В Python 3.7 появился importlib.resources модуль. 
#К примеру, если у вас есть Питон пакет data внутри которого лежит файл.txt, то чтобы достать текст:
#https://ru.stackoverflow.com/questions/535318/%D0%A2%D0%B5%D0%BA%D1%83%D1%89%D0%B0%D1%8F-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D0%B2-python


import datetime , time
from pathlib import Path

import execute_json as json
import random as rnd

from attr import attrib, attrs, Factory

@attrs
##class Ini()
# Все необходимые установки для запуска программы
#<ul>
#<li>start_time : время запуска скрипта</li>
#<li>webdriver_settings : время запуска скрипта</li>
#<li>print_type : время запуска скрипта</li>
#<li>suppliers : время запуска скрипта</li>
#<li>languages : время запуска скрипта</li>
#<li>if_threads : время запуска скрипта</li>
#<li>mode : время запуска скрипта</li>
#<li>paths() : время запуска скрипта</li>
#</ul>
class Ini():
    
    #start_time          : datetime = attrib(init = False ,default = datetime.datetime.now().strftime('%d-%m_%H.%M.%S'))
    #launcher            : dict = attrib(init = False)
    #paths               : paths = attrib(init = False ,default = None)
  
    @attrs
    class paths():
        ## В классе path я строю все пути к файлам и директориям программы
        
        #launcher        : dict = attrib(kw_only=True)
        #root            : Path = attrib(init=False , default = Path.cwd().absolute())
        #ini_files_dir   : Path  = attrib(init = False, default = False)
        #export_dir      : Path = attrib(init = False, default = False)
        #log_file        : Path = attrib(init = False, default = False)
        #apis_file       : Path = attrib(init = False, default = False)

        #def __attrs_post_init__(self,  *args, **kwards):
        #    _ : dict = self.launcher['program_paths']
        #    self.ini_files_dir = Path(self.root ,  _['ini_files_dir']).absolute()
        #    self.export_dir = Path(self.root.parent , _['export_dir']).absolute()
        #    self.logfile  = Path(self.root.parent , _['log_files_dir'] , f'''{self.launcher['start_time']}.htm''').absolute()
        #    self.apis_file = Path(self.ini_files_dir ,  _['apis_file']).absolute()
  
    
    def __attrs_post_init__(self , *args, **kwards):
        ## __attrs_post_init__ == __init__


        # потихоньку отключаю функционал
        #self.launcher : dict = json.loads(Path('launcher.json'))
        ### словарь из файла ./launcher.json
        #self.launcher['start_time'] = self.get_now()
        #self.paths = self.paths(launcher = self.launcher)
        ### определяю пути для скрипта 

    @staticmethod
    def get_now(strformat : str = '%m%d%H%M%S') -> datetime :
        ##штамп текущего времени
        #------------------
        # @param strformat : в каком формате вернуть штамп (by default : %m%d%H%M%S)
        return  datetime.datetime.now().strftime(strformat)
    
    
    @staticmethod
    def get_randint(r:range = None ) -> int:
        # возвращает random int
        # ------------------
        # @param r : в каком диапазоне вернуть random 
        r = r if not r is None else [0,5]
        return rnd.randint(r)
