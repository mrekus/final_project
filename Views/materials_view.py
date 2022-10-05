from utils import *


class MaterialsViews:
    def fill_materials_data_box(self):
        """
        Atstato pradinę lango būseną su Materials duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.materialsTable.grid(
            row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW
        )
        for i in self.materialsTable.get_children():
            self.materialsTable.delete(i)
        self.materialsTable.column(f"# {1}", anchor=tk.CENTER, width=40)
        self.materialsTable.heading(f"# {1}", text="ID")
        for i, col_heading in enumerate(["Name", "Price / kg"], 2):
            self.materialsTable.column(f"# {i}", anchor=tk.CENTER, width=120)
            self.materialsTable.heading(f"# {i}", text=col_heading)
        self.currency_list.bind("<<ComboboxSelected>>", self.refresh_materials)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in control.get_table_data("Materials"):
            self.materialsTable.insert(
                "", "end", values=(i.id, i.name, round((i.price * rate), 2))
            )
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(command=self.edit_material_get_values, text="Edit")

    def refresh_materials(self, _event):
        """
        Atnaujina Materials lentelės įrašus
        :param _event: aktyvuojama currency combobox pasirinkimu
        """
        for i in self.materialsTable.get_children():
            self.materialsTable.delete(i)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in control.get_table_data("Materials"):
            self.materialsTable.insert(
                "", "end", values=(i.id, i.name, round((i.price * rate), 2))
            )

    def edit_record_materials(self):
        """
        Sukuria visus Materials edit langus
        """
        self.labelEdit1.grid(row=1, column=7, sticky="W")
        self.labelEdit2.grid(row=2, column=7, sticky="W")
        self.labelEdit1.config(text="Name: ")
        self.labelEdit2.config(text="Price: ")
        self.buttonEdit.config(text="Save changes", command=self.edit_material)
        self.buttonDelete.config(state=tk.DISABLED, bg="gray")
        self.entryFieldEdit1.grid(row=1, column=8)
        self.entryFieldEdit2.grid(row=2, column=8)
        self.buttonCancelEditing.grid(row=3, column=6)
        self.buttonCancelEditing.config(command=self.cancel_editing_material)
        self.entryFieldEdit1.focus()

    def edit_material_get_values(self):
        """
        Paima pasirinkto Materials įrašo vertes redagavimui
        """
        try:
            self.edit_record_materials()
            selection = self.materialsTable.item(self.materialsTable.focus())
            selection = selection["values"]
            self.idForEdit.set(selection[0])
            self.entryFieldEdit1.insert(0, selection[1])
            self.entryFieldEdit2.insert(0, selection[2])
        except IndexError:
            logging.warning("No record selected when trying to edit material")
            self.fill_materials_data_box()

    def cancel_editing_material(self):
        """
        Atšaukia Materials įrašo redagavimą
        """
        self.cancel_editing()
        self.buttonEdit.config(text="Edit", command=self.edit_material_get_values)

    def edit_material(self):
        """
        Tikrina redaguojamą Materials įrašą ar jis turi pavadinimą, tada ar jis nesikartoja
        ir ar Price reikšmės didesnės už 0, jei taip, redaguotą įrašą išsaugo, jei ne meta ERROR.
        """
        selected_field = control.get_record_by_id("Materials", self.idForEdit.get())
        selected_field = selected_field.name
        entered_name = self.entryFieldEdit1.get().strip()
        entered_name = re.sub(" +", " ", entered_name)
        if any(i.isalpha() or i.isdigit() for i in entered_name):
            if entered_name.lower() not in [
                i.lower()
                for i in control.check_for_duplicates_materials()
                if i != selected_field
            ]:
                try:
                    entered_price = float(self.entryFieldEdit2.get())
                    if entered_price > 0:
                        control.update_material(
                            self.idForEdit.get(), entered_name, entered_price
                        )
                        self.fill_materials_data_box()
                    else:
                        logging.error(
                            "Material price entered was less than 0 when trying to edit a material"
                        )
                        ErrorWindow("Price must be more than 0!")
                except ValueError:
                    logging.error(
                        "Wrong material values input when trying to edit a material"
                    )
                    ErrorWindow("Price must be a number!")
            else:
                logging.error("Entered a duplicate name when editing material record")
                ErrorWindow("Material record with that name already exists!")
        else:
            logging.error("No name entered when trying to edit a material record")
            ErrorWindow("No name entered!")
