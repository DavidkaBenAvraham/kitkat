from selenium.webdriver.common.keys import Keys

def login(driver):
    #<a id="21" ...
    login_ancor_id = '21'
    driver.implicitly_wait(25)
    try:
        driver.find_element_by_id('21').click() 
    except:
        try:
            driver.find_element_by_id('closeXButton').click()
            driver.implicitly_wait(10)
            driver.find_element_by_id('2507').click() 
            driver.implicitly_wait(2)
            driver.find_element_by_id('21').click() 
        except:
            try:
                driver.implicitly_wait(2)
                driver.find_element_by_id('2507').click() 
            except:
                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_id('2507').click() 
                except:
                    pass
            finally:
                driver.implicitly_wait(2)
                driver.find_element_by_id('21').click() 
            pass


    # modal-dialog является частью основного html 
    # страницы и не требует никаких спец методов для обращения к ним.
    driver.find_element_by_id('Email').send_keys('sales@aluf.co.il')
    driver.find_element_by_id('Password').send_keys('9643766')
    try:
        driver.find_element_by_id('3486').click()
    except:
        driver.find_element_by_id('closeXButton').click()
        driver.find_element_by_id('3486').click()

    # https://habr.com/ru/post/250921/
    # Следующая строка — это утверждение (англ. assertion), что заголовок содержит слово 
    # “Python” [assert позволяет проверять предположения о значениях произвольных данных 
    # в произвольном месте программы. По своей сути assert напоминает констатацию факта, 
    # расположенную посреди кода программы. В случаях, когда произнесенное утверждение не верно, 
    # assert возбуждает исключение. Такое поведение позволяет контролировать выполнение программы 
    # в строго определенном русле. Отличие assert от условий заключается в том, что программа 
    # с assert не приемлет иного хода событий, считая дальнейшее выполнение программы или функции 
    # бессмысленным — Прим. пер.]:

    # driver.implicitly_wait(10)
    assert 'שלום אלוף' in driver.find_element_by_id('24').text 
    return True