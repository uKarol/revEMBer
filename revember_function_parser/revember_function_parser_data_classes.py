from dataclasses import*

@dataclass
class FunctionParser_FunctObject:
    name : str
    parameters : list
    begin : int
    end : int


#warnings line, warning_text
#returns line_begin, line_end, stray
@dataclass
class FunctionParser_FunctDetails:
    returns : list
    warnings : list
    revember_artifacts : list 

@dataclass
class FUnctionParser_FunctData:
    name : str
    parameters : list
    begin : int
    end : int
    returns : list
    warnings : list
    revember_artifacts : list 