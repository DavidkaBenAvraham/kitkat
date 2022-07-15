'''
Created by auto_sdk on 2021.08.10
'''
from top.api.base import RestApi
class AliexpressLogisticsQueryEnumRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'aliexpress.logistics.query.enum'
