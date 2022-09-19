from tkinter import *
from tkinter import ttk
import logging
from Views import ProcessViews, RecipiesViews, StorageViews, OrderViews


class MyButton(Button):
    """
    Perrašo default Button klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            bg="white",
            fg="black",
            font=("courier", 12, "bold"),
            relief="groove",
            height=3,
            width=15,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )


class MyLabel(Label):
    """
    Perrašo default Label klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(font=("courier", 14, "bold"))


class MyEntry(Entry):
    """
    Perrašo default Entry klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(font=("courier", 14, "bold"), width=15)


class Main(ProcessViews, RecipiesViews, StorageViews, OrderViews):
    """
    Pagrindinis programos langas
    """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.style = ttk.Style()
        self.style.theme_use("clam")

        logging.basicConfig(
            filename="Project_error_log.log",
            level=logging.WARNING,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="UTF-8",
        )

        self.gradient_step = 0
        self.hex_step = 400
        for _ in range(40):
            color_hex = str(224499 + self.hex_step)
            Frame(master, width=100, height=550, bg="#" + color_hex).place(
                x=self.gradient_step, y=0
            )
            self.gradient_step += 100
            self.hex_step += 300

        self.idForEdit = IntVar()

        self.topFrame = Frame(master)
        self.leftFrame = Frame(master)

        self.menu = Menu(master)
        self.master.config(menu=self.menu)
        self.submenu = Menu(self.menu, tearoff=False)

        self.buttonAddOrder = Button(
            self.topFrame,
            text="Add an Order",
            height=3,
            width=20,
            anchor=CENTER,
            bg="white",
            fg="black",
            font=("courier", 20, "bold"),
            relief="groove",
            command=self.order_adding_widgets,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )
        self.buttonProcesses = MyButton(
            self.leftFrame, text="Processes", command=self.fill_process_data_box
        )
        self.buttonRecipies = MyButton(
            self.leftFrame, text="Recipies", command=self.fill_recipe_data_box
        )
        self.buttonStorage = MyButton(
            self.leftFrame, text="Storage", command=self.fill_storage_data_box
        )
        self.buttonEdit = MyButton(self.leftFrame, text="Edit")
        self.buttonDelete = Button(
            self.leftFrame,
            text="Delete",
            bg="red",
            fg="black",
            font=("courier", 12),
            height=3,
            width=15,
            command=self.delete_record,
        )
        self.buttonAddRecipe = MyButton(
            self.leftFrame, text="Add Recipe", command=self.add_record_recipies
        )
        self.buttonCancelEditing = MyButton(
            self.leftFrame, text="Cancel", command=self.cancel_editing
        )
        self.buttonCancelOrder = Button(
            self.topFrame,
            text="Cancel Order",
            height=3,
            width=20,
            anchor=CENTER,
            bg="red",
            fg="black",
            font=("courier", 14, "bold"),
            relief="groove",
            command=self.cancel_order,
        )
        self.buttonConfirmOrder = Button(
            self.topFrame,
            text="Confirm Order",
            height=3,
            width=20,
            anchor=CENTER,
            bg="white",
            fg="black",
            font=("courier", 14, "bold"),
            relief="groove",
            command=self.order_calculation,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )
        self.labelEdit1 = MyLabel(self.leftFrame)
        self.labelEdit2 = MyLabel(self.leftFrame)
        self.labelEdit3 = MyLabel(self.leftFrame)
        self.labelEdit4 = MyLabel(self.leftFrame)
        self.labelEdit5 = MyLabel(self.leftFrame)
        self.labelEdit6 = MyLabel(self.leftFrame)
        self.labelOrder = Label(
            self.topFrame, text="Amount in kg:", font=("courier", 25, "bold"), width=15
        )
        self.entryFieldEdit1 = MyEntry(self.leftFrame)
        self.entryFieldEdit2 = MyEntry(self.leftFrame)
        self.entryFieldEdit3 = MyEntry(self.leftFrame)
        self.entryFieldEdit4 = MyEntry(self.leftFrame)
        self.entryFieldEdit5 = MyEntry(self.leftFrame)
        self.entryFieldEdit6 = MyEntry(self.leftFrame)
        self.entryFieldOrder = Entry(
            self.topFrame, font=("courier", 25, "bold"), width=15
        )
        self.recipe_list = ttk.Combobox(
            self.topFrame, width=12, font=("courier", 25, "bold"), state="readonly"
        )
        self.processTable = ttk.Treeview(
            self.leftFrame,
            columns=("id", "Process", "Material", "Efficiency kg/h"),
            show="headings",
            height=8,
        )
        self.recipeTable = ttk.Treeview(
            self.leftFrame,
            columns=(
                "id",
                "Recipe",
                "Material 1",
                "Material 2",
                "Material 3",
                "Material 4",
                "Material 5",
            ),
            show="headings",
            height=8,
        )
        self.storageTable = ttk.Treeview(
            self.leftFrame,
            columns=("id", "Name", "Amount kg"),
            show="headings",
            height=8,
        )

        self.menu.add_cascade(label="Menu", menu=self.submenu)
        self.submenu.add_command(label="Back to main", command=self.back_to_main)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=master.destroy)

        self.buttonAddOrder.grid(row=0, column=0)
        self.buttonProcesses.grid(row=1, column=1)
        self.buttonRecipies.grid(row=2, column=1)
        self.buttonStorage.grid(row=3, column=1)
        self.topFrame.pack(side=TOP, expand=True)
        self.leftFrame.pack(side=LEFT)

    def default_button_layouts(self):
        """
        Atstato pradinius mygtukų išdėstymus, išvalo EDIT laukus
        """
        self.buttonEdit.grid(row=1, column=6)
        self.buttonDelete.grid(row=2, column=6)
        self.buttonDelete.config(state=DISABLED, bg="gray")
        self.cancel_editing()

    def cancel_editing(self):
        """
        Pašalina visus Edit langus ir juos išvalo
        """
        self.entryFieldEdit1.grid_forget()
        self.entryFieldEdit2.grid_forget()
        self.entryFieldEdit3.grid_forget()
        self.entryFieldEdit4.grid_forget()
        self.entryFieldEdit5.grid_forget()
        self.entryFieldEdit6.grid_forget()
        self.labelEdit1.grid_forget()
        self.labelEdit2.grid_forget()
        self.labelEdit3.grid_forget()
        self.labelEdit4.grid_forget()
        self.labelEdit5.grid_forget()
        self.labelEdit6.grid_forget()
        self.buttonCancelEditing.grid_forget()
        self.reset_entry_fields()
        self.buttonDelete.config(state=DISABLED, bg="gray")

    def forget_tables(self):
        """Pašalina visas duomenų lenteles"""
        self.processTable.grid_forget()
        self.recipeTable.grid_forget()
        self.storageTable.grid_forget()

    def reset_entry_fields(self):
        """
        Išvalo visus Edit įrašų laukus
        """
        self.entryFieldEdit1.delete(0, END)
        self.entryFieldEdit2.delete(0, END)
        self.entryFieldEdit3.delete(0, END)
        self.entryFieldEdit4.delete(0, END)
        self.entryFieldEdit5.delete(0, END)
        self.entryFieldEdit6.delete(0, END)
        self.entryFieldEdit1.focus()

    def back_to_main(self):
        """
        Grąžina programą į pradinę būseną
        """
        self.default_button_layouts()
        self.forget_tables()
        self.cancel_order()
        self.buttonEdit.grid_forget()
        self.buttonDelete.grid_forget()
        self.buttonCancelEditing.grid_forget()
        self.buttonAddRecipe.grid_forget()


def main():
    window = Tk()
    Main(window)
    window.geometry("1570x550+400+400")
    window.resizable(False, False)
    window.title("Control panel")
    window.mainloop()


if __name__ == "__main__":
    main()
