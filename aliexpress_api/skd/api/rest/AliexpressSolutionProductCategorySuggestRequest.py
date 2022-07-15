'''
Created by auto_sdk on 2022.02.18
'''
from top.api.base import RestApi
class AliexpressSolutionProductCategorySuggestRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.image_url = None
		self.language = None
		self.title = None

	def getapiname(self):
		return 'aliexpress.solution.product.category.suggest'
