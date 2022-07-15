'''
Created by auto_sdk on 2022.01.20
'''
from top.api.base import RestApi
class AliexpressLogisticsLocalListlogisticsserviceRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.locale = None

	def getapiname(self):
		return 'aliexpress.logistics.local.listlogisticsservice'
