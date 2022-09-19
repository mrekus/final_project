from utils import *


class RecipiesViews:
    def fill_recipe_data_box(self):
        """
        Atstato pradinę lango būseną su Recipe duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        headings = Control.check_for_duplicates_storage()
        self.recipeTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.recipeTable.get_children():
            self.recipeTable.delete(i)
        for i, col_heading in enumerate(
                ["ID", "Recipe", headings[0], headings[1], headings[2], headings[3], headings[4]], 1):
            self.recipeTable.column(f"# {i}", anchor=tk.CENTER, width=90)
            self.recipeTable.heading(f"# {i}", text=col_heading)
        for i in Control.get_recipe_data():
            self.recipeTable.insert('', 'end', values=(
                i.id, i.name, i.material1, i.material2, i.material3, i.material4, i.material5))
        self.buttonDelete.config(state=tk.NORMAL, bg="red")
        self.buttonAddRecipe.grid(row=3, column=6)
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")

    def edit_record_recipies(self):
        """
        Sukuria visus Recipies edit langus
        """
        self.edit_record_process()
        self.buttonEdit.config(text="Save changes", command=self.edit_recipe)
        self.labelEdit4.grid(row=1, column=9, sticky="W")
        self.labelEdit5.grid(row=2, column=9, sticky="W")
        self.labelEdit6.grid(row=3, column=9, sticky="W")
        self.labelEdit2.config(text="Material 1: ")
        self.labelEdit3.config(text="Material 2: ")
        self.labelEdit4.config(text="Material 3: ")
        self.labelEdit5.config(text="Material 4: ")
        self.labelEdit6.config(text="Material 5: ")
        self.entryFieldEdit4.grid(row=1, column=10)
        self.entryFieldEdit5.grid(row=2, column=10)
        self.entryFieldEdit6.grid(row=3, column=10)
        self.buttonCancelEditing.config(command=self.cancel_editing_recipies)

    def delete_record(self):
        """
        Ištrina pasirinktą recepto įrašą
        """
        try:
            selection = self.recipeTable.item(self.recipeTable.focus())
            deletion_id = str(selection).replace("]", "[")
            deletion_id = deletion_id.replace(" ", "")
            deletion_id = deletion_id.split("[")
            deletion_id = deletion_id[1]
            deletion_id = int(deletion_id[0])
            Control.delete_recipe_record(deletion_id)
            self.fill_recipe_data_box()
            self.refresh_recipe_list()
        except IndexError:
            logging.warning("No record selected when trying to delete recipe!")
            self.fill_recipe_data_box()

    def add_record_recipies(self):
        """
        Atidaro naujo Recipies įrašo pridėjimo laukus, pakeičia Edit
        mygtuką į Save
        """
        self.edit_record_recipies()
        self.buttonEdit.config(command=self.gui_add_recipe)

    def gui_add_recipe(self):
        """
        Prideda naują receptą į DB jei jis turi pavadinimą, ir medžiagų dalių suma yra 1,
        klaidos atveju meta ERROR
        """
        if self.entryFieldEdit1.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                       Control.check_for_duplicates_recipe()]:
            if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
                try:
                    check_values = [float(self.entryFieldEdit2.get()), float(self.entryFieldEdit3.get()),
                                    float(self.entryFieldEdit4.get()), float(self.entryFieldEdit5.get()),
                                    float(self.entryFieldEdit6.get())]
                    if all(0 <= i <= 1 for i in check_values) and round(sum(check_values), 3) == 1:
                        Control.add_recipe(self.entryFieldEdit1.get(), self.entryFieldEdit2.get(), self.entryFieldEdit3.get(),
                                           self.entryFieldEdit4.get(), self.entryFieldEdit5.get(), self.entryFieldEdit6.get())
                        self.fill_recipe_data_box()
                        self.refresh_recipe_list()
                    else:
                        logging.error("Material sum not equal to 1 when trying to add new recipe")
                        ErrorWindow("Material sum must amount to 1!")
                except ValueError:
                    logging.error("Wrong material values input when trying to add new recipe")
                    ErrorWindow("Material inputs are not numbers, or are not filled!")
            else:
                logging.error("No name input when trying to add new recipe")
                ErrorWindow("No name entered!")
        else:
            logging.error("Entered a duplicate name when adding new recipe")
            ErrorWindow("Recipe with that name already exists!")

    def edit_recipies_get_values(self):
        """
        Pasiima pasirinkto Recipies įrašo vertes redagavimui
        """
        try:
            self.edit_record_recipies()
            selection = self.recipeTable.item(self.recipeTable.focus())
            record = str(selection).replace("]", "[")
            record = record.split("[")
            record = record[1]
            self.idForEdit.set(int(record[0]))
            record = record.replace("'", "")
            record = record.split(",")
            self.entryFieldEdit1.insert(0, record[1][1::])
            self.entryFieldEdit2.insert(0, record[2][1::])
            self.entryFieldEdit3.insert(0, record[3][1::])
            self.entryFieldEdit4.insert(0, record[4][1::])
            self.entryFieldEdit5.insert(0, record[5][1::])
            self.entryFieldEdit6.insert(0, record[6][1::])
        except IndexError:
            logging.warning("No record selected when trying to edit a recipe")
            self.fill_recipe_data_box()

    def edit_recipe(self):
        """
        Redaguoja Recipies įrašą jei jis turi pavadinimą, ar jis nesikartoja,
         ir ar medžiagų dalių suma yra 1, ir prideda jį į DB. Klaidos atveju meta ERROR.
        :return:
        """
        selected_field = Control.session.query(Control.Recipe).get(self.idForEdit.get())
        selected_field = selected_field.name
        if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
            if self.entryFieldEdit1.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                           Control.check_for_duplicates_recipe() if
                                                                           i != selected_field]:
                try:
                    check_values = [float(self.entryFieldEdit2.get()), float(self.entryFieldEdit3.get()),
                                    float(self.entryFieldEdit4.get()), float(self.entryFieldEdit5.get()),
                                    float(self.entryFieldEdit6.get())]
                    if all((0 <= i <= 1) for i in check_values) and round(sum(check_values), 3) == 1:
                        Control.update_recipe(self.idForEdit.get(), self.entryFieldEdit1.get(), self.entryFieldEdit2.get(),
                                              self.entryFieldEdit3.get(),
                                              self.entryFieldEdit4.get(), self.entryFieldEdit5.get(),
                                              self.entryFieldEdit6.get())
                        self.fill_recipe_data_box()
                        self.refresh_recipe_list()
                    else:
                        logging.error("Material sum was not equal to 1 or were negative when trying to edit a recipe")
                        ErrorWindow("Material sum must amount to 1 and material values must be positive!")
                except ValueError:
                    logging.error("Wrong material values input when trying to edit a recipe")
                    ErrorWindow("Material inputs must be numbers!")
            else:
                logging.error("Entered a duplicate name when editing recipe record")
                ErrorWindow("Recipe record with that name already exists!")
        else:
            logging.error("No recipe name entered when trying to edit a recipe")
            ErrorWindow("No name entered!")

    def cancel_editing_recipies(self):
        """
        Atšaukia Recipies įrašo redagavimą ir pašalina laukus
        """
        self.cancel_editing()
        self.buttonDelete.config(state=tk.NORMAL, bg="red")
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")
