# Filename: revEMBer_view.py
# Author: Karol Ujda (uKarol)
# Description: Grafical user inferface of revEMBer

import tkinter as tk
import tkinter.filedialog as fd
import os
from revember_view.tree_view import FileFunctionWIndows
from typing import Protocol

class FileChooseList:

    def __init__(self, root, btn_get_callback):
        self.lb_frame = tk.Frame(master=root)
        self.btn_frame = tk.Frame(master=root)
        self.file_lb = tk.Listbox(self.lb_frame, height= 40, width=100, selectmode= "extended")
        self.b = tk.Button(self.btn_frame, text = "FIND FUNCTIONS IN SELECTED FILES", command = btn_get_callback)
        self.dir_btn = tk.Button(self.btn_frame, text= "add directory", command= self.add_dir)
        self.file_btn = tk.Button(self.btn_frame, text= "add file", command= self.add_files)
        self.b.pack(side=tk.LEFT)
        self.file_btn.pack(side=tk.LEFT)
        self.dir_btn.pack(side=tk.RIGHT)
        self.file_lb.pack()
        self.lb_frame.pack()
        self.btn_frame.pack()
        
        self.file_lb.bind('<Delete>', func = self.delete_on_key)
        self.current_idx = 0

    def add_dir(self):
        dirname = fd.askdirectory(title='Choose a file')
        print(dirname)
        for (root, dirs, file) in os.walk(dirname):
            for f in file:
                if f.strip().endswith(".c"):
                    self.add_item(root + '/' + f)

    def add_files(self):
        files = fd.askopenfilenames(title='Choose a file')
        print(files)
        for file in files:
            self.add_item(file)

    def add_item(self, item):
        self.file_lb.insert(self.current_idx, item)
        self.current_idx = self.current_idx + 1

    def get_files(self):
        return self.file_lb.get(0, tk.END)

    def delete_on_key(self, evt):
        self.delete()

    def delete(self):
        selections = self.file_lb.curselection()
        for selection in selections: 
            self.file_lb.delete(selection)
            self.current_idx = self.current_idx - 1

class rev_controller(Protocol):
    def process_selected_files(self):
        ...

    def add_debug_functions(self):
        ...

    def remove_debug_functions(self):
        ...
class user_functions:

    def __init__(self, root):
        self.check_var_beg = tk.BooleanVar()
        self.check_var_ret = tk.BooleanVar()
        self.check_var_end = tk.BooleanVar()
        self.check_var_param = tk.BooleanVar()
        frame_beg = tk.Frame(master=root)
        frame_ret = tk.Frame(master=root)
        frame_ext = tk.Frame(master=root)
        frame_param = tk.Frame(master=root)
        user_desc = tk.Label(master=frame_beg, text="TO BE LOGGED")
        user_desc.pack()

        self.user_function_begin_Checkbox = tk.Checkbutton(master=frame_beg, variable= self.check_var_beg, text="function begin")
        self.user_function_begin_Checkbox.select()
        self.user_function_return_Checkbox = tk.Checkbutton(master=frame_ret, variable= self.check_var_ret, text = "function return")
        self.user_function_return_Checkbox.select()
        self.user_function_end_Checkbox = tk.Checkbutton(master=frame_ext, variable= self.check_var_end, text="function end")
        self.user_function_end_Checkbox.select()
        self.user_function_param_Checkbox = tk.Checkbutton(master=frame_param, variable= self.check_var_param, text="function params")


        self.user_function_begin_Checkbox.pack(side=tk.LEFT)
        self.user_function_return_Checkbox.pack(side=tk.LEFT)
        self.user_function_end_Checkbox.pack(side=tk.LEFT)
        self.user_function_param_Checkbox.pack(side=tk.LEFT)

        frame_beg.pack()
        frame_ret.pack()
        frame_ext.pack()
        frame_param.pack()

    def get_user_functions(self):
        user_begin = self.check_var_beg.get()
        user_return = self.check_var_ret.get()
        user_end = self.check_var_end.get()
        user_param = self.check_var_param.get()
        return {"begin" : user_begin, "ret" : user_return, "end" : user_end, "param" : user_param}

class revEMBer_view:
    
    def setup(self, controller : rev_controller):
        self.ctl = controller
        self.root = tk.Tk()
        self.root.title("revEMBer")
        file_frame = tk.Frame(self.root)
        self.file_selector = FileChooseList(file_frame, self.ctl.process_selected_files)
        function_frame = tk.Frame(self.root)
        self.function_selector = FileFunctionWIndows(function_frame, self.ctl.add_debug_functions, "APPLY TO SELECTED FUNCTIONS")
        function_frame.pack(side=tk.RIGHT, expand=True, fill="x")
        file_frame.pack(side=tk.LEFT)


        function_frame2 = tk.Frame(self.root)
        self.function_selector2 = FileFunctionWIndows(function_frame2, self.ctl.remove_debug_functions, "REMOVE FROM SELECTED FUNCTIONS")
        function_frame2.pack(side=tk.RIGHT, expand=True, fill="x")
        
        user_function_frame = tk.Frame(self.root)
        self.user_functions_getter = user_functions(user_function_frame) 
        user_function_frame.pack()

    def get_user_functions(self):
        return self.user_functions_getter.get_user_functions()

    def get_selected_files(self):
        return self.file_selector.get_files()
    
    def get_selected_functions(self):
        return self.function_selector.get_functions()

    def get_selected_functions_del(self):
        return self.function_selector2.get_functions()
    
    def add_file(self, filename):
        self.function_selector.add_file(filename)

    def add_function(self, filename, function_name, begin, end, rets = []):
        self.function_selector.add_function(filename, function_name, begin, end, rets)

    def add_file_unclear(self, filename):
        self.function_selector2.add_file(filename)

    def add_function_unclear(self, filename, function_name, begin, end, rets = []):
        self.function_selector2.add_function(filename, function_name, begin, end, rets)

    def del_all_functions(self):
        self.function_selector2.del_all_functions()
        self.function_selector.del_all_functions()

    def start(self):
        self.root.mainloop()
