# https://habr.com/ru/post/250921/
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

import login_scenario 
import get_data

def main(browser = 'Firefox' , status = 'dev'):
    '''
    status 
           'dev'  razrabotka  
           'prod' production
    '''
    #print(f'Status {status}')

    if status == 'dev': 
        if browser == 'Firefox': go(webdriver.Firefox())
        if browser == 'Chrome': go(webdriver.Chrome())
        if browser == 'Opera': go(webdriver.Opera())
        if browser == 'Edge': go(webdriver.Edge())

    if status == 'prod':
        if browser == 'Firefox':
            with webdriver.Firefox() as driver:
                go(driver)

        if browser == 'Chrome':
            with webdriver.Chrome() as driver:
                go(driver)

        if browser == 'Opera':
            with webdriver.Opera() as driver:
                go(driver)

        if browser == 'Edge':
            with webdriver.Edge() as driver:
                go(driver)

def go(driver):
    driver.get("http://www.morlevi.co.il")
    if login_scenario.login(driver):
        get_data.maxwevim()

if __name__ == "__main__":
    # execute only if run as a script
    main()