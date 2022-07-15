'''
Created by auto_sdk on 2019.04.10
'''
from top.api.base import RestApi
class AliexpressMerchantProfileGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'aliexpress.merchant.profile.get'
