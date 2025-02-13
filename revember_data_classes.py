from dataclasses import*

@dataclass
class FunctObject:
    name : str
    begin : int
    returns : list
    end : int