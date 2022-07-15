'''
Created by auto_sdk on 2022.01.26
'''
from top.api.base import RestApi
class AliexpressPostproductRedefiningPostaeproductRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.aeop_a_e_product = None
		self.ext_param = None

	def getapiname(self):
		return 'aliexpress.postproduct.redefining.postaeproduct'
