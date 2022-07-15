'''
Created by auto_sdk on 2022.03.17
'''
from top.api.base import RestApi
class AliexpressMemberRedefiningUicquerytbnickRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.login_id = None

	def getapiname(self):
		return 'aliexpress.member.redefining.uicquerytbnick'
