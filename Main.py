import tkinter as tk
from tkinter import ttk
import logging
from Views import ProcessViews, RecipiesViews, StorageViews, OrderViews, MaterialsViews
import API
from datetime import datetime


class MyButton(tk.Button):
    """
    Perrašo default Button klasę, prideda
    spalvų pasikeitimus užvedus pelę ant
    mygtuko.
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
            activebackground="#75C1BF",
            activeforeground="#e6d415",
        )
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _e):
        self['background'] = self['activebackground']

    def on_leave(self, _e):
        self['background'] = self.defaultBackground


class MyOrderButton(tk.Button):
    """
    Perrašo default Button klasę, prideda
    spalvų pasikeitimus užvedus pelę ant
    mygtuko.
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            height=3,
            width=20,
            anchor=tk.CENTER,
            fg="black",
            font=("courier", 14, "bold"),
            relief="groove",
            activebackground="#75C1BF",
            activeforeground="#e6d415",
        )
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _e):
        self['background'] = self['activebackground']

    def on_leave(self, _e):
        self['background'] = self.defaultBackground


class MyScrollButton(tk.Button):
    """
    Perrašo default Button klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            fg="black",
            font=("courier", 12, "bold"),
            relief="groove",
            height=1,
            width=15,
            activebackground="#0a0a0a",
            activeforeground="#e6d415",
        )


class MyLabel(tk.Label):
    """
    Perrašo default Label klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(font=("courier", 14, "bold"))


class MyCombobox(ttk.Combobox):
    """
    Perrašo default Combobox klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(width=10, font=("courier", 15, "bold"), state="readonly")


class MyEntry(tk.Entry):
    """
    Perrašo default Entry klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(font=("courier", 14, "bold"), width=14)


class MyTreeview(ttk.Treeview):
    """
    Perrašo default Treeview klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            show="headings",
            height=8,
            selectmode="browse",
        )


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
            tk.Frame(master, width=100, height=550, bg="#" + self.color_hex).place(
                x=self.gradient_step, y=0
            )
            self.gradient_step += 100
            self.hex_step += 300

        self.idForEdit = tk.IntVar()

        self.rates = API.get_rates()

        self.topFrame = tk.Frame(master)
        self.leftFrame = tk.Frame(master)

        self.menu = tk.Menu(master)
        self.master.config(menu=self.menu)
        self.submenu = tk.Menu(self.menu, tearoff=False)

        self.buttonAddOrder = tk.Button(
            self.master,
            text="Add an Order",
            height=3,
            width=20,
            anchor=tk.CENTER,
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
        self.buttonDelete = tk.Button(
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
        self.buttonFilterOrders = MyButton(
            self.leftFrame, text="Filter", command=self.filter_orders_buttons
        )
        self.buttonCancelOrder = MyOrderButton(
            self.master,
            text="Cancel Order",
            bg="red",
            command=self.cancel_order,
        )
        self.buttonConfirmOrder = MyOrderButton(
            self.master,
            text="Confirm Order",
            bg="white",
            command=self.recipe_calculation,
        )
        self.buttonScrollUp = MyScrollButton(
            self.master,
            bg="gray",
            text="↑↑↑",
            command="",
            state=tk.DISABLED,
        )
        self.buttonScrollDown = MyScrollButton(
            self.master,
            bg="white",
            text="↓↓↓",
            command=self.scroll_down_1,
        )
        self.labelEdit1 = MyLabel(self.leftFrame)
        self.labelEdit2 = MyLabel(self.leftFrame)
        self.labelEdit3 = MyLabel(self.leftFrame)
        self.labelEdit4 = MyLabel(self.leftFrame)
        self.labelEdit5 = MyLabel(self.leftFrame)
        self.labelEdit6 = MyLabel(self.leftFrame)
        self.labelOrderProfit1 = MyLabel(self.leftFrame, text="Period profit:")
        self.labelOrderProfit2 = MyLabel(self.leftFrame)
        self.labelOrder = tk.Label(
            self.master, text="Amount in kg:", font=("courier", 25, "bold"), width=15
        )
        self.labelRecipe = tk.Label(
            self.master, text="Recipe:", font=("courier", 25, "bold"), width=13
        )
        self.labelFilterFrom = tk.Label(
            self.master, text="From:", font=("courier", 18, "bold"), width=13
        )
        self.labelFilterTo = tk.Label(
            self.master, text="To:", font=("courier", 18, "bold"), width=13
        )
        self.labelMailOrder = tk.Label(
            self.master, text="Mail orders:", font=("courier", 24, "bold"), width=13
        )

        self.entryFieldEdit1 = MyEntry(self.leftFrame)
        self.entryFieldEdit2 = MyEntry(self.leftFrame)
        self.entryFieldEdit3 = MyEntry(self.leftFrame)
        self.entryFieldEdit4 = MyEntry(self.leftFrame)
        self.entryFieldEdit5 = MyEntry(self.leftFrame)
        self.entryFieldEdit6 = MyEntry(self.leftFrame)
        self.entryFieldOrder = tk.Entry(
            self.master, font=("courier", 25, "bold"), width=15
        )

        self.recipe_list = ttk.Combobox(
            self.master, width=12, font=("courier", 25, "bold"), state="readonly"
        )
        self.currency_list = ttk.Combobox(
            self.master,
            width=6,
            font=("courier", 25, "bold"),
            state="readonly",
            values=API.PAIRS,
        )
        self.currency_list.set("EUR")
        self.mail_list = ttk.Combobox(
            self.master,
            values=["YES", "NO"],
            width=4,
            font=("courier", 25, "bold"),
            state="readonly",
        )
        self.mail_list.set("YES")
        self.year_list_from = MyCombobox(
            self.leftFrame, values=["2022", "2023", "2024", "2025"]
        )
        self.month_list_from = MyCombobox(
            self.leftFrame,
            values=["0" + str(i) if len(str(i)) <= 1 else str(i) for i in range(1, 13)],
        )
        self.day_list_from = MyCombobox(
            self.leftFrame, values=[str(i) for i in range(1, 32)]
        )
        self.year_list_to = MyCombobox(
            self.leftFrame, values=["2022", "2023", "2024", "2025"]
        )
        self.month_list_to = MyCombobox(
            self.leftFrame,
            values=["0" + str(i) if len(str(i)) <= 1 else str(i) for i in range(1, 13)],
        )
        self.day_list_to = MyCombobox(
            self.leftFrame, values=[str(i) for i in range(1, 32)]
        )
        self.year_list_from.set("2022")
        self.month_list_from.set("01")
        self.day_list_from.set("1")
        self.year_list_to.set(str(datetime.now().year))
        self.month_list_to.set(str(datetime.now().month))
        self.day_list_to.set(str(datetime.now().day))

        self.processTable = MyTreeview(
            self.leftFrame, columns=("id", "Process", "Material", "Efficiency kg/h")
        )
        self.recipeTable = MyTreeview(
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
        )
        self.storageTable = MyTreeview(
            self.leftFrame, columns=("id", "Name", "Amount kg")
        )
        self.ordersTable = MyTreeview(
            self.leftFrame,
            columns=(
                "id",
                "Date",
                "Recipe",
                "Amount",
                "Manufacturing Cost",
                "Selling price",
            ),
        )
        self.materialsTable = MyTreeview(
            self.leftFrame, columns=("id", "Name", "Price")
        )

        self.scrollbar_recipe = tk.Scrollbar(
            self.recipeTable, orient=tk.VERTICAL, command=self.recipeTable.yview
        )

        self.menu.add_cascade(label="Menu", menu=self.submenu)
        self.submenu.add_command(label="Back to main", command=self.back_to_main)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=master.destroy)

        self.currency_list.place(x=0, y=130)
        self.mail_list.place(x=1470, y=0)
        self.labelMailOrder.place(x=1230, y=0)
        self.buttonScrollUp.place(x=0, y=282)
        self.buttonScrollDown.place(x=0, y=314)
        self.buttonAddOrder.place(x=585, y=130)
        self.buttonMenu1.grid(row=1, column=1)
        self.buttonMenu2.grid(row=2, column=1)
        self.buttonMenu3.grid(row=3, column=1)
        self.topFrame.pack(side=tk.TOP, expand=True)
        self.leftFrame.pack(side=tk.LEFT)

    def default_button_layouts(self):
        """
        Atstato pradinius mygtukų išdėstymus, išvalo EDIT laukus
        """
        self.buttonEdit.grid(row=1, column=6)
        self.buttonDelete.grid(row=2, column=6)
        self.buttonDelete.config(state=tk.DISABLED, bg="gray")
        self.buttonEdit.config(state=tk.NORMAL, bg="white", text="Edit", activebackground="#75C1BF")
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
        self.labelFilterFrom.place_forget()
        self.labelFilterTo.place_forget()
        self.year_list_from.grid_forget()
        self.month_list_from.grid_forget()
        self.day_list_from.grid_forget()
        self.year_list_to.grid_forget()
        self.month_list_to.grid_forget()
        self.day_list_to.grid_forget()
        self.buttonCancelEditing.grid_forget()
        self.buttonFilterOrders.grid_forget()
        self.labelOrderProfit1.grid_forget()
        self.labelOrderProfit2.grid_forget()
        self.reset_entry_fields()
        self.buttonDelete.config(state=tk.DISABLED, bg="gray")

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
        self.entryFieldEdit1.delete(0, tk.END)
        self.entryFieldEdit2.delete(0, tk.END)
        self.entryFieldEdit3.delete(0, tk.END)
        self.entryFieldEdit4.delete(0, tk.END)
        self.entryFieldEdit5.delete(0, tk.END)
        self.entryFieldEdit6.delete(0, tk.END)
        self.year_list_from.set("2022")
        self.month_list_from.set("01")
        self.day_list_from.set("1")
        self.year_list_to.set(str(datetime.now().year))
        self.month_list_to.set(str(datetime.now().month))
        self.day_list_to.set(str(datetime.now().day))
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
        self.buttonScrollUp.config(state=tk.DISABLED, bg="gray")
        self.buttonScrollDown.config(
            command=self.scroll_down_1, state=tk.NORMAL, bg="white"
        )
        self.buttonEdit.grid_forget()
        self.buttonDelete.grid_forget()
        self.buttonCancelEditing.grid_forget()
        self.buttonAddRecipe.grid_forget()

    def scroll_down_1(self):
        """
        Scrollina menu žemyn iš pradinės būsenos
        """
        self.buttonMenu1.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu2.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu3.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonScrollDown.config(command=self.scroll_down_2)
        self.buttonScrollUp.config(command=self.scroll_up_1, state=tk.NORMAL, bg="white")

    def scroll_down_2(self):
        """
        Scrollina menu žemyn iš antros nuo viršaus būsenos
        """
        self.buttonMenu1.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu2.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonMenu3.config(text="Orders", command=self.fill_orders_data_box)
        self.buttonScrollDown.config(state=tk.DISABLED, bg="gray")
        self.buttonScrollUp.config(command=self.scroll_up_2)

    def scroll_up_1(self):
        """
        Scrollina menu aukštyn iš antros nuo apačios būsenos
        """
        self.buttonMenu1.config(text="Process", command=self.fill_process_data_box)
        self.buttonMenu2.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu3.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonScrollUp.config(state=tk.DISABLED, bg="gray")
        self.buttonScrollDown.config(command=self.scroll_down_1)

    def scroll_up_2(self):
        """
        Scrollina menu aukštyn iš žemutinės būsenos
        """
        self.buttonMenu1.config(text="Recipies", command=self.fill_recipe_data_box)
        self.buttonMenu2.config(text="Storage", command=self.fill_storage_data_box)
        self.buttonMenu3.config(text="Materials", command=self.fill_materials_data_box)
        self.buttonScrollUp.config(command=self.scroll_up_1, state=tk.NORMAL, bg="white")
        self.buttonScrollDown.config(
            command=self.scroll_down_2, state=tk.NORMAL, bg="white"
        )


def main():
    window = tk.Tk()
    Main(window)
    window.geometry("1570x550+400+400")
    window.resizable(False, False)
    window.title("Control panel")
    window.mainloop()


if __name__ == "__main__":
    main()
