pattern1 = 'void pattern1 (int x, int y) {std::cout<<"pattern1";}'

pattern2 = 'void pattern2(int x, int y){std::cout<<"pattern2";'

pattern3 = 'void pattern3(int x, int y){'

x = pattern1.split( '(' )

pattern4 = 'void pattern5(int x, int y)'

str1 = ["void (*fpData)(void);",
"int  (*fpData)(int);",
"int dupa[5] = {",
"struct dupa{",
"int  (*fpData)(char *) { to_nie_dziala(); ",
"int* (*fpData)(char *);",
"int  (*fpData)(int, char *);",
"int* (*fpData)(int, int *, char *);",
"int* (*fpData)(int , char, int (*paIndex)[3]);",
"int* (*fpData)(int , int (*paIndex)[3] , int (* fpMsg) (const char *));",
"int* (*fpData)(int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *));",
"int* (*fpData[2])(int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *)) { }",
"int* (*(*fpData)(const char *))(int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *)) { x++; }",
]

SUCCESS = 0
INCOMPLETE = 1
FAILURE = 2

class cascased_split:

    def __init__(self):
        self.stage = 0
        self.splitt_str = ['{', '}']
        self.fun_list = ['','','','']
        self.unallowed_words_in_stage = [ ['=',';'],[], [] ]
        self.last_result = []

    def stage_0_validate(self):
        signature = self.fun_list[0]
        if( len(signature) > 0) and ('(' in signature) and ( ')' in signature ):
            return True
        else:
            return False 

    def reset_variables(self):
        self.fun_list = ['','','','']
        self.stage = 0

    def add_val(self, new_val):
        to_be_added = self.fun_list[self.stage]
        new_val = to_be_added + new_val
        self.fun_list[self.stage] = new_val
    
    def validate_stage(self, current_stage):
        if self.stage == 0:
            return self.stage_0_validate()
        else: 
            return True

    def validate_token(self, token):
        ret_val = True
        if( any(wrd in token for wrd in self.unallowed_words_in_stage[self.stage]) ):
            ret_val = False
            self.reset_variables()
        return ret_val
    
    def get_function_signature(self):
        return self.last_result[0]

    def c_splitter(self, line):

        to_be_added: str
        next_token = "test"
        state_transition = False
        while(len(next_token) > 0):

            if(self.splitt_str[self.stage] in line):
                splitted = line.split(self.splitt_str[self.stage]) 
                to_be_added = splitted[0]
                next_token = splitted[1]
                state_transition = True
            else:
                to_be_added = line
                state_transition = False

            if self.validate_token(to_be_added) == True:
                self.add_val(to_be_added)
            else:
                self.reset_variables()
                return FAILURE 

            if(state_transition == True):
                if(self.validate_stage(self.fun_list[self.stage]) == True):
                    self.stage = self.stage + 1
                    if(self.stage == len(self.splitt_str)):
                        self.last_result = self.fun_list
                        self.reset_variables()
                        return SUCCESS
                    else:
                        line = next_token
                else:
                    self.reset_variables()
                    return FAILURE
            else:
                return INCOMPLETE    

                
def test():

    spt = cascased_split()
    spt.c_splitter(pattern1)
    print(spt.get_function_signature())
    spt.reset_variables()

    spt.c_splitter('void ')
    spt.c_splitter('dupa')
    spt.c_splitter('(')
    spt.c_splitter('int x')
    spt.c_splitter('int y)')
    spt.c_splitter('')
    spt.c_splitter('{ xd;')
    spt.c_splitter('}')
    print(spt.get_function_signature())
    print("cascaded splitter end")
    print("")


    for s in str1:
        if spt.c_splitter(s) == SUCCESS:
            print(spt.get_function_signature())
            print("")