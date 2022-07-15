'''
Created by auto_sdk on 2021.12.23
'''
from top.api.base import RestApi
class AliexpressLogisticsItemForbidattributeQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.query_item_attribute_request = None

	def getapiname(self):
		return 'aliexpress.logistics.item.forbidattribute.query'
