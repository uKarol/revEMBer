from tkinter import Tk, Button, ttk


class FileFunctionWIndows:

    def __init__(self, root, get_selected_callback):
        self.tree = ttk.Treeview(root, height= 30)
        self.tree["columns"]=("begin","end", "rets")
        self.tree.column("#0", width=400)
        self.tree.column("begin", width=100)
        self.tree.column("end", width=100)
        self.tree.column("rets", width=100)
        self.tree.heading("#0", text="function name")
        self.tree.heading("begin", text="function begin")
        self.tree.heading("end", text="function end")
        self.tree.heading("rets", text="function returns")
        self.tree.pack()
        self.id_ctr = 0
        button_del = Button(root, text="APPLY TO SELECTED FUNCTIONS", command=get_selected_callback)
        button_del.pack()
        self.tree.bind("<Delete>", self.delete_evt)

    def get_functions(self):
        children = self.tree.get_children()
        ret_val = {}
        for child in children:
            ret_val.update({child: []})
            funcs = self.tree.get_children(child)
            for fun in funcs:
                ret_val[child].append(self.tree.item(fun)["text"])   
                ret_val[child].append(self.tree.item(fun)["values"])   
        return ret_val  


    def add_file(self, filename):
        self.tree.insert("" , "end", filename ,text=filename, values=("",""))

    def add_function(self, filename, function_name, begin, end, rets = []):
        self.tree.insert(filename, "end", self.id_ctr, text=function_name, values=(begin, end, rets))
        self.id_ctr = self.id_ctr + 1

    def delete_evt(self, evt):
        self.delete()

    def delete(self):
        for item in self.tree.selection():
            self.tree.delete(item)
