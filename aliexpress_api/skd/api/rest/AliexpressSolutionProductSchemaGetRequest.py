'''
Created by auto_sdk on 2021.11.16
'''
from top.api.base import RestApi
class AliexpressSolutionProductSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.aliexpress_category_id = None

	def getapiname(self):
		return 'aliexpress.solution.product.schema.get'
