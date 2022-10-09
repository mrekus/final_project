from utils import *


class RecipiesViews(widgets.Widgets):
    """
    Visi metodai valdantys Recipies laukus
    """
    def fill_recipe_data_box(self):
        """
        Atstato pradinę lango būseną su Recipe duomenų lentele,
        sukuria scroll bar jei įrašų daugiau nei 8
        """
        self.default_button_layouts()
        self.forget_tables()
        headings = control.check_for_duplicates("Materials")
        self.recipeTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.recipeTable.get_children():
            self.recipeTable.delete(i)
        self.recipeTable.column(f"# {1}", anchor=tk.CENTER, width=40)
        self.recipeTable.heading(f"# {1}", text="ID")
        self.recipeTable.column(f"# {2}", anchor=tk.CENTER, width=130)
        self.recipeTable.heading(f"# {2}", text="Recipe")
        for i, col_heading in enumerate(
            [*headings],
            3,
        ):
            self.recipeTable.column(f"# {i}", anchor=tk.CENTER, width=83)
            self.recipeTable.heading(f"# {i}", text=col_heading)
        for i in control.get_table_data("Recipe"):
            self.recipeTable.insert(
                "",
                "end",
                values=(
                    i.id,
                    i.name,
                    i.material1,
                    i.material2,
                    i.material3,
                    i.material4,
                    i.material5,
                ),
            )
        self.buttonDelete.config(state=tk.NORMAL, bg="red")
        self.buttonAddRecipe.grid(row=3, column=6)
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")
        if len(self.recipeTable.get_children()) >= 9:
            self.scrollbar_recipe.place(x=571, y=27, height=175)
            self.recipeTable.configure(yscrollcommand=self.scrollbar_recipe.set)

    def refresh_recipies(self):
        """
        Atnaujina Recipe lentelės įrašus, atstato pradinę
        mygtukų būseną. Sukuria scroll bar jei įrašų daugiau
        nei 8.
        """
        for i in self.recipeTable.get_children():
            self.recipeTable.delete(i)
        for i in control.get_table_data("Recipe"):
            self.recipeTable.insert(
                "",
                "end",
                values=(
                    i.id,
                    i.name,
                    i.material1,
                    i.material2,
                    i.material3,
                    i.material4,
                    i.material5,
                ),
            )
        self.default_button_layouts()
        self.buttonDelete.config(state=tk.NORMAL, bg="red")
        self.buttonAddRecipe.grid(row=3, column=6)
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")
        self.scrollbar_recipe.place_forget()
        self.recipe_list.config(values=control.check_for_duplicates("Recipe"))
        self.recipe_list.set("")
        if len(self.recipeTable.get_children()) >= 9:
            self.scrollbar_recipe.place(x=571, y=27, height=175)
            self.recipeTable.configure(yscrollcommand=self.scrollbar_recipe.set)

    def edit_record_recipies(self):
        """
        Sukuria visus Recipies edit langus
        """
        materials = control.check_for_duplicates("Materials")
        self.buttonEdit.config(
            text="Save changes", activebackground="#00A650", command=self.edit_recipe
        )
        self.labelEdit1.grid(row=1, column=7, sticky="W")
        self.labelEdit2.grid(row=2, column=7, sticky="W")
        self.labelEdit3.grid(row=3, column=7, sticky="W")
        self.labelEdit4.grid(row=1, column=9, sticky="W")
        self.labelEdit5.grid(row=2, column=9, sticky="W")
        self.labelEdit6.grid(row=3, column=9, sticky="W")
        self.buttonCancelEditing.grid(row=3, column=6)
        self.labelEdit1.config(text="Name: ")
        self.labelEdit2.config(text=f"{materials[0]}: ")
        self.labelEdit3.config(text=f"{materials[1]}: ")
        self.labelEdit4.config(text=f"{materials[2]}: ")
        self.labelEdit5.config(text=f"{materials[3]}: ")
        self.labelEdit6.config(text=f"{materials[4]}: ")
        self.entryFieldEdit1.grid(row=1, column=8)
        self.entryFieldEdit2.grid(row=2, column=8)
        self.entryFieldEdit3.grid(row=3, column=8)
        self.entryFieldEdit4.grid(row=1, column=10)
        self.entryFieldEdit5.grid(row=2, column=10)
        self.entryFieldEdit6.grid(row=3, column=10)
        self.buttonCancelEditing.config(
            activebackground="red", command=self.cancel_editing_recipies
        )
        self.buttonDelete.config(activebackground="red", state=tk.DISABLED, bg="gray")
        self.entryFieldEdit1.focus()

    def delete_record(self):
        """
        Ištrina pasirinktą recepto įrašą
        """
        try:
            selection = self.recipeTable.item(self.recipeTable.focus())
            selection = selection["values"]
            deletion_id = selection[0]
            control.delete_recipe_record(deletion_id)
            self.refresh_recipies()
            self.recipe_list.config(values=control.check_for_duplicates("Recipe"))
            self.recipe_list.set("")
        except IndexError:
            logging.warning("No record selected when trying to delete recipe!")
            self.refresh_recipies()

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
        entered_name = self.entryFieldEdit1.get().strip()
        entered_name = re.sub(" +", " ", entered_name)
        if entered_name.lower() not in [
            i.lower() for i in control.check_for_duplicates("Recipe")
        ]:
            if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
                try:
                    check_values = [
                        float(self.entryFieldEdit2.get()),
                        float(self.entryFieldEdit3.get()),
                        float(self.entryFieldEdit4.get()),
                        float(self.entryFieldEdit5.get()),
                        float(self.entryFieldEdit6.get()),
                    ]
                    if (
                        all(0 <= i <= 1 for i in check_values)
                        and round(sum(check_values), 3) == 1
                    ):
                        control.add_recipe(
                            self.entryFieldEdit1.get(),
                            self.entryFieldEdit2.get(),
                            self.entryFieldEdit3.get(),
                            self.entryFieldEdit4.get(),
                            self.entryFieldEdit5.get(),
                            self.entryFieldEdit6.get(),
                        )
                        self.refresh_recipies()
                    else:
                        logging.error(
                            "Material sum not equal to 1 when trying to add new recipe"
                        )
                        ErrorWindow("Material sum must amount to 1!")
                except ValueError:
                    logging.error(
                        "Wrong material values input when trying to add new recipe"
                    )
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
            selection = selection["values"]
            self.idForEdit.set(selection[0])
            self.entryFieldEdit1.insert(0, selection[1])
            self.entryFieldEdit2.insert(0, selection[2])
            self.entryFieldEdit3.insert(0, selection[3])
            self.entryFieldEdit4.insert(0, selection[4])
            self.entryFieldEdit5.insert(0, selection[5])
            self.entryFieldEdit6.insert(0, selection[6])
        except IndexError:
            logging.warning("No record selected when trying to edit a recipe")
            self.refresh_recipies()

    def edit_recipe(self):
        """
        Redaguoja Recipies įrašą jei jis turi pavadinimą, ar jis nesikartoja,
         ir ar medžiagų dalių suma yra 1, ir prideda jį į DB. Klaidos atveju meta ERROR.
        :return:
        """
        selected_field = control.get_record_by_id("Recipe", self.idForEdit.get())
        selected_field = selected_field.name
        entered_name = self.entryFieldEdit1.get().strip()
        entered_name = re.sub(" +", " ", entered_name)
        if any(i.isalpha() or i.isdigit() for i in entered_name):
            if entered_name.lower() not in [
                i.lower()
                for i in control.check_for_duplicates("Recipe")
                if i != selected_field
            ]:
                try:
                    check_values = [
                        float(self.entryFieldEdit2.get()),
                        float(self.entryFieldEdit3.get()),
                        float(self.entryFieldEdit4.get()),
                        float(self.entryFieldEdit5.get()),
                        float(self.entryFieldEdit6.get()),
                    ]
                    if (
                        all((0 <= i <= 1) for i in check_values)
                        and round(sum(check_values), 3) == 1
                    ):
                        control.update_recipe(
                            self.idForEdit.get(),
                            self.entryFieldEdit1.get(),
                            self.entryFieldEdit2.get(),
                            self.entryFieldEdit3.get(),
                            self.entryFieldEdit4.get(),
                            self.entryFieldEdit5.get(),
                            self.entryFieldEdit6.get(),
                        )
                        self.refresh_recipies()
                    else:
                        logging.error(
                            "Material sum was not equal to 1 or were negative when trying to edit a recipe"
                        )
                        ErrorWindow(
                            "Material sum must amount to 1 and material values must be positive!"
                        )
                except ValueError:
                    logging.error(
                        "Wrong material values input when trying to edit a recipe"
                    )
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
        self.buttonEdit.config(
            command=self.edit_recipies_get_values,
            activebackground="#75C1BF",
            text="Edit",
        )
