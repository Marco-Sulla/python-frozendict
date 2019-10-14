from enum import Enum

class StringConstant(str, Enum):
	undeletable_err_tpl = "'{klass}' object does not support attribute deletion"
	unsettable_err_tpl = "'{klass}' object does not support attribute setting"
	add_err_tpl = "unsupported operand type(s) for +: '{klass1}' and '{klass2}'"
	sub_err_tpl = "unsupported operand type(s) for -: '{klass1}' and '{klass2}'"
	reinit_err_msg = "you can't reinitialize the object"

	items = "items"
	_dict = "_dict"
	empty = ""
	class_repr_tpl = "{klass}({body})"
	open_curly_bracket = "{"
	closed_curly_bracket = "}"
	dict_repr_items_sep = ", "
	dict_repr_tpl = "{k}: {v}" + dict_repr_items_sep
