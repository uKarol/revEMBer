from dataclasses import*

@dataclass
class FunctionParser_FunctObject:
    name : str
    begin : int
    returns : list
    end : int