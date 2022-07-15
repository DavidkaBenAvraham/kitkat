'''
Created by auto_sdk on 2022.02.23
'''
from top.api.base import RestApi
class AliexpressLogisticsOrderShipmentRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_aeop_seller_shipment_sub_trade_order_request = None

	def getapiname(self):
		return 'aliexpress.logistics.order.shipment'
