'''
Created by auto_sdk on 2022.03.08
'''
from top.api.base import RestApi
class AliexpressLocalLogisticsOrderInfoQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param1 = None

	def getapiname(self):
		return 'aliexpress.local.logistics.order.info.query'
