class AttrDict:
    """
    A special object that sets its __dict__ to the passed dict.
    Allows getattr instead of getitem for easier code writing.
    """
    def __init__(self, d: dict):
        # recursively turn all nested dicts inside to AttrDict s
        self.__dict__ = {k: AttrDict(v) if isinstance(v, dict) else v for k, v in d.items()}

    def __repr__(self): return repr(self.__dict__)

    def __str__(self): return str(self.__dict__)
