from utils import *
from API import get_rates


class MaterialsViews:
    def __init__(self):
        self.rates = get_rates()

    def fill_materials_data_box(self):
        """
        Atstato pradinę lango būseną su Materials duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.materialsTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.materialsTable.get_children():
            self.materialsTable.delete(i)
        for i, col_heading in enumerate(
            ["ID", "Name", "Price"], 1
        ):
            self.materialsTable.column(f"# {i}", anchor=tk.CENTER, width=90)
            self.materialsTable.heading(f"# {i}", text=col_heading)
        self.currency_list.bind('<<ComboboxSelected>>', self.refresh_materials)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in Control.get_materials_data():
            self.materialsTable.insert(
                "",
                "end",
                values=(i.id, i.name, round((i.price * rate), 2))
            )
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(state=tk.DISABLED, bg="gray")

    def refresh_materials(self, event):
        for i in self.materialsTable.get_children():
            self.materialsTable.delete(i)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in Control.get_materials_data():
            self.materialsTable.insert(
                "",
                "end",
                values=(i.id, i.name, round((i.price * rate), 2))
            )
