class AttrDict:
    """
    A special object that sets its __dict__ to the passed dict.
    Allows getattr instead of getitem for easier code writing.
    """
    def __init__(self, d):
        self.__dict__ = d
