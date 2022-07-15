'''
Created by auto_sdk on 2020.09.08
'''
from top.api.base import RestApi
import execute_json as json
from ini_files_dir import Ini
from attr import attrib, attrs, Factory
@attrs
class AliexpressSolutionOrderGetRequest(RestApi):
	param0 = attrib(init = False , default = None)
	def __attrs_post_init__(self):
		RestApi.__attrs_post_init__(self)
		self.param0 = None

	def getapiname(self):
		return 'aliexpress.solution.order.get'
