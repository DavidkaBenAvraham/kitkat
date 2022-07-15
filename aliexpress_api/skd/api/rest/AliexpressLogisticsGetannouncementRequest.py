'''
Created by auto_sdk on 2021.08.27
'''
from top.api.base import RestApi
class AliexpressLogisticsGetannouncementRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_time = None
		self.seller_id = None
		self.start_time = None

	def getapiname(self):
		return 'aliexpress.logistics.getannouncement'
