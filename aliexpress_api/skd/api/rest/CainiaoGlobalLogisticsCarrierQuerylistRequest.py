'''
Created by auto_sdk on 2021.01.28
'''
from top.api.base import RestApi
class CainiaoGlobalLogisticsCarrierQuerylistRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.locale = None

	def getapiname(self):
		return 'cainiao.global.logistics.carrier.querylist'
