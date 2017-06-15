from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.key_constructor import bits


class HubsKeyConstructor(KeyConstructor):
	unique_method_id = bits.UniqueMethodIdKeyBit()
	unique_view_id = bits.UniqueViewIdKeyBit()
	format = bits.FormatKeyBit()
	language = bits.LanguageKeyBit()
	query_params = bits.QueryParamsKeyBit()
	pagination = bits.PaginationKeyBit()


class HubsPerUserKeyConstructor(KeyConstructor):
	unique_method_id = bits.UniqueMethodIdKeyBit()
	unique_view_id = bits.UniqueViewIdKeyBit()
	format = bits.FormatKeyBit()
	language = bits.LanguageKeyBit()
	query_params = bits.QueryParamsKeyBit()
	pagination = bits.PaginationKeyBit()
	user = bits.UserKeyBit()

global_cache_key_func = HubsKeyConstructor()
cache_key_func = HubsPerUserKeyConstructor()
