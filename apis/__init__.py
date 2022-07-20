# -*- coding: utf-8 -*-
#!/usr/bin/env python
##@package Katia
#Documentation for this module

from aliexpress_api import AliexpressApi, models
''' отсюда https://github.com/sergioteula/python-aliexpress-api/ 
не рассматривал 
'''
import top, dingtalk, aliyun 
''' библиотеки aliexperess '''
import datetime
import execute_json as json
from ini_files_dir import Ini
ini = Ini()

from attr import attrs, attrib, Factory
@attrs
class ALIEXPRESS(AliexpressApi):

	_appkey			: str = attrib(init = False, default = None)
	_secret			: str = attrib(init = False, default = None)
	_url			: str = attrib(init = False, default = None)
	_port_http		: str = attrib(init = False, default = None)
	_port_https		: str = attrib(init = False, default = None)
	_access_token	: str = attrib(init = False, default = None)
	_refresh_token	: str = attrib(init = False, default = None)
	_aliexpress_api : AliexpressApi = attrib(init = False, default = None)

	def __attrs_post_init__(self, *args, **kwrads):
		#ini = ini
		_k : dict = json.loads(ini.paths.apis_file)['aliexpress']
		self._appkey = _k['appkey']
		self._secret = _k['secret']
		self._url = _k['url']
		self._port_http = _k['port_http']
		self._port_https = _k['port_https']
		self._access_token = _k['access_token']
		self._refresh_token = _k['refresh_token']
		self.TRACKING_ID = 'new_API'
		self = AliexpressApi(self._appkey, self._secret, models.Language.HE, models.Currency.USD , self.TRACKING_ID  )
	

	def get_api_keys(self) -> dict:
		pass

	def get_product(self , product_id  , product_url) :
		
		#return self.get_products_details([product_id  , product_url])
		#print(products[0].product_title, products[1].target_sale_price)
		product = aliexpress.product_info('1005001597632686')
		print(product.product_title)
	def request(self , https:bool=True):
		#return self._aliexpress_api


		_port = self._port_https if https else self._port_http
		req=top.api.AliexpressSolutionOrderGetRequest(self._url,_port)
		req.set_app_info(top.appinfo(self._appkey,self._secret))
 
		req.param0=""
		try:
			sessionkey = self._access_token
			resp= req.getResponse(sessionkey)
			print(resp)
		except Exception as ex:print(ex)


		#req=top.api.AliexpressSolutionOrderGetRequest()
		#req.set_app_info(top.appinfo(self._appkey, self._secret))
		
		#req.param0 = {
		##'create_date_start': (datetime.utcnow() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
		#'create_date_start': ini.get_now(),
		#'page_size': 10,
		#'current_page': 1
		#}

		##https://oauth.aliexpress.com/authorize?response_type=token&client_id=33759699&state=1212&view=web&sp=ae
		#sessionkey = self._access_token

		#resp = req.getResponse(sessionkey)
		#pprint.pprint(resp['aliexpress_solution_order_get_response']['result'])

		

