from utils import *


class ProcessViews:
    def fill_process_data_box(self):
        """
        Atstato pradinę lango būseną su Process duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.processTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.processTable.get_children():
            self.processTable.delete(i)
        self.processTable.column(f"# {1}", anchor=tk.CENTER, width=40)
        self.processTable.heading(f"# {1}", text="ID")
        for i, col_heading in enumerate(["Process", "Material", "Efficiency kg/h"], 2):
            self.processTable.column(f"# {i}", anchor=tk.CENTER, width=160)
            self.processTable.heading(f"# {i}", text=col_heading)
        for i in control.get_table_data("Process"):
            self.processTable.insert(
                "", "end", values=(i.id, i.name, i.materials.name, i.efficiency)
            )
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(command=self.edit_process_get_values, text="Edit")

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
        self.buttonEdit.config(
            text="Save changes", activebackground="#00A650", command=self.edit_process
        )
        self.buttonDelete.config(state=tk.DISABLED, bg="gray")
        self.entryFieldEdit1.grid(row=1, column=8)
        self.entryFieldEdit2.grid(row=2, column=8)
        self.entryFieldEdit3.grid(row=3, column=8)
        self.buttonCancelEditing.grid(row=3, column=6)
        self.buttonCancelEditing.config(
            activebackground="red", command=self.cancel_editing_process
        )
        self.entryFieldEdit1.focus()

    def edit_process_get_values(self):
        """
        Paima pasirinkto Process įrašo vertes redagavimui
        """
        try:
            self.edit_record_process()
            selection = self.processTable.item(self.processTable.focus())
            selection = selection["values"]
            self.idForEdit.set(selection[0])
            self.entryFieldEdit1.insert(0, selection[1])
            self.entryFieldEdit2.insert(0, selection[2])
            self.entryFieldEdit3.insert(0, selection[3])
        except IndexError:
            logging.warning("No record selected when trying to edit process")
            self.fill_process_data_box()

    def edit_process(self):
        """
        Redaguoja Process įrašą jei jis turi pavadinimą, jis nesikartoja ir našumas daugiau nei 0,
        ir įrašo vertes į DB. Kitu atveju meta ERROR
        """
        selected_field = control.get_record_by_id("Process", self.idForEdit.get())
        selected_field_name = selected_field.name
        selected_field_material = selected_field.materials.name
        entered_process = self.entryFieldEdit1.get().strip()
        entered_process = re.sub(" +", " ", entered_process)
        entered_material = self.entryFieldEdit2.get().strip()
        entered_material = re.sub(" +", " ", entered_material)
        if any(i.isalpha() or i.isdigit() for i in entered_process):
            if entered_process.lower() not in [
                i.lower()
                for i in control.check_for_duplicates_process()
                if i != selected_field_name
            ]:
                if any(i.isalpha() or i.isdigit() for i in entered_material):
                    if entered_material.lower() not in [
                        i.lower()
                        for i in control.check_for_duplicates_materials()
                        if i != selected_field_material
                    ]:
                        try:
                            entered_efficiency = float(self.entryFieldEdit3.get())
                            if entered_efficiency > 0:
                                control.update_process(
                                    self.idForEdit.get(),
                                    entered_process,
                                    entered_efficiency,
                                )
                                control.update_material(
                                    self.idForEdit.get(), entered_material
                                )
                                self.fill_process_data_box()
                            else:
                                logging.error(
                                    "Efficiency input was less than 0 when trying to edit a process"
                                )
                                ErrorWindow("Efficiency must be more than 0!")
                        except ValueError:
                            logging.error(
                                "Efficiency value was not a number when trying to edit a process"
                            )
                            ErrorWindow("Efficiency must be a number!")
                    else:
                        logging.error(
                            "Entered a duplicate material name when editing process record"
                        )
                        ErrorWindow("Material with that name already exists!")
                else:
                    logging.error(
                        "No material name entered when editing process record"
                    )
                    ErrorWindow("No material name entered!")
            else:
                logging.error("Entered a duplicate name when editing process record")
                ErrorWindow("Process record with that name already exists!")
        else:
            logging.error("No process name entered when trying to edit a process")
            ErrorWindow("No name entered!")

    def cancel_editing_process(self):
        """
        Atšaukia Process įrašo redagavimą
        """
        self.cancel_editing()
        self.buttonEdit.config(
            text="Edit",
            activebackground="#75C1BF",
            command=self.edit_process_get_values,
        )
