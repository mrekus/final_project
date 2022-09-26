from utils import *


class StorageViews:
    def fill_storage_data_box(self):
        """
        Atstato pradinę lango būseną su Storage duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.storageTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.storageTable.get_children():
            self.storageTable.delete(i)
        for i, col_heading in enumerate(["ID", "Name", "Amount kg"], 1):
            self.storageTable.column(f"# {i}", anchor=tk.CENTER, width=90)
            self.storageTable.heading(f"# {i}", text=col_heading)
        for i in Control.get_storage_data():
            self.storageTable.insert("", "end", values=(i.id, i.materials.name, i.amount))
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(command=self.edit_storage_get_values, text="Edit")

    def edit_record_storage(self):
        """
        Sukuria visus Storage edit langus
        """
        self.edit_record_process()
        self.buttonEdit.config(text="Save changes", command=self.edit_storage)
        self.labelEdit1.grid(row=1, column=7, sticky="W")
        self.labelEdit2.grid(row=2, column=7, sticky="W")
        self.labelEdit1.config(text="Name: ")
        self.labelEdit2.config(text="Ammount: ")
        self.buttonCancelEditing.config(command=self.cancel_editing_storage)
        self.labelEdit3.grid_forget()
        self.entryFieldEdit3.grid_forget()

    def edit_storage_get_values(self):
        """
        Paima pasirinkto Storage įrašo vertes redagavimui
        """
        try:
            self.edit_record_storage()
            selection = self.storageTable.item(self.storageTable.focus())
            record = str(selection).replace("]", "[")
            record = record.split("[")
            record = record[1]
            self.idForEdit.set(int(record[0]))
            record = record.replace("'", "")
            record = record.split(",")
            self.entryFieldEdit1.insert(0, record[1][1::])
            self.entryFieldEdit2.insert(0, record[2][1::])
        except IndexError:
            logging.warning("No record selected when trying to edit a storage record")
            self.fill_storage_data_box()

    def edit_storage(self):
        """
        Tikrina redaguojamą Storage įrašą ar jis turi pavadinimą, tada ar jis nesikartoja
        ir ar reikšmės didesnės už 0, jei taip, redaguotą įrašą išsaugo, jei ne meta ERROR.
        Taip pat pakeičia procesų DB material pavadinimą
        """
        selected_field = Control.session.query(Control.Storage).get(
            self.idForEdit.get()
        )
        selected_field = selected_field.name
        if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
            if self.entryFieldEdit1.get().lower().replace(" ", "") not in [
                i.lower().replace(" ", "")
                for i in Control.check_for_duplicates_storage()
                if i != selected_field
            ]:
                try:
                    if float(self.entryFieldEdit2.get()) > 0:
                        Control.update_storage(
                            self.idForEdit.get(),
                            self.entryFieldEdit2.get()
                        )
                        Control.update_material(
                            self.idForEdit.get(), self.entryFieldEdit1.get()
                        )
                        self.fill_storage_data_box()
                    else:
                        logging.error(
                            "Material amount entered was less than 0 when trying to edit a storage record"
                        )
                        ErrorWindow("Amount must be more than 0!")
                except ValueError:
                    logging.error(
                        "Wrong material values input when trying to edit a storage record"
                    )
                    ErrorWindow("Amount must be a number!")
            else:
                logging.error("Entered a duplicate name when editing storage record")
                ErrorWindow("Storage record with that name already exists!")
        else:
            logging.error("No name entered when trying to edit a storage record")
            ErrorWindow("No name entered!")

    def cancel_editing_storage(self):
        """
        Atšaukia Storage įrašo redagavimą ir atstato laukus
        """
        self.cancel_editing()
        self.buttonEdit.config(text="Edit", command=self.edit_storage_get_values)
