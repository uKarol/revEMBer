from dataclasses import*

@dataclass
class View_FunctObject:
    name : str
    begin : int
    returns : list
    end : int