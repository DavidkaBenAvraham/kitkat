'''
Created by auto_sdk on 2022.01.06
'''
from top.api.base import RestApi
class AliexpressSolutionFeedSubmitRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.developer_features = None
		self.item_list = None
		self.operation_type = None

	def getapiname(self):
		return 'aliexpress.solution.feed.submit'
