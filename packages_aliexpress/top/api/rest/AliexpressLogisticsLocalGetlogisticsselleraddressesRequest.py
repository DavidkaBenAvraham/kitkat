'''
Created by auto_sdk on 2022.01.14
'''
from top.api.base import RestApi
class AliexpressLogisticsLocalGetlogisticsselleraddressesRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.seller_address_query = None

	def getapiname(self):
		return 'aliexpress.logistics.local.getlogisticsselleraddresses'
