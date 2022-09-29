from tkinter import *
from tkinter import ttk
import logging
from Views import ProcessViews, RecipiesViews, StorageViews, OrderViews, MaterialsViews
from API import get_rates, PAIRS


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


class Main(ProcessViews, RecipiesViews, StorageViews, OrderViews, MaterialsViews):
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
            self.color_hex = str(224499 + self.hex_step)
            Frame(master, width=100, height=550, bg="#" + self.color_hex).place(
                x=self.gradient_step, y=0
            )
            self.gradient_step += 100
            self.hex_step += 300

        self.idForEdit = IntVar()

        self.rates = get_rates()

        self.topFrame = Frame(master)
        self.leftFrame = Frame(master)

        self.menu = Menu(master)
        self.master.config(menu=self.menu)
        self.submenu = Menu(self.menu, tearoff=False)

        self.buttonAddOrder = Button(
            self.master,
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
        self.buttonMenu1 = MyButton(
            self.leftFrame, text="Processes", command=self.fill_process_data_box
        )
        self.buttonMenu2 = MyButton(
            self.leftFrame, text="Recipies", command=self.fill_recipe_data_box
        )
        self.buttonMenu3 = MyButton(
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
            self.master,
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
            self.master,
            text="Confirm Order",
            height=3,
            width=20,
            anchor=CENTER,
            bg="white",
            fg="black",
            font=("courier", 14, "bold"),
            relief="groove",
            command=self.recipe_calculation,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )
        self.buttonScrollUp = Button(
            self.master,
            bg="gray",
            fg="black",
            font=("courier", 12, "bold"),
            relief="groove",
            height=1,
            width=15,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
            text="↑↑↑",
            command="",
            state=DISABLED,
        )
        self.buttonScrollDown = Button(
            self.master,
            bg="white",
            fg="black",
            font=("courier", 12, "bold"),
            relief="groove",
            height=1,
            width=15,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
            text="↓↓↓",
            command=self.scroll_down_1,
        )
        self.labelEdit1 = MyLabel(self.leftFrame)
        self.labelEdit2 = MyLabel(self.leftFrame)
        self.labelEdit3 = MyLabel(self.leftFrame)
        self.labelEdit4 = MyLabel(self.leftFrame)
        self.labelEdit5 = MyLabel(self.leftFrame)
        self.labelEdit6 = MyLabel(self.leftFrame)
        self.labelOrder = Label(
            self.master, text="Amount in kg:", font=("courier", 25, "bold"), width=15
        )
        self.labelRecipe = Label(
            self.master, text="Recipe:", font=("courier", 25, "bold"), width=13
        )
        self.entryFieldEdit1 = MyEntry(self.leftFrame)
        self.entryFieldEdit2 = MyEntry(self.leftFrame)
        self.entryFieldEdit3 = MyEntry(self.leftFrame)
        self.entryFieldEdit4 = MyEntry(self.leftFrame)
        self.entryFieldEdit5 = MyEntry(self.leftFrame)
        self.entryFieldEdit6 = MyEntry(self.leftFrame)
        self.entryFieldOrder = Entry(
            self.master, font=("courier", 25, "bold"), width=15
        )

        self.recipe_list = ttk.Combobox(
            self.master, width=12, font=("courier", 25, "bold"), state="readonly"
        )
        self.currency_list = ttk.Combobox(
            self.master, width=6, font=("courier", 25, "bold"), state="readonly"
        )
        self.currency_list.config(values=PAIRS)
        self.currency_list.set("EUR")

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
        self.ordersTable = ttk.Treeview(
            self.leftFrame,
            columns=("id", "Date", "Recipe", "Amount", "Manufacturing Cost", "Selling price"),
            show="headings",
            height=8,
        )
        self.materialsTable = ttk.Treeview(
            self.leftFrame,
            columns=("id", "Name", "Price"),
            show="headings",
            height=8,
        )

        self.menu.add_cascade(label="Menu", menu=self.submenu)
        self.submenu.add_command(label="Back to main", command=self.back_to_main)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=master.destroy)

        self.currency_list.place(x=0, y=130)
        self.buttonScrollUp.place(x=0, y=282)
        self.buttonScrollDown.place(x=0, y=314)
        self.buttonAddOrder.place(x=585, y=130)
        self.buttonMenu1.grid(row=1, column=1)
        self.buttonMenu2.grid(row=2, column=1)
        self.buttonMenu3.grid(row=3, column=1)
        self.topFrame.pack(side=TOP, expand=True)
        self.leftFrame.pack(side=LEFT)

    def default_button_layouts(self):
        """
        Atstato pradinius mygtukų išdėstymus, išvalo EDIT laukus
        """
        self.buttonEdit.grid(row=1, column=6)
        self.buttonDelete.grid(row=2, column=6)
        self.buttonDelete.config(state=DISABLED, bg="gray")
        self.buttonEdit.config(state=NORMAL, bg="white")
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
        self.ordersTable.grid_forget()
        self.materialsTable.grid_forget()

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
        self.buttonMenu1.config(text="Process", command=self.fill_process_data_box)
        self.buttonMenu2.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu3.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonScrollUp.config(state=DISABLED, bg="gray")
        self.buttonScrollDown.config(command=self.scroll_down_1, state=NORMAL, bg="white")
        self.buttonEdit.grid_forget()
        self.buttonDelete.grid_forget()
        self.buttonCancelEditing.grid_forget()
        self.buttonAddRecipe.grid_forget()

    def color_background(self):
        for _ in range(40):
            self.color_hex = str(224499 + self.hex_step)
            Frame(self.master, width=100, height=550, bg="#" + self.color_hex).place(
                x=self.gradient_step, y=0
            )
            self.gradient_step += 100
            self.hex_step += 300

    def scroll_down_1(self):
        self.buttonMenu1.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu2.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu3.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonScrollDown.config(command=self.scroll_down_2)
        self.buttonScrollUp.config(command=self.scroll_up_1, state=NORMAL, bg="white")

    def scroll_down_2(self):
        self.buttonMenu1.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu2.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonMenu3.config(text="Orders", command=self.fill_orders_data_box)
        self.buttonScrollDown.config(state=DISABLED, bg="gray")
        self.buttonScrollUp.config(command=self.scroll_up_2)

    def scroll_up_1(self):
        self.buttonMenu1.config(text="Process", command=self.fill_process_data_box)
        self.buttonMenu2.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu3.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonScrollUp.config(state=DISABLED, bg="gray")
        self.buttonScrollDown.config(command=self.scroll_down_1)

    def scroll_up_2(self):
        self.buttonMenu1.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu2.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu3.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonScrollUp.config(command=self.scroll_up_1, state=NORMAL, bg="white")
        self.buttonScrollDown.config(command=self.scroll_down_2, state=NORMAL, bg="white")


def main():
    window = Tk()
    Main(window)
    window.geometry("1570x550+400+400")
    window.resizable(False, False)
    window.title("Control panel")
    window.mainloop()


if __name__ == "__main__":
    main()
