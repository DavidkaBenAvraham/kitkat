'''
Created by auto_sdk on 2022.02.28
'''
from top.api.base import RestApi
class AliexpressLogisticsLocalGetwaybillbypdfRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.intl_tracking_no = None
		self.warehouse_order_id = None

	def getapiname(self):
		return 'aliexpress.logistics.local.getwaybillbypdf'
