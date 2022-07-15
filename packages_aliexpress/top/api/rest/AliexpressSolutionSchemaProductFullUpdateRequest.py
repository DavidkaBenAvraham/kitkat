'''
Created by auto_sdk on 2022.01.10
'''
from top.api.base import RestApi
class AliexpressSolutionSchemaProductFullUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.developer_features = None
		self.schema_full_update_request = None

	def getapiname(self):
		return 'aliexpress.solution.schema.product.full.update'
