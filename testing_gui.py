import tkinter as tk
import tkinter.filedialog as fd
import os
from tree_view import *
from typing import Protocol

class FileChooseList:

    def __init__(self, root, btn_get_callback):
        self.lb_frame = tk.Frame(master=root)
        self.btn_frame = tk.Frame(master=root)
        self.file_lb = tk.Listbox(self.lb_frame, height= 40, width=100, selectmode= "extended")
        self.b = tk.Button(self.btn_frame, text = "get items", command = btn_get_callback)
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

    def process_selected_functions(self):
        ...

class mainviev:
    
    def setup(self, controller : rev_controller):
        self.ctl = controller
        self.root = tk.Tk()
        file_frame = tk.Frame(self.root)
        self.file_selector = FileChooseList(file_frame, self.ctl.process_selected_files)
        function_frame = tk.Frame(self.root)
        self.function_selector = FileFunctionWIndows(function_frame, self.ctl.process_selected_functions)
        function_frame.pack(side=tk.RIGHT)
        file_frame.pack(side=tk.LEFT)

    def get_selected_files(self):
        return self.file_selector.get_files()

    def get_selected_functions(self):
        return self.function_selector.get_functions()
    
    def add_file(self, filename):
        self.function_selector.add_file(filename)

    def add_function(self, filename, function_name, begin, end, rets = []):
        self.function_selector.add_function(filename, function_name, begin, end, rets)

    def start(self):
        self.root.mainloop()
