import execute_products as product
from Ini import Ini
#import execute_json as json
import execute_json as json
import check_and_convert_datatypes as check_type
from Logging import Log as Log

@print_f
def execute_list_of_scenaries(self) ->[] :
    
    ''' по умолчанию все сценарии прописаны в файе <supplier>.json 
    при инициализации объекта он хранится в self.scenaries
    
    Сценарии сгруппированы в иерархии:
  <scenario>:[
        [],
        []
    ]

    self - class Supplier (mor, cdata, visual, etc.)


    '''

    #1. Общий список товаров полученный в ходе выполнения ВСЕХ сценариев
    p = []


    for scenario_files in self.scenaries:
        
        for json_file in scenario_files:      
            
            self.json_scenario = json.loads( f'''{self.path_root}Ini/{json_file}''')

            # заполняемый сейчас список товаров
            current_p = run_scenario(self)
            #self.log(f''' список заполненных товаров current_p {current_p}''')
            # проверяю, что список товаров не пустой и присоединяю его к существующшму
            if not check_type.is_none_or_false(current_p):  
                p += current_p

    ''' возвращает список товаров по всему пройденому сценарию'''
    return p

@print_f
def run_scenario(self):
   
    product.build_produscts_list_by_scenario(self)
    product.flush_p(self)
