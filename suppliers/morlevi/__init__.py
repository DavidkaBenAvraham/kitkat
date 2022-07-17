# -*- coding: utf-8 -*-
#!/usr/bin/env python
## @package Katia.suppliers.morlevi
# Documentation for this module

import execute_json as json
from strings_formatter import StringFormatter as SF
from suppliers.product import Product 
from loguru import logger
def login(supplier):
    _s = supplier
    _d = _s.d
    _d.get_url(_s.settings['login_url'])
    if _login(_s): return True
    else: 
        try:
            #'''
            #закрываю модальные окна сайта
            #выпадающие до входа
            #'''
            logger.error( f''' Ошибка, пытаюсь закрыть popup''')
            _d.page_refresh()
            if _login(_s): return True


            close_popup_locator = (_s.locators['login']['close_popup_locator']['by'], _s.locators['login']['close_popup_locator']['selector'])

            close_popup_btn = _d.find(close_popup_locator)
            _d.wait(5)
            if str(type(close_popup_btn)).find("class 'list'") >-1:  # Если появилось несколько
                for b in close_popup_btn:
                    try:
                        b.click()
                        if _login(_s) : 
                            
                            return True
                            break
                    except: pass
            if str(type(close_popup_btn)).find("webelement") >-1:  # нашелся только один элемент
                close_popup_btn.click()
                return _login(_s)
        except Exception as ex:
            logger.error(f''' 
            Не удалось залогиниться 
            ''')
            return False

def _login(_s):
    logger.debug( f''' Собссно, логин Морлеви''')
    _s.driver.refresh()
    #self.driver.switch_to_active_element()
    email = _s.locators['login']['email']
    password = _s.locators['login']['password']

    open_login_dialog_locator = _s.locators['login']['open_login_dialog_locator']

    email_locator = _s.locators['login']['email_locator']

    password_locator = _s.locators['login']['password_locator']

    loginbutton_locator =  _s.locators['login']['loginbutton_locator']

    try:
        
        _s.d.find(open_login_dialog_locator).click()
        _s.d.find(email_locator).send_keys(email)
        _s.d.find(password_locator).send_keys(password)
        _s.d.find(loginbutton_locator).click()
        logger.debug('Mor logged in')
        return True
    except Exception as ex:
        logger.error(f''' LOGIN ERROR 
        {ex}''')
        return False

def grab_product_page(s , p) -> Product:
    p.grab_product_page(s)



    _ : dict = s.locators['product']
    _d = s.driver
    _d.scroll(3)
    _field = p.fields

    '''комбинации/опции товара '''
    _combinot = p.combinations
    
    
    ''' 
    Вытаскиваю со страницы товара все поля по локаторам
    ------------
    p - товар
    '''
    
    def set_id():
        _id = _d.find(_['product_sku_locator'])


        _field['id'] = _d.find(_['product_sku_locator'])

        logger.debug(f'''
        id - {_field['id']}
        ''')
    def set_sku_suppl():
        _field['mkt suppl'] = _field['id']
        #logger.debug(f'''
        #mkt_suppl - 
        #{_field['mkt_suppl']}
        #''')
    def set_sku_prod():
        if not _field['id']  is None :
            _field['mkt'] = str('ksp-') + _field['id']
        #logger.debug(f'''
        #mkt_suppl - 
        #{_field['mkt_suppl']}
        #''')
    def set_title():
        title = _d.find(_['product_title_locator'])
        _field['title'] = SF.remove_non_latin_characters(title)
        #logger.debug(f'''
        #title - 
        #{_field['title']}
        #''')
    def set_summary():
        _field['summary'] = _d.find(_['product_summary_locator'])
        #logger.debug(f'''
        #summary - 
        #{_field['description']}
        #''')
    def set_description():
        _field['description'] = _d.find(_['product_description_locator'])
        #logger.debug(f'''
        #description - 
        #{_field['description']}
        #''')

    def set_cost_price():
        _price = _d.find(_['product_price_locator'])
        '''  Может прийти все, что угодно  '''
        _price = SF.clear_price(_price)
        _field['cost price'] =  _price
        logger.debug(f'''
        цена - {_field['cost price']}
        ''')
        return True
    def set_before_tax_price():
        _field['price tax excluded']  = _field['cost price']
     
        return True

    def set_delivery():
        '''@TODO  перенести в комбинации '''
        product_delivery_list = _d.find(_['product_delivery_locator'])
        #for i in product_delivery_list:
        #    pass


    def set_images():
        #imgs_list  = _d.find(_['product_images_locator'])
        #imgs_str :str = ','.join(_d.find(_['product_images_locator']))
        imgs = _d.find(_['product_images_locator'])
        ''' может вернуться одна или несколько картинок или хуй.
        есть несколько ситуаций:
        - картинки нет на сайте
        - картинка не загрузилась (таймаут)
        - прочая хуйня
        '''
        if imgs is None: 
            imgs = ''
        elif isinstance(imgs , list):
            imgs = ','.join(imgs)
        
        logger.debug(f''' 
        ссылки на картинки 
        {imgs}
        ''')
        _field['img url'] = imgs
       

    def set_combinations():pass

    def set_qty():pass

    def set_specification():pass

    def set_customer_reviews():pass

    def set_supplier():
        _field['supplier'] = '2787'
        pass

    set_id()
    set_sku_suppl()
    set_sku_prod()
    set_title()
    set_summary()
    set_cost_price()
    set_before_tax_price()
    set_delivery()
    set_images()
    set_combinations()
    #set_qty()
    #set_byer_protection()
    set_description()
    #set_specification()
    #set_customer_reviews()
    set_supplier()
    return p
    pass

