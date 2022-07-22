# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##@brief Doxygen style comments
##@package Katia.Product
import inspect
from pathlib import Path
import pandas as pd
from script_logger import logger

from strings_formatter import StringFormatter
formatter = StringFormatter()
from ini_files_dir import Ini
ini = Ini()
import execute_json as json

from attr import attrs, attrib, Factory
@attrs

class Category():
  
    ##@param fields : pd.DataFrame 
    #поля товара 
    fields : pd.DataFrame = attrib(init = False, default = None)

    ##@param combinations : pd.DataFrame
    #поля комбинаций товара
    combinations : pd.DataFrame = attrib(init = False , default = None)
    

    ##@param attributes : pd.DataFrame
    #поля аттрибутов товара
    attributes : pd.DataFrame = attrib(init = False , default = None)
   
    ## инициализация класса
    #
    #словарь полей товара определена в файле <prestashop>_product_fields.json
    #словарь полей комбинаций товара определена в файле <prestashop>_product_combination.json
    def __attrs_post_init__(self , *args, **kwards):

        self.fields = json.loads(Path(SCENARIES_DIRECTORY , f'''prestashop_product_fields.json'''))
        self.combinations =json.loads(Path(SCENARIES_DIRECTORY , f'''prestashop_product_combinations_fields.json'''))
        
    
    @attrs
    class err:
        def __attrs_post_init__(self , *args, **kwards):
            pass

        def handler(ex:Exception , locator , field):
            ## 
            #@params ex
            #@params field
            #@params locator


            #field = None
            logger.error(f''' 
            {ex}, 
            locator {locator} , 
            field {field} ''')
            return False


    ##собраю локаторами нужные мне позиции со страницы товара 
    #collect the positions from the product page with locators
    def grab_product_page(self , s):
      
        _d = s.driver
        _ : dict = s.locators['product']
        _current_node = s.current_node
        field = self.fields
            
        def set_id():pass
        def set_sku_suppl():pass
        def set_supplier(): pass
        def set_title():pass
        def set_cost_price():pass
        def set_before_tax_price():pass
        def set_delivery():pass
        def set_images():pass            
        def set_combinations():pass
        def set_qty():pass
        def set_byer_protection():pass
        def set_description():pass
        def set_specification():pass
        def set_customer_reviews():pass


        def set_categories():
            categories :str = ','.join(_current_node['prestashop_categories'].keys())
            field['categories'] = categories

        set_id()
        set_sku_suppl()
        set_title()
        set_supplier()
        set_cost_price()
        set_before_tax_price()
        set_delivery()
        set_images()
        set_combinations()
        set_qty()
        set_byer_protection()
        set_description()
        set_specification()
        set_customer_reviews()
        set_categories()
        
        return self
