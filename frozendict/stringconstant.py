from enum import Enum

class StringConstant(str, Enum):
	immutable_tpl = "'{klass}' object is immutable"
	add_err_tpl = "unsupported operand type(s) for +: '{klass1}' and '{klass2}'"
	sub_err_tpl = "unsupported operand type(s) for -: '{klass1}' and '{klass2}'"
	reinit_err_msg = "you can't reinitialize the object"
	
	class_repr_tpl = "{klass}({body})"

__all__ = (StringConstant.__name__, )
