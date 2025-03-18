from dataclasses import*

@dataclass
class FunctionParser_FunctObject:
    name : str
    begin : int
    returns : list
    #parameters : list
    #revember_artifacts : list
    #single_returns : list
    end : int