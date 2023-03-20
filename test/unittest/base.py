import pytest

class FrozendictTestBase:
    _frozendict_class = None
    
    
    @property
    def frozendict_class(self):
        val = self._frozendict_class
        
        if val == None:
            raise ValueError("frozendict_class is None")
        
        return val
    
    
    @frozendict_class.setter
    def frozendict_class(self, val):
        self._frozendict_class = val
    
    
    _c_ext = None
    
    
    @property
    def c_ext(self):
        val = self._c_ext
        
        if val == None:
            raise ValueError("c_ext is None")
        
        return val
    
    
    @c_ext.setter
    def c_ext(self, val):
        self._c_ext = val
    
    
    _is_subclass = None
    
    
    @property
    def is_subclass(self):
        val = self._is_subclass
        
        if val == None:
            raise ValueError("is_subclass is None")
        
        return val
    
    
    @is_subclass.setter
    def is_subclass(self, val):
        self._is_subclass = val
    
    
    ##########################################################################
    # dict fixtures

    @pytest.fixture
    def fd_dict(self):
        return {
            "Guzzanti": "Corrado", 
            "Hicks": "Bill", 
            self.frozendict_class({1: 2}): "frozen"
        }

    @pytest.fixture
    def fd_dict_hole(self, fd_dict):
        new_dict = fd_dict.copy()
        del new_dict["Guzzanti"]
        return new_dict

    @pytest.fixture
    def fd_dict_eq(self):
        return {
            "Hicks": "Bill", 
            "Guzzanti": "Corrado", 
            self.frozendict_class({1: 2}): "frozen"
        }

    @pytest.fixture
    def fd_dict_2(self):
        return {
            "Guzzanti": "Corrado", 
            "Hicks": "Bill", 
            "frozen": self.frozendict_class({1: 2})
        }

    @pytest.fixture
    def fd_dict_sabina(self):
        return {'Corrado': 'Guzzanti', 'Sabina': 'Guzzanti'}

    @pytest.fixture
    def generator_seq2(self, fd_dict):
        seq2 = list(fd_dict.items())
        seq2.append(("Guzzanti", "Mario"))
        return (x for x in seq2)

    ##########################################################################
    # frozendict fixtures

    @pytest.fixture
    def fd(self, fd_dict):
        return self.frozendict_class(fd_dict)

    @pytest.fixture
    def fd_hole(self, fd_dict_hole):
        return self.frozendict_class(fd_dict_hole)

    @pytest.fixture
    def fd_unhashable(self):
        return self.frozendict_class({1: []})

    @pytest.fixture
    def fd_eq(self, fd_dict_eq):
        return self.frozendict_class(fd_dict_eq)
    
    @pytest.fixture
    def fd2(self, fd_dict_2):
        return self.frozendict_class(fd_dict_2)

    @pytest.fixture
    def fd_sabina(self, fd_dict_sabina):
        return self.frozendict_class(fd_dict_sabina)

    @pytest.fixture
    def fd_items(self, fd_dict):
        return tuple(fd_dict.items())

    @pytest.fixture
    def fd_empty(self):
        return self.frozendict_class()

    @pytest.fixture
    def module_prefix(self):
        if self.is_subclass:
            return ""
        
        return "frozendict."
    
