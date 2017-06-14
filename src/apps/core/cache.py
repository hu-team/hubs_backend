from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.key_constructor import bits


class HubsKeyConstructor(KeyConstructor):
	unique_method_id = bits.UniqueMethodIdKeyBit()
	format = bits.FormatKeyBit()
	language = bits.LanguageKeyBit()
	query_params = bits.QueryParamsKeyBit()
	sql_query = bits.SqlQueryKeyBitBase

cache_key_func = HubsKeyConstructor()
