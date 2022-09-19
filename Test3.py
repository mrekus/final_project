from tkinter import *
from Project1.Control import *
from tkinter import ttk
import logging
from datetime import datetime


class MyButton(Button):
    """
    Perrašo default Button klasę
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="white", fg="black", font=("courier", 12, "bold"), relief="groove", height=3, width=15,
                    activebackground="#0a0a0a", activeforeground="#e6d415")


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


class Main:
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style()
        self.style.theme_use("clam")

        logging.basicConfig(filename="Project_error_log.log", level=logging.WARNING,
                            format="%(asctime)s - %(levelname)s - %(message)s", encoding="UTF-8")

        gradient_step = 0
        hex_step = 400
        for _ in range(40):
            color_hex = str(224499 + hex_step)
            Frame(master, width=100, height=550, bg="#" + color_hex).place(x=gradient_step, y=0)
            gradient_step += 100
            hex_step += 300

        self.idForEdit = IntVar()

        self.topFrame = Frame(master)
        self.leftFrame = Frame(master)

        self.menu = Menu(master)
        self.master.config(menu=self.menu)
        self.submenu = Menu(self.menu, tearoff=False)

        self.buttonAddOrder = Button(self.topFrame, text="Add an Order", height=3, width=20, anchor=CENTER,
                                     bg="white", fg="black", font=("courier", 20, "bold"), relief="groove",
                                     command=self.order_adding_widgets, activebackground="#0a0a0a",
                                     activeforeground="#e6d415")
        self.buttonProcesses = MyButton(self.leftFrame, text="Processes", command=self.fill_process_data_box)
        self.buttonRecipies = MyButton(self.leftFrame, text="Recipies", command=self.fill_recipe_data_box)
        self.buttonStorage = MyButton(self.leftFrame, text="Storage", command=self.fill_storage_data_box)
        self.buttonEdit = MyButton(self.leftFrame, text="Edit")
        self.buttonDelete = Button(self.leftFrame, text="Delete", bg="red", fg="black", font=("courier", 12), height=3,
                                   width=15, command=self.delete_record)
        self.buttonAddRecipe = MyButton(self.leftFrame, text="Add Recipe", command=self.add_record_recipies)
        self.buttonCancelEditing = MyButton(self.leftFrame, text="Cancel", command=self.cancel_editing)
        self.buttonCancelOrder = Button(self.topFrame, text="Cancel Order", height=3, width=20, anchor=CENTER,
                                        bg="red", fg="black", font=("courier", 14, "bold"), relief="groove",
                                        command=self.cancel_order)
        self.buttonConfirmOrder = Button(self.topFrame, text="Confirm Order", height=3, width=20, anchor=CENTER,
                                         bg="white", fg="black", font=("courier", 14, "bold"), relief="groove",
                                         command=self.order_calculation, activebackground="#0a0a0a",
                                         activeforeground="#e6d415")
        self.labelEdit1 = MyLabel(self.leftFrame)
        self.labelEdit2 = MyLabel(self.leftFrame)
        self.labelEdit3 = MyLabel(self.leftFrame)
        self.labelEdit4 = MyLabel(self.leftFrame)
        self.labelEdit5 = MyLabel(self.leftFrame)
        self.labelEdit6 = MyLabel(self.leftFrame)
        self.labelOrder = Label(self.topFrame, text="Amount in kg:", font=("courier", 25, "bold"), width=15)
        self.entryFieldEdit1 = MyEntry(self.leftFrame)
        self.entryFieldEdit2 = MyEntry(self.leftFrame)
        self.entryFieldEdit3 = MyEntry(self.leftFrame)
        self.entryFieldEdit4 = MyEntry(self.leftFrame)
        self.entryFieldEdit5 = MyEntry(self.leftFrame)
        self.entryFieldEdit6 = MyEntry(self.leftFrame)
        self.entryFieldOrder = Entry(self.topFrame, font=("courier", 25, "bold"), width=15)
        self.recipe_list = ttk.Combobox(self.topFrame, width=12, font=("courier", 25, "bold"), state="readonly")
        self.processTable = ttk.Treeview(self.leftFrame, columns=("id", "Process", "Material", "Efficiency kg/h"),
                                         show='headings', height=8)
        self.recipeTable = ttk.Treeview(self.leftFrame, columns=(
            "id", "Recipe", "Material 1", "Material 2", "Material 3", "Material 4", "Material 5"), show='headings',
                                        height=8)
        self.storageTable = ttk.Treeview(self.leftFrame, columns=("id", "Name", "Amount kg"), show='headings', height=8)

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

    def fill_process_data_box(self):
        """
        Atstato pradinę lango būseną su Process duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.processTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
        for i in self.processTable.get_children():
            self.processTable.delete(i)
        for i, col_heading in enumerate(["ID", "Process", "Material", "Efficiency kg/h"], 1):
            self.processTable.column(f"# {i}", anchor=CENTER, width=90)
            self.processTable.heading(f"# {i}", text=col_heading)
        for i in get_process_data():
            self.processTable.insert('', 'end', values=(i.id, i.name, i.produced_material, i.efficiency))
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(command=self.edit_process_get_values, text="Edit")

    def fill_recipe_data_box(self):
        """
        Atstato pradinę lango būseną su Recipe duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        headings = check_for_duplicates_storage()
        self.recipeTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
        for i in self.recipeTable.get_children():
            self.recipeTable.delete(i)
        for i, col_heading in enumerate(
                ["ID", "Recipe", headings[0], headings[1], headings[2], headings[3], headings[4]], 1):
            self.recipeTable.column(f"# {i}", anchor=CENTER, width=90)
            self.recipeTable.heading(f"# {i}", text=col_heading)
        for i in get_recipe_data():
            self.recipeTable.insert('', 'end', values=(
                i.id, i.name, i.material1, i.material2, i.material3, i.material4, i.material5))
        self.buttonDelete.config(state=NORMAL, bg="red")
        self.buttonAddRecipe.grid(row=3, column=6)
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")

    def fill_storage_data_box(self):
        """
        Atstato pradinę lango būseną su Storage duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.storageTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
        for i in self.storageTable.get_children():
            self.storageTable.delete(i)
        for i, col_heading in enumerate(["ID", "Name", "Amount kg"], 1):
            self.storageTable.column(f"# {i}", anchor=CENTER, width=90)
            self.storageTable.heading(f"# {i}", text=col_heading)
        for i in get_storage_data():
            self.storageTable.insert('', 'end', values=(i.id, i.name, i.amount))
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(command=self.edit_storage_get_values, text="Edit")

    def default_button_layouts(self):
        """
        Atstato pradinius mygtukų išdėstymus, išvalo EDIT laukus
        """
        self.buttonEdit.grid(row=1, column=6)
        self.buttonDelete.grid(row=2, column=6)
        self.buttonDelete.config(state=DISABLED, bg="gray")
        self.cancel_editing()

    def edit_record_process(self):
        """
        Sukuria visus Process edit langus
        """
        self.labelEdit1.grid(row=1, column=7, sticky="W")
        self.labelEdit2.grid(row=2, column=7, sticky="W")
        self.labelEdit3.grid(row=3, column=7, sticky="W")
        self.labelEdit1.config(text="Name: ")
        self.labelEdit2.config(text="Material: ")
        self.labelEdit3.config(text="Efficiency: ")
        self.buttonEdit.config(text="Save changes", command=self.edit_process)
        self.buttonDelete.config(state=DISABLED, bg="gray")
        self.entryFieldEdit1.grid(row=1, column=8)
        self.entryFieldEdit2.grid(row=2, column=8)
        self.entryFieldEdit3.grid(row=3, column=8)
        self.buttonCancelEditing.grid(row=3, column=6)
        self.buttonCancelEditing.config(command=self.cancel_editing_process)
        self.entryFieldEdit1.focus()

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
            delete_recipe_record(deletion_id)
            self.fill_recipe_data_box()
            self.refresh_recipe_list()
        except IndexError:
            logging.warning("No record selected when trying to delete recipe!")
            self.fill_recipe_data_box()

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
                                                                       check_for_duplicates_recipe()]:
            if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
                try:
                    check_values = [float(self.entryFieldEdit2.get()), float(self.entryFieldEdit3.get()),
                                    float(self.entryFieldEdit4.get()), float(self.entryFieldEdit5.get()),
                                    float(self.entryFieldEdit6.get())]
                    if all(0 <= i <= 1 for i in check_values) and round(sum(check_values), 3) == 1:
                        add_recipe(self.entryFieldEdit1.get(), self.entryFieldEdit2.get(), self.entryFieldEdit3.get(),
                                   self.entryFieldEdit4.get(), self.entryFieldEdit5.get(), self.entryFieldEdit6.get())
                        self.fill_recipe_data_box()
                        self.refresh_recipe_list()
                    else:
                        logging.error("Material sum not equal to 1 when trying to add new recipe")
                        self.error_popup("Material sum must amount to 1!")
                except ValueError:
                    logging.error("Wrong material values input when trying to add new recipe")
                    self.error_popup("Material inputs are not numbers, or are not filled!")
            else:
                logging.error("No name input when trying to add new recipe")
                self.error_popup("No name entered!")
        else:
            logging.error("Entered a duplicate name when adding new recipe")
            self.error_popup("Recipe with that name already exists!")

    def edit_process_get_values(self):
        """
        Paima pasirinkto Process įrašo vertes redagavimui
        """
        try:
            self.edit_record_process()
            selection = self.processTable.item(self.processTable.focus())
            record = str(selection).replace("]", "[")
            record = record.split("[")
            record = record[1]
            self.idForEdit.set(int(record[0]))
            record = record.replace("'", "")
            record = record.split(",")
            self.entryFieldEdit1.insert(0, record[1][1::])
            self.entryFieldEdit2.insert(0, record[2][1::])
            self.entryFieldEdit3.insert(0, record[3][1::])
        except IndexError:
            logging.warning("No record selected when trying to edit process")
            self.fill_process_data_box()

    def edit_process(self):
        """
        Redaguoja Process įrašą jei jis turi pavadinimą, jis nesikartoja ir našumas daugiau nei 0,
        ir įrašo vertes į DB. Kitu atveju meta ERROR
        """
        selected_field = session.query(Process).get(self.idForEdit.get())
        selected_field_name = selected_field.name
        selected_field_material = selected_field.produced_material
        if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
            if self.entryFieldEdit1.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                           check_for_duplicates_process() if
                                                                           i != selected_field_name]:
                if self.entryFieldEdit2.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                               check_for_duplicates_storage() if
                                                                               i != selected_field_material]:
                    try:
                        if float(self.entryFieldEdit3.get()) > 0:
                            update_process(self.idForEdit.get(), self.entryFieldEdit1.get(), self.entryFieldEdit2.get(),
                                           self.entryFieldEdit3.get())
                            update_storage_material_from_process(self.idForEdit.get(), self.entryFieldEdit2.get())
                            self.fill_process_data_box()
                        else:
                            logging.error("Efficiency input was less than 0 when trying to edit a process")
                            self.error_popup("Efficiency must be more than 0!")
                    except ValueError:
                        logging.error("Efficiency value was not a number when trying to edit a process")
                        self.error_popup("Efficiency must be a number!")
                else:
                    logging.error("Entered a duplicate material name when editing process record")
                    self.error_popup("Process record with that material name already exists!")
            else:
                logging.error("Entered a duplicate name when editing process record")
                self.error_popup("Process record with that name already exists!")
        else:
            logging.error("No process name entered when trying to edit a process")
            self.error_popup("No name entered!")

    def cancel_editing_process(self):
        """
        Atšaukia Process įrašo redagavimą
        """
        self.cancel_editing()
        self.buttonEdit.config(text="Edit", command=self.edit_process_get_values)

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
        selected_field = session.query(Recipe).get(self.idForEdit.get())
        selected_field = selected_field.name
        if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
            if self.entryFieldEdit1.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                           check_for_duplicates_recipe() if
                                                                           i != selected_field]:
                try:
                    check_values = [float(self.entryFieldEdit2.get()), float(self.entryFieldEdit3.get()),
                                    float(self.entryFieldEdit4.get()), float(self.entryFieldEdit5.get()),
                                    float(self.entryFieldEdit6.get())]
                    if all((0 <= i <= 1) for i in check_values) and round(sum(check_values), 3) == 1:
                        update_recipe(self.idForEdit.get(), self.entryFieldEdit1.get(), self.entryFieldEdit2.get(),
                                      self.entryFieldEdit3.get(),
                                      self.entryFieldEdit4.get(), self.entryFieldEdit5.get(),
                                      self.entryFieldEdit6.get())
                        self.fill_recipe_data_box()
                        self.refresh_recipe_list()
                    else:
                        logging.error("Material sum was not equal to 1 or were negative when trying to edit a recipe")
                        self.error_popup("Material sum must amount to 1 and material values must be positive!")
                except ValueError:
                    logging.error("Wrong material values input when trying to edit a recipe")
                    self.error_popup("Material inputs must be numbers!")
            else:
                logging.error("Entered a duplicate name when editing recipe record")
                self.error_popup("Recipe record with that name already exists!")
        else:
            logging.error("No recipe name entered when trying to edit a recipe")
            self.error_popup("No name entered!")

    def cancel_editing_recipies(self):
        """
        Atšaukia Recipies įrašo redagavimą ir pašalina laukus
        """
        self.cancel_editing()
        self.buttonDelete.config(state=NORMAL, bg="red")
        self.buttonEdit.config(command=self.edit_recipies_get_values, text="Edit")

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
        selected_field = session.query(Storage).get(self.idForEdit.get())
        selected_field = selected_field.name
        if any(i.isalpha() or i.isdigit() for i in self.entryFieldEdit1.get()):
            if self.entryFieldEdit1.get().lower().replace(" ", "") not in [i.lower().replace(" ", "") for i in
                                                                           check_for_duplicates_storage() if
                                                                           i != selected_field]:
                try:
                    if float(self.entryFieldEdit2.get()) > 0:
                        update_storage(self.idForEdit.get(), self.entryFieldEdit1.get(), self.entryFieldEdit2.get())
                        update_process_material_from_storage(self.idForEdit.get(), self.entryFieldEdit1.get())
                        self.fill_storage_data_box()
                    else:
                        logging.error("Material amount entered was less than 0 when trying to edit a storage record")
                        self.error_popup("Amount must be more than 0!")
                except ValueError:
                    logging.error("Wrong material values input when trying to edit a storage record")
                    self.error_popup("Amount must be a number!")
            else:
                logging.error("Entered a duplicate name when editing storage record")
                self.error_popup("Storage record with that name already exists!")
        else:
            logging.error("No name entered when trying to edit a storage record")
            self.error_popup("No name entered!")

    def cancel_editing_storage(self):
        """
        Atšaukia Storage įrašo redagavimą ir atstato laukus
        """
        self.cancel_editing()
        self.buttonEdit.config(text="Edit", command=self.edit_storage_get_values)

    def refresh_recipe_list(self):
        """
        Atjauniną receptų sąrašą
        """
        self.recipe_list.config(values=check_for_duplicates_recipe())
        self.recipe_list.set("")

    def order_adding_widgets(self):
        """
        Sukuria užsakymo pridėjimo laukus ir atnaujina receptų sąrašą
        """
        self.refresh_recipe_list()
        self.recipe_list.grid(row=1, column=0)
        self.buttonAddOrder.grid_forget()
        self.entryFieldOrder.grid(row=1, column=1)
        self.labelOrder.grid(row=0, column=1)
        self.buttonConfirmOrder.grid(row=1, column=2)
        self.buttonCancelOrder.grid(row=1, column=3)

    def cancel_order(self):
        """
        Atšaukia užsakymo pridėjimą, pašalina ir išvalo laukus
        """
        self.buttonAddOrder.grid(row=1, column=0)
        self.entryFieldOrder.grid_forget()
        self.entryFieldOrder.delete(0, END)
        self.labelOrder.grid_forget()
        self.buttonCancelOrder.grid_forget()
        self.buttonConfirmOrder.grid_forget()
        self.recipe_list.grid_forget()
        self.recipe_list.set("")

    def order_calculation(self):
        """
        Tikrina ar pasirinktas receptas, tada ar užsakymo vertė daugiau už 0,
        jei taip, skaičiuoja reikiamą žaliavų kiekį, jei ne meta ERROR
        """
        try:
            if self.recipe_list.get() != "":
                if int(self.entryFieldOrder.get()) > 0:
                    selected_recipe = str(session.query(Recipe).filter_by(name=self.recipe_list.get()).one())
                    selected_recipe = selected_recipe.replace(" ", "")
                    selected_recipe = selected_recipe.replace(";", "-")
                    selected_recipe = selected_recipe.split("-")
                    del selected_recipe[0]
                    selected_recipe = [float(i) for i in selected_recipe]
                    self.calculate_required_materials(selected_recipe, int(self.entryFieldOrder.get()))
                    self.fill_storage_data_box()
                    self.cancel_order()
                else:
                    logging.error("Order amount entered was less than 0 when trying to submit an order")
                    self.error_popup("Order amount must be more than 0!")
            else:
                logging.error("No recipe chosen when trying to submit an order")
                self.error_popup("No recipe chosen!")
        except ValueError:
            logging.error("Wrong value type entered when trying to add an order")
            self.error_popup("Amount is not a number!")

    def calculate_required_materials(self, selected_recipe, entry):
        """
        Skaičiuoja reikiamą žaliavų kiekį užsakymui įvykdyti
        :param selected_recipe: pasirinktas receptas užsakymui
        :param entry: užsakymo dydis
        """
        required_materials = [i * entry for i in selected_recipe]
        storage = str(get_storage_data())
        storage = storage.replace(",", "-")
        storage = storage.replace("]", "")
        storage = storage.replace(" ", "")
        storage = storage.replace("kg", "")
        storage = storage.split("-")
        storage = [float(i) for i in storage[1::2]]
        storage_remaining = [i - j for (i, j) in zip(storage, required_materials)]
        self.check_storage_remainder(storage_remaining)

    def check_storage_remainder(self, storage_remaining):
        """
        Tikrina ar sandėlio žaliavų likutis yra neigiamas, jei taip, apskaičiuoja
        kiek reikės darbo valandų kad pasiekti teigiamą kiekį, jei ne, surašo į DB
        :param storage_remaining: priima sandėlio likutį
        """
        num = 0
        if min(storage_remaining) < 0:
            storage = str(get_process_data())
            efficiency = storage.replace("k", "-")
            efficiency = efficiency.replace(" ", "")
            efficiency = efficiency.split("-")
            efficiency = [float(i) for i in efficiency[2::3]]
            check_remainder = [i + j for (i, j) in zip(efficiency, storage_remaining)]
            num += 1
            while min(check_remainder) < 0:
                check_remainder = [i + j for (i, j) in zip(efficiency, check_remainder)]
                num += 1
            logging.critical("Not enough material in storage to complete an order")
            self.error_popup(
                f"Not enough materials to complete the order,\n"
                f"it will take {num} working hours to get enough material")
            with open("orders.txt", "a", encoding="utf-8") as record_order:
                record_order.write(
                    f"{datetime.now()} - Order of {self.recipe_list.get()} - {self.entryFieldOrder.get()}kg could not "
                    f"be completed, not enough materials. It will take {num} working hours to complete this order.\n")
        else:
            record_id = 1
            with open("orders.txt", "a", encoding="utf-8") as record_order:
                record_order.write(
                    f"{datetime.now()} - Order of {self.recipe_list.get()} - "
                    f"{self.entryFieldOrder.get()}kg completed.\n")
            for i in storage_remaining:
                record = session.query(Storage).get(record_id)
                record.amount = round(i, 1)
                record_id += 1
            session.commit()

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

    def error_popup(self, text):
        """
        Iššaukia ERROR langą su tekstu
        :param text: priima error lango tekstą
        """
        error_window = Toplevel()
        error_window.geometry("+900+500")
        error_window.title("Error")
        frame = Frame(error_window)
        error_text = Label(frame, text=text, anchor=CENTER, font=("courier", 25, "bold"))
        ok_button = Button(frame, text="Confirm", command=error_window.destroy, anchor=CENTER, bg="white", fg="black",
                           font=("courier", 12, "bold"), relief="groove", height=1, width=15,
                           activebackground="#0a0a0a", activeforeground="#e6d415")
        error_text.grid(row=0, column=1)
        ok_button.grid(row=1, column=1)
        frame.pack(expand=True)
        self.master.bell()


def main():
    window = Tk()
    Main(window)
    window.geometry("1570x550+400+400")
    window.resizable(False, False)
    window.title("Control panel")
    window.mainloop()


if __name__ == '__main__':
    main()
