# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia.Tools
## Documentation for module strings_formatter.py
    #
    #        $a = '1,5,';
    #        if(!preg_match('/^(?:\d\,)+$/', $a)) {
    #         echo 1;
    #        }
    #        ^ - начало строки
    #        $ - конец строки
    #        (?:\d\,) - цифра и запятая
    #        + - ищем один или более раз (в данном случае цифру с запятой)
    #        Если нужно искать без запятой в конце:
    #        /^(?:\d\,)+\d?$/
    #        Если через запятую будут указаны большие числа (132,564,234324):
    #        /^(?:\d+\,)+\d?$/
    #    наиболее важные методы регулярного выражения модуля Python Re:
    #                Re.findall (шаблон, строка) : Проверяет, соответствует ли строка шаблон и возвращает Все вхождения 
    #                                            сопоставленного шаблона как список строк.
    #                Re.Search (шаблон, строка) : Проверяет, соответствует ли строка шаблона Regex и возвращает только Первый матч 
    #                                            как объект матча. Объект Match – это просто: объект, который хранит мета информацию о матче, 
    #                                            такой как соответствующая позиция и соответствующая подстрока.
    #                Re.match (шаблон, строка) : Проверяет, если кто-нибудь Струнный префикс 
    #                                            Соответствует шаблону Regex и возвращает объект совпадения.
    #                Re.fullmatch (шаблон, строка) : Проверяет, если целая строка Соответствует шаблону Regex и 
    #                                            возвращает объект совпадения.
    #                Re.compile (Pattern) : Создает объект регулярного выражения из шаблона для ускорения совпадения, 
    #                                            если вы хотите использовать шаблон Regex несколько раз.
    #                Re.Split (шаблон, строка) : Разбивает строку, где бы закономерность регенсирует и возвращает список строк. 
    #                                                Например, вы можете разделить строку в список слов, используя пробельные символы в качестве сепараторов.
    #                Re.sub (шаблон, репрект, строка) : Заменяет ( sub stitutes) Первое возникновение рисунка Regex с заменой 
    #                                                String Repland и вернуть новую строку.
    #                чтобы проверить, содержит ли строка шестнадцатеричные цифры (от 0 до 9 и от A до F), следует использовать 
    #                такой диапазон:
    #                [A-Fa-f0-9]
    #                Чтобы проверить обратное, используйте отрицательный диапазон, который в нашем случае подходит под любой символ, 
    #                кроме цифр от 0 до 9 и букв от A до F:
    #                [^A-Fa-f0-9]


    ##pattern_find_phone : re = attrib(init = False , default = re.compile(r'''(
	   ## (\d{3}|\(\d{3}\))?   #Area code
	   ## (\s|-|\.)			 #Separator
	   ## (\d{3})				 #First 3 digits
	   ## (\s|-|\.)			 #Separator
	   ## (\d{4})				 #Second four digits
	   ## (\s*(ext|x|ext.)\s*(\d{2,5}))?
	   ## )''', re.VERBOSE)

    ##pattern_find_email : re = attrib(init = False , default = re.compile(r'''(
	   ## [a-zA-Z0-9_%+-.]+	#Username
	   ## @					#@ symbol
	   ## [a-zA-Z0-9.-]+		#domain name
	   ## (\.[a-zA-z0-9]{2,5})#dot-something
	   ## )''', re.VERBOSE)


import re
import pandas as pd
import execute_json as json
import sys
import os
import importlib
import datetime
import time
import json
import random as rnd

from attr import attrs, attrib, Factory

'''
https://github.com/chuanconggao/html2json/blob/master/README.md
'''


pattern_remove_HTML :re = re.compile ('<[^<]+?>')
pattern_remove_non_latin_characters : re = re.compile ('[^A-Za-z0-9-]')
pattern_remove_line_breaks : re = re.compile ('^\s+|\n|\r|\s+$')
pattern_clear_price : re = re.compile ('[^0-9.,]')
pattern_clear_number : re = re.compile ('[^0-9.]')
pattern_remove_special_characters :re = re.compile ('[#|]')            
pattern_remove_supplier_name :re = re.compile ('[KSP,ksp]')
    
import ast

@attrs
class StringFormatter():
    ''' Обработчик строк '''

    def remove_suppliers_and_special_chars(method_to_decorate:object , s:str)->object: 
        ## Декоратор для внутренних функций форматера.
        #Убираю имя поставщика и значки не удовлетворяющие условиям хранения строк в базе данных
        #моего каталога
        
        def remover(self , s:str)->str:
            s = pattern_remove_suppliers_from_string.sub(r'',s)
            s = pattern_remove_special_characters.sub(r'',s)
            s = pattern_remove_line_breaks.sub(r'',s)
            method_to_decorate(self,s)
        return remover(s)

    def __attrs_post_init__(self , *srgs, **kwrads):
        ## инициализация класса StringFormatter()
        self.pattern_remove_HTML = pattern_remove_HTML
        self.pattern_remove_non_latin_characters = pattern_remove_non_latin_characters
        self.pattern_remove_line_breaks = pattern_remove_line_breaks
        self.pattern_clear_number = pattern_clear_number
        self.pattern_clear_price = pattern_clear_price
        self.pattern_remove_special_characters = pattern_remove_special_characters

        pass
    @staticmethod
    # убираю все значки переноса строк
    def remove_line_breaks(s:str)->str:
        def _(s):
            return pattern_remove_line_breaks.sub(r'', s).strip()

        if isinstance(s , list ):
            for sub_s in s:
                sub_s = _(sub_s)
        else: s=_(s)
        return s
    
    @staticmethod
    # remove_suppliers_and_special_chars
    def remove_htmls(s:str)->str:
        def _(s):
            return pattern_remove_HTML.sub(r'', str(s)).strip()
        ''' если пришел список строк '''
        if isinstance(s , list ):
            for sub_s in s: sub_s = _(sub_s)
        else: s=_(s)
        return s


    @staticmethod
    #     def remove_non_latin_characters
    def remove_non_latin_characters(s:str)->str:
        s = StringFormatter.remove_special_characters(s)
        def _(s):
            return pattern_remove_non_latin_characters.sub(r'', str(s)).strip()

        ''' если пришел список строк '''
        if isinstance(s , list ):
            for sub_s in s: sub_s = _(sub_s)
        else: s=_(s)

        return s
    @staticmethod
    def remove_special_characters(s:str)->str:
        s = StringFormatter.remove_htmls(s)
        s = StringFormatter.remove_line_breaks(s)
        return s

    @staticmethod
    def clear_number(s:str)->str:
        def _(s):
            s = pattern_clear_number.sub(r'', str(s)).strip()
            return ast.literal_eval(s)

        if isinstance(s , list):
            for sub_s in s: sub_s = _(sub_s)
        else: s = _(s)
        return s
    @staticmethod
    def clear_price(s:str)->str:
        def _(s):
            s = pattern_clear_price.sub(r'', str(s)).strip().replace(',','.')
            return ast.literal_eval(s)

        if isinstance(s, list ):
            for sub_s in s: sub_s = _(sub_s)
        else: s=_(s)
        return s

    @staticmethod
    def convert_url_to_valid_string(s)->str:
        def remove_protocol(s)->str:
            return s.split(':')[-1]
        def convert_slashes_to_to_mysign(s)->str:
            return s.split('/')[-1]
        def convert_dottes_to_underlines(s)->str:
            return str(s).replace('.','_')
        def convert_question_sign_to_mysign(s)->str:
            return str(s).replace('?','-_params_-')
        def convert_amp_sign_to_mysign(s)->str:
            return str(s).replace('&','-_p_-')
        def convert_eq_sign_to_mysign(s)->str:
            return str(s).replace('=','-_v_-')

        s = remove_protocol(s)
        s = convert_dottes_to_underlines(s)
        s = convert_slashes_to_to_mysign(s)
        s = convert_question_sign_to_mysign(s)
        s = convert_amp_sign_to_mysign(s)
        s = convert_eq_sign_to_mysign(s)
        
        return s

    @staticmethod
    def  get_urlstr_params_as_dict(s:str)->dict:
       
        _list = str(s).split(str(s).find('?'))
        _params_str = f'''{{ {str(_list[1]).strip().replace('=' , ':' ,str(_list[1]))} }}'''
        _params = ast.literal_eval(_params_str)

        _out :dict = {"url":_list[0], "params":_params}

        return _out
