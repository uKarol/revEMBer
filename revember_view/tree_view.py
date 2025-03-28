from tkinter import Tk, Button, ttk
from revember_view.view_data_classes import *

class FileFunctionWIndows:

    def __init__(self, root, get_selected_callback, btn_text):
        self.tree = ttk.Treeview(root, height= 30)
        
        self.tree.pack(expand=True, fill="both")
        self.id_ctr = 0
        button_del = Button(root, text=btn_text, command=get_selected_callback)
        button_del.pack()
        self.tree.bind("<Delete>", self.delete_evt)

    def get_functions(self):
        children = self.tree.get_children()
        ret_val = {}
        for child in children:
            ret_val.update({child: []})
            funcs = self.tree.get_children(child)
            for fun in funcs:
                ret_val[child].append(View_FunctObject(self.tree.item(fun)["text"]))    
        return ret_val  


    def add_file(self, filename):
        self.tree.insert("" , "end", filename ,text=filename)

    def add_function(self, filename, function_name, begin, end, rets = []):
        self.tree.insert(filename, "end", self.id_ctr, text=function_name)

        self.tree.insert(self.id_ctr, "end", filename+function_name+str(0), text=f"begin {begin}")
        self.tree.insert(self.id_ctr, "end", filename+function_name+str(1), text=f"end {end}")
        sub_ctr = 2
        for ret in rets:
            self.tree.insert(self.id_ctr, "end", filename+function_name+str(sub_ctr), text=f"return {ret}")
            sub_ctr = sub_ctr + 1

        self.id_ctr = self.id_ctr + 1

    def delete_evt(self, evt):
        self.delete()

    def delete(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def del_all_functions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)