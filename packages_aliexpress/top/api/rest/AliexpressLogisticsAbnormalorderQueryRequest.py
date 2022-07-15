'''
Created by auto_sdk on 2022.01.06
'''
from top.api.base import RestApi
class AliexpressLogisticsAbnormalorderQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.current_page = None
		self.gmt_create_end = None
		self.gmt_create_start = None
		self.gmt_status_update_end = None
		self.gmt_status_update_start = None
		self.intl_tracking_no = None
		self.page_size = None
		self.trade_order_id = None
		self.warehouse_status_list = None

	def getapiname(self):
		return 'aliexpress.logistics.abnormalorder.query'
