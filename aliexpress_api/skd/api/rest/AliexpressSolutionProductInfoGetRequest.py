'''
Created by auto_sdk on 2022.03.16
'''
from top.api.base import RestApi
class AliexpressSolutionProductInfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.product_id = None

	def getapiname(self):
		return 'aliexpress.solution.product.info.get'
