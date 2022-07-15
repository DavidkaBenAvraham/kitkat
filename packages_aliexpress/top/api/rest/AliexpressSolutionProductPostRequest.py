'''
Created by auto_sdk on 2022.01.06
'''
from top.api.base import RestApi
class AliexpressSolutionProductPostRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.post_product_request = None

	def getapiname(self):
		return 'aliexpress.solution.product.post'
