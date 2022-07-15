'''
Created by auto_sdk on 2021.08.10
'''
from top.api.base import RestApi
class AliexpressLogisticsWarehouseQuerydetailRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.consign_type = None
		self.current_page = None
		self.domestic_logistics_num = None
		self.gmt_create_end_str = None
		self.gmt_create_start_str = None
		self.international_logistics_num = None
		self.logistics_status = None
		self.page_size = None
		self.trade_order_id = None
		self.warehouse_carrier_service = None

	def getapiname(self):
		return 'aliexpress.logistics.warehouse.querydetail'
