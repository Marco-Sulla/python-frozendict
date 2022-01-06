class F(frozendict_superclass):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

class FMissing(frozendict_superclass):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)
    
    def __missing__(self, key):
        return key

frozendict_class = F
