'''
Created by auto_sdk on 2021.11.24
'''
from top.api.base import RestApi
class TopSecretGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.customer_user_id = None
		self.random_num = None
		self.secret_version = None

	def getapiname(self):
		return 'taobao.top.secret.get'
