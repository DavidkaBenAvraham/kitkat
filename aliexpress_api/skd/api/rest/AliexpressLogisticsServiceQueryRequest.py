'''
Created by auto_sdk on 2022.01.21
'''
from top.api.base import RestApi
class AliexpressLogisticsServiceQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.interface_request = None

	def getapiname(self):
		return 'aliexpress.logistics.service.query'
