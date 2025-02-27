from detector import *
import tkinter as tk
from file_manip import *
 
class function_list():

    def function_list_setup(self, frame):
        # Create a listbox
        self.listbox = tk.Listbox(frame, width=80, height=20, selectmode=tk.MULTIPLE)
        self.listbox.pack(expand=1, fill=tk.BOTH)
    
    def select_all(self):
        self.listbox.select_set(0, tk.END)

    def deselect_all(self):
        self.listbox.select_clear(0, tk.END)

    def setup_buttons(self, frame, callback):
        tk.Button(frame, text='select all', command=self.select_all).pack(side=tk.LEFT)
        tk.Button(frame, text='deselect all', command=self.deselect_all).pack(side=tk.RIGHT)
        btn = tk.Button(frame, text='Get Selected', command=callback)
        # Placing the button and listbox
        btn.pack(side=tk.RIGHT)

    def __init__(self, root, get_sel_callback):
        self.idx = 0
        self.root = root
        self.list_frame = tk.Frame(self.root)
        self.btn_frame = tk.Frame(self.root)
        self.function_list_setup(self.list_frame)
        self.setup_buttons(self.btn_frame, get_sel_callback)
        self.list_frame.pack(expand=1)
        self.btn_frame.pack(expand=1)

    def add_list_item(self, item):
        self.listbox.insert(self.idx, item)
        self.idx = self.idx + 1


    # Function for printing the
    # selected listbox value(s)
    def get_selected_item(self):
        ret_val = []
        # Traverse the tuple returned by
        # curselection method and print
        # corresponding value(s) in the listbox
        for i in self.listbox.curselection():
            #print(self.listbox.get(i))
            ret_val.append(self.listbox.get(i))
        #print(ret_val)
        return ret_val
    
class control_panel:
    
    def setup_ctl_panel(self):
        # Create a button widget and
        # map the command parameter to
        # selected_item function
        pass
        #listbox.pack()

    def __init__(self, root, controller):
        self.ctl = controller
        self.control_frame = tk.Frame(root)
        self.setup_ctl_panel()
        self.control_frame.pack()

class revember_view_tk:
    # Create the root window
    def setup(self, controller):    
        self.root = tk.Tk(screenName= "revEMBer")
        self.ctl = controller
        self.root.geometry('380x500')
        self.rvlistbox = function_list(self.root, controller.get_selected_items)
        #self.ctl_panel = control_panel(self.root, controller)

    def add_item(self, item):
        self.rvlistbox.add_list_item(item)

    def start(self):
        self.root.mainloop()

    def get_selected_item(self):
        return self.rvlistbox.get_selected_item()

class experimental_controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.setup(self)
        self.func_finder = cascaded_function_finder()
        self.current_file = ""
        self.found_functions = {}

    def get_selected_items(self):
        items = self.view.get_selected_item()
        temp_dict = {}
        for item in items:
            temp_dict.update({item : self.found_functions[item]})
        fman = CFileManip()
        fman.add_dbg_functions(self.current_file, temp_dict)

    def search_file(self, path):
        self.current_file = path
        self.func_finder.search_file(path)
        self.found_functions = self.func_finder.get_found_functions()
        for ffunction in self.found_functions:
            self.view.add_item(ffunction)

    def start_app(self):
        self.view.start()


my_view = revember_view_tk()

revember_ctl = experimental_controller(None, my_view)

revember_ctl.search_file("stm32g4xx_hal_cortex.c")

revember_ctl.start_app()
