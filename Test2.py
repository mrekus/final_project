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


def fill_process_data_box():
    """
    Atstato pradinę lango būseną su Process duomenų lentele
    """
    default_button_layouts()
    forget_tables()
    processTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
    for i in processTable.get_children():
        processTable.delete(i)
    for i, col_heading in enumerate(
        ["ID", "Process", "Material", "Efficiency kg/h"], 1
    ):
        processTable.column(f"# {i}", anchor=CENTER, width=90)
        processTable.heading(f"# {i}", text=col_heading)
    for i in get_process_data():
        processTable.insert(
            "", "end", values=(i.id, i.name, i.produced_material, i.efficiency)
        )
    buttonAddRecipe.grid_forget()
    buttonEdit.config(command=edit_process_get_values, text="Edit")


def fill_recipe_data_box():
    """
    Atstato pradinę lango būseną su Recipe duomenų lentele
    """
    default_button_layouts()
    forget_tables()
    headings = check_for_duplicates_storage()
    recipeTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
    for i in recipeTable.get_children():
        recipeTable.delete(i)
    for i, col_heading in enumerate(
        [
            "ID",
            "Recipe",
            headings[0],
            headings[1],
            headings[2],
            headings[3],
            headings[4],
        ],
        1,
    ):
        recipeTable.column(f"# {i}", anchor=CENTER, width=90)
        recipeTable.heading(f"# {i}", text=col_heading)
    for i in get_recipe_data():
        recipeTable.insert(
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
    buttonDelete.config(state=NORMAL, bg="red")
    buttonAddRecipe.grid(row=3, column=6)
    buttonEdit.config(command=edit_recipies_get_values, text="Edit")


def fill_storage_data_box():
    """
    Atstato pradinę lango būseną su Storage duomenų lentele
    """
    default_button_layouts()
    forget_tables()
    storageTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=NSEW)
    for i in storageTable.get_children():
        storageTable.delete(i)
    for i, col_heading in enumerate(["ID", "Name", "Amount kg"], 1):
        storageTable.column(f"# {i}", anchor=CENTER, width=90)
        storageTable.heading(f"# {i}", text=col_heading)
    for i in get_storage_data():
        storageTable.insert("", "end", values=(i.id, i.name, i.amount))
    buttonAddRecipe.grid_forget()
    buttonEdit.config(command=edit_storage_get_values, text="Edit")


def default_button_layouts():
    """
    Atstato pradinius mygtukų išdėstymus, išvalo EDIT laukus
    """
    buttonEdit.grid(row=1, column=6)
    buttonDelete.grid(row=2, column=6)
    buttonDelete.config(state=DISABLED, bg="gray")
    cancel_editing()


def edit_record_process():
    """
    Sukuria visus Process edit langus
    """
    labelEdit1.grid(row=1, column=7, sticky="W")
    labelEdit2.grid(row=2, column=7, sticky="W")
    labelEdit3.grid(row=3, column=7, sticky="W")
    labelEdit1.config(text="Name: ")
    labelEdit2.config(text="Material: ")
    labelEdit3.config(text="Efficiency: ")
    buttonEdit.config(text="Save changes", command=edit_process)
    buttonDelete.config(state=DISABLED, bg="gray")
    entryFieldEdit1.grid(row=1, column=8)
    entryFieldEdit2.grid(row=2, column=8)
    entryFieldEdit3.grid(row=3, column=8)
    buttonCancelEditing.grid(row=3, column=6)
    buttonCancelEditing.config(command=cancel_editing_process)
    entryFieldEdit1.focus()


def edit_record_storage():
    """
    Sukuria visus Storage edit langus
    """
    edit_record_process()
    buttonEdit.config(text="Save changes", command=edit_storage)
    labelEdit1.grid(row=1, column=7, sticky="W")
    labelEdit2.grid(row=2, column=7, sticky="W")
    labelEdit1.config(text="Name: ")
    labelEdit2.config(text="Ammount: ")
    buttonCancelEditing.config(command=cancel_editing_storage)
    labelEdit3.grid_forget()
    entryFieldEdit3.grid_forget()


def edit_record_recipies():
    """
    Sukuria visus Recipies edit langus
    """
    edit_record_process()
    buttonEdit.config(text="Save changes", command=edit_recipe)
    labelEdit4.grid(row=1, column=9, sticky="W")
    labelEdit5.grid(row=2, column=9, sticky="W")
    labelEdit6.grid(row=3, column=9, sticky="W")
    labelEdit2.config(text="Material 1: ")
    labelEdit3.config(text="Material 2: ")
    labelEdit4.config(text="Material 3: ")
    labelEdit5.config(text="Material 4: ")
    labelEdit6.config(text="Material 5: ")
    entryFieldEdit4.grid(row=1, column=10)
    entryFieldEdit5.grid(row=2, column=10)
    entryFieldEdit6.grid(row=3, column=10)
    buttonCancelEditing.config(command=cancel_editing_recipies)


def cancel_editing():
    """
    Pašalina visus Edit langus ir juos išvalo
    """
    entryFieldEdit1.grid_forget()
    entryFieldEdit2.grid_forget()
    entryFieldEdit3.grid_forget()
    entryFieldEdit4.grid_forget()
    entryFieldEdit5.grid_forget()
    entryFieldEdit6.grid_forget()
    labelEdit1.grid_forget()
    labelEdit2.grid_forget()
    labelEdit3.grid_forget()
    labelEdit4.grid_forget()
    labelEdit5.grid_forget()
    labelEdit6.grid_forget()
    buttonCancelEditing.grid_forget()
    reset_entry_fields()
    buttonDelete.config(state=DISABLED, bg="gray")


def forget_tables():
    """Pašalina visas duomenų lenteles"""
    processTable.grid_forget()
    recipeTable.grid_forget()
    storageTable.grid_forget()


def delete_record():
    """
    Ištrina pasirinktą recepto įrašą
    """
    try:
        selection = recipeTable.item(recipeTable.focus())
        deletion_id = str(selection).replace("]", "[")
        deletion_id = deletion_id.replace(" ", "")
        deletion_id = deletion_id.split("[")
        deletion_id = deletion_id[1]
        deletion_id = int(deletion_id[0])
        delete_recipe_record(deletion_id)
        fill_recipe_data_box()
        refresh_recipe_list()
    except IndexError:
        logging.warning("No record selected when trying to delete recipe!")
        fill_recipe_data_box()


def reset_entry_fields():
    """
    Išvalo visus Edit įrašų laukus
    """
    entryFieldEdit1.delete(0, END)
    entryFieldEdit2.delete(0, END)
    entryFieldEdit3.delete(0, END)
    entryFieldEdit4.delete(0, END)
    entryFieldEdit5.delete(0, END)
    entryFieldEdit6.delete(0, END)
    entryFieldEdit1.focus()


def add_record_recipies():
    """
    Atidaro naujo Recipies įrašo pridėjimo laukus, pakeičia Edit
    mygtuką į Save
    """
    edit_record_recipies()
    buttonEdit.config(command=gui_add_recipe)


def gui_add_recipe():
    """
    Prideda naują receptą į DB jei jis turi pavadinimą, ir medžiagų dalių suma yra 1,
    klaidos atveju meta ERROR
    """
    if entryFieldEdit1.get().lower().replace(" ", "") not in [
        i.lower().replace(" ", "") for i in check_for_duplicates_recipe()
    ]:
        if any(i.isalpha() or i.isdigit() for i in entryFieldEdit1.get()):
            try:
                check_values = [
                    float(entryFieldEdit2.get()),
                    float(entryFieldEdit3.get()),
                    float(entryFieldEdit4.get()),
                    float(entryFieldEdit5.get()),
                    float(entryFieldEdit6.get()),
                ]
                if (
                    all(0 <= i <= 1 for i in check_values)
                    and round(sum(check_values), 3) == 1
                ):
                    add_recipe(
                        entryFieldEdit1.get(),
                        entryFieldEdit2.get(),
                        entryFieldEdit3.get(),
                        entryFieldEdit4.get(),
                        entryFieldEdit5.get(),
                        entryFieldEdit6.get(),
                    )
                    fill_recipe_data_box()
                    refresh_recipe_list()
                else:
                    logging.error(
                        "Material sum not equal to 1 when trying to add new recipe"
                    )
                    error_popup("Material sum must amount to 1!")
            except ValueError:
                logging.error(
                    "Wrong material values input when trying to add new recipe"
                )
                error_popup("Material inputs are not numbers, or are not filled!")
        else:
            logging.error("No name input when trying to add new recipe")
            error_popup("No name entered!")
    else:
        logging.error("Entered a duplicate name when adding new recipe")
        error_popup("Recipe with that name already exists!")


def edit_process_get_values():
    """
    Paima pasirinkto Process įrašo vertes redagavimui
    """
    try:
        edit_record_process()
        selection = processTable.item(processTable.focus())
        record = str(selection).replace("]", "[")
        record = record.split("[")
        record = record[1]
        idForEdit.set(int(record[0]))
        record = record.replace("'", "")
        record = record.split(",")
        entryFieldEdit1.insert(0, record[1][1::])
        entryFieldEdit2.insert(0, record[2][1::])
        entryFieldEdit3.insert(0, record[3][1::])
    except IndexError:
        logging.warning("No record selected when trying to edit process")
        fill_process_data_box()


def edit_process():
    """
    Redaguoja Process įrašą jei jis turi pavadinimą, jis nesikartoja ir našumas daugiau nei 0,
    ir įrašo vertes į DB. Kitu atveju meta ERROR
    """
    selected_field = session.query(Process).get(idForEdit.get())
    selected_field_name = selected_field.name
    selected_field_material = selected_field.produced_material
    if any(i.isalpha() or i.isdigit() for i in entryFieldEdit1.get()):
        if entryFieldEdit1.get().lower().replace(" ", "") not in [
            i.lower().replace(" ", "")
            for i in check_for_duplicates_process()
            if i != selected_field_name
        ]:
            if entryFieldEdit2.get().lower().replace(" ", "") not in [
                i.lower().replace(" ", "")
                for i in check_for_duplicates_storage()
                if i != selected_field_material
            ]:
                try:
                    if float(entryFieldEdit3.get()) > 0:
                        update_process(
                            idForEdit.get(),
                            entryFieldEdit1.get(),
                            entryFieldEdit2.get(),
                            entryFieldEdit3.get(),
                        )
                        update_storage_material_from_process(
                            idForEdit.get(), entryFieldEdit2.get()
                        )
                        fill_process_data_box()
                    else:
                        logging.error(
                            "Efficiency input was less than 0 when trying to edit a process"
                        )
                        error_popup("Efficiency must be more than 0!")
                except ValueError:
                    logging.error(
                        "Efficiency value was not a number when trying to edit a process"
                    )
                    error_popup("Efficiency must be a number!")
            else:
                logging.error(
                    "Entered a duplicate material name when editing process record"
                )
                error_popup("Process record with that material name already exists!")
        else:
            logging.error("Entered a duplicate name when editing process record")
            error_popup("Process record with that name already exists!")
    else:
        logging.error("No process name entered when trying to edit a process")
        error_popup("No name entered!")


def cancel_editing_process():
    """
    Atšaukia Process įrašo redagavimą
    """
    cancel_editing()
    buttonEdit.config(text="Edit", command=edit_process_get_values)


def edit_recipies_get_values():
    """
    Pasiima pasirinkto Recipies įrašo vertes redagavimui
    """
    try:
        edit_record_recipies()
        selection = recipeTable.item(recipeTable.focus())
        record = str(selection).replace("]", "[")
        record = record.split("[")
        record = record[1]
        idForEdit.set(int(record[0]))
        record = record.replace("'", "")
        record = record.split(",")
        entryFieldEdit1.insert(0, record[1][1::])
        entryFieldEdit2.insert(0, record[2][1::])
        entryFieldEdit3.insert(0, record[3][1::])
        entryFieldEdit4.insert(0, record[4][1::])
        entryFieldEdit5.insert(0, record[5][1::])
        entryFieldEdit6.insert(0, record[6][1::])
    except IndexError:
        logging.warning("No record selected when trying to edit a recipe")
        fill_recipe_data_box()


def edit_recipe():
    """
    Redaguoja Recipies įrašą jei jis turi pavadinimą, ar jis nesikartoja,
     ir ar medžiagų dalių suma yra 1, ir prideda jį į DB. Klaidos atveju meta ERROR.
    :return:
    """
    selected_field = session.query(Recipe).get(idForEdit.get())
    selected_field = selected_field.name
    if any(i.isalpha() or i.isdigit() for i in entryFieldEdit1.get()):
        if entryFieldEdit1.get().lower().replace(" ", "") not in [
            i.lower().replace(" ", "")
            for i in check_for_duplicates_recipe()
            if i != selected_field
        ]:
            try:
                check_values = [
                    float(entryFieldEdit2.get()),
                    float(entryFieldEdit3.get()),
                    float(entryFieldEdit4.get()),
                    float(entryFieldEdit5.get()),
                    float(entryFieldEdit6.get()),
                ]
                if (
                    all((0 <= i <= 1) for i in check_values)
                    and round(sum(check_values), 3) == 1
                ):
                    update_recipe(
                        idForEdit.get(),
                        entryFieldEdit1.get(),
                        entryFieldEdit2.get(),
                        entryFieldEdit3.get(),
                        entryFieldEdit4.get(),
                        entryFieldEdit5.get(),
                        entryFieldEdit6.get(),
                    )
                    fill_recipe_data_box()
                    refresh_recipe_list()
                else:
                    logging.error(
                        "Material sum was not equal to 1 or were negative when trying to edit a recipe"
                    )
                    error_popup(
                        "Material sum must amount to 1 and material values must be positive!"
                    )
            except ValueError:
                logging.error(
                    "Wrong material values input when trying to edit a recipe"
                )
                error_popup("Material inputs must be numbers!")
        else:
            logging.error("Entered a duplicate name when editing recipe record")
            error_popup("Recipe record with that name already exists!")
    else:
        logging.error("No recipe name entered when trying to edit a recipe")
        error_popup("No name entered!")


def cancel_editing_recipies():
    """
    Atšaukia Recipies įrašo redagavimą ir pašalina laukus
    """
    cancel_editing()
    buttonDelete.config(state=NORMAL, bg="red")
    buttonEdit.config(command=edit_recipies_get_values, text="Edit")


def edit_storage_get_values():
    """
    Paima pasirinkto Storage įrašo vertes redagavimui
    """
    try:
        edit_record_storage()
        selection = storageTable.item(storageTable.focus())
        record = str(selection).replace("]", "[")
        record = record.split("[")
        record = record[1]
        idForEdit.set(int(record[0]))
        record = record.replace("'", "")
        record = record.split(",")
        entryFieldEdit1.insert(0, record[1][1::])
        entryFieldEdit2.insert(0, record[2][1::])
    except IndexError:
        logging.warning("No record selected when trying to edit a storage record")
        fill_storage_data_box()


def edit_storage():
    """
    Tikrina redaguojamą Storage įrašą ar jis turi pavadinimą, tada ar jis nesikartoja
    ir ar reikšmės didesnės už 0, jei taip, redaguotą įrašą išsaugo, jei ne meta ERROR.
    Taip pat pakeičia procesų DB material pavadinimą
    """
    selected_field = session.query(Storage).get(idForEdit.get())
    selected_field = selected_field.name
    if any(i.isalpha() or i.isdigit() for i in entryFieldEdit1.get()):
        if entryFieldEdit1.get().lower().replace(" ", "") not in [
            i.lower().replace(" ", "")
            for i in check_for_duplicates_storage()
            if i != selected_field
        ]:
            try:
                if float(entryFieldEdit2.get()) > 0:
                    update_storage(
                        idForEdit.get(), entryFieldEdit1.get(), entryFieldEdit2.get()
                    )
                    update_process_material_from_storage(
                        idForEdit.get(), entryFieldEdit1.get()
                    )
                    fill_storage_data_box()
                else:
                    logging.error(
                        "Material amount entered was less than 0 when trying to edit a storage record"
                    )
                    error_popup("Amount must be more than 0!")
            except ValueError:
                logging.error(
                    "Wrong material values input when trying to edit a storage record"
                )
                error_popup("Amount must be a number!")
        else:
            logging.error("Entered a duplicate name when editing storage record")
            error_popup("Storage record with that name already exists!")
    else:
        logging.error("No name entered when trying to edit a storage record")
        error_popup("No name entered!")


def cancel_editing_storage():
    """
    Atšaukia Storage įrašo redagavimą ir atstato laukus
    """
    cancel_editing()
    buttonEdit.config(text="Edit", command=edit_storage_get_values)


def refresh_recipe_list():
    """
    Atjauniną receptų sąrašą
    """
    recipe_list.config(values=check_for_duplicates_recipe())
    recipe_list.set("")


def order_adding_widgets():
    """
    Sukuria užsakymo pridėjimo laukus ir atnaujina receptų sąrašą
    """
    refresh_recipe_list()
    recipe_list.grid(row=1, column=0)
    buttonAddOrder.grid_forget()
    entryFieldOrder.grid(row=1, column=1)
    labelOrder.grid(row=0, column=1)
    buttonConfirmOrder.grid(row=1, column=2)
    buttonCancelOrder.grid(row=1, column=3)


def cancel_order():
    """
    Atšaukia užsakymo pridėjimą, pašalina ir išvalo laukus
    """
    buttonAddOrder.grid(row=1, column=0)
    entryFieldOrder.grid_forget()
    entryFieldOrder.delete(0, END)
    labelOrder.grid_forget()
    buttonCancelOrder.grid_forget()
    buttonConfirmOrder.grid_forget()
    recipe_list.grid_forget()
    recipe_list.set("")


def order_calculation():
    """
    Tikrina ar pasirinktas receptas, tada ar užsakymo vertė daugiau už 0,
    jei taip, skaičiuoja reikiamą žaliavų kiekį, jei ne meta ERROR
    """
    try:
        if recipe_list.get() != "":
            if int(entryFieldOrder.get()) > 0:
                selected_recipe = str(
                    session.query(Recipe).filter_by(name=recipe_list.get()).one()
                )
                selected_recipe = selected_recipe.replace(" ", "")
                selected_recipe = selected_recipe.replace(";", "-")
                selected_recipe = selected_recipe.split("-")
                del selected_recipe[0]
                selected_recipe = [float(i) for i in selected_recipe]
                calculate_required_materials(
                    selected_recipe, int(entryFieldOrder.get())
                )
                fill_storage_data_box()
                cancel_order()
            else:
                logging.error(
                    "Order amount entered was less than 0 when trying to submit an order"
                )
                error_popup("Order amount must be more than 0!")
        else:
            logging.error("No recipe chosen when trying to submit an order")
            error_popup("No recipe chosen!")
    except ValueError:
        logging.error("Wrong value type entered when trying to add an order")
        error_popup("Amount is not a number!")


def calculate_required_materials(selected_recipe, entry):
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
    check_storage_remainder(storage_remaining)


def check_storage_remainder(storage_remaining):
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
        error_popup(
            f"Not enough materials to complete the order,\n it will take {num} working hours to get enough material "
        )
        with open("orders.txt", "a", encoding="utf-8") as record_order:
            record_order.write(
                f"{datetime.now()} - Order of {recipe_list.get()} - {entryFieldOrder.get()}kg could not be "
                f"completed, not enough materials. It will take {num} working hours to complete this order.\n"
            )
    else:
        record_id = 1
        with open("orders.txt", "a", encoding="utf-8") as record_order:
            record_order.write(
                f"{datetime.now()} - Order of {recipe_list.get()} - {entryFieldOrder.get()}kg completed.\n"
            )
        for i in storage_remaining:
            record = session.query(Storage).get(record_id)
            record.amount = round(i, 1)
            record_id += 1
        session.commit()


def back_to_main():
    """
    Grąžina programą į pradinę būseną
    """
    default_button_layouts()
    forget_tables()
    cancel_order()
    buttonEdit.grid_forget()
    buttonDelete.grid_forget()
    buttonCancelEditing.grid_forget()
    buttonAddRecipe.grid_forget()


def error_popup(text):
    """
    Iššaukia ERROR langą su tekstu
    :param text: priima error lango tekstą
    """
    error_window = Toplevel()
    error_window.geometry("+900+500")
    error_window.title("Error")
    frame = Frame(error_window)
    error_text = Label(frame, text=text, anchor=CENTER, font=("courier", 25, "bold"))
    ok_button = Button(
        frame,
        text="Confirm",
        command=error_window.destroy,
        anchor=CENTER,
        bg="white",
        fg="black",
        font=("courier", 12, "bold"),
        relief="groove",
        height=1,
        width=15,
        activebackground="#0a0a0a",
        activeforeground="#e6d415",
    )
    error_text.grid(row=0, column=1)
    ok_button.grid(row=1, column=1)
    frame.pack(expand=True)
    window.bell()


window = Tk()
logging.basicConfig(
    filename="Project_error_log.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="UTF-8",
)

window.geometry("1570x550+400+400")
window.resizable(False, False)
window.title("Control panel")
style = ttk.Style()
style.theme_use("clam")

gradient_step = 0
hex_step = 400
for _ in range(40):
    color_hex = str(224499 + hex_step)
    Frame(window, width=100, height=550, bg="#" + color_hex).place(x=gradient_step, y=0)
    gradient_step += 100
    hex_step += 300

idForEdit = IntVar()

topFrame = Frame(window)
leftFrame = Frame(window)

menu = Menu(window)
window.config(menu=menu)
submenu = Menu(menu, tearoff=False)

buttonAddOrder = Button(
    topFrame,
    text="Add an Order",
    height=3,
    width=20,
    anchor=CENTER,
    bg="white",
    fg="black",
    font=("courier", 20, "bold"),
    relief="groove",
    command=order_adding_widgets,
    activebackground="#0a0a0a",
    activeforeground="#e6d415",
)
buttonProcesses = MyButton(leftFrame, text="Processes", command=fill_process_data_box)
buttonRecipies = MyButton(leftFrame, text="Recipies", command=fill_recipe_data_box)
buttonStorage = MyButton(leftFrame, text="Storage", command=fill_storage_data_box)
buttonEdit = MyButton(leftFrame, text="Edit")
buttonDelete = Button(
    leftFrame,
    text="Delete",
    bg="red",
    fg="black",
    font=("courier", 12),
    height=3,
    width=15,
    command=delete_record,
)
buttonAddRecipe = MyButton(leftFrame, text="Add Recipe", command=add_record_recipies)
buttonCancelEditing = MyButton(leftFrame, text="Cancel", command=cancel_editing)
buttonCancelOrder = Button(
    topFrame,
    text="Cancel Order",
    height=3,
    width=20,
    anchor=CENTER,
    bg="red",
    fg="black",
    font=("courier", 14, "bold"),
    relief="groove",
    command=cancel_order,
)
buttonConfirmOrder = Button(
    topFrame,
    text="Confirm Order",
    height=3,
    width=20,
    anchor=CENTER,
    bg="white",
    fg="black",
    font=("courier", 14, "bold"),
    relief="groove",
    command=order_calculation,
    activebackground="#0a0a0a",
    activeforeground="#e6d415",
)
labelEdit1 = MyLabel(leftFrame)
labelEdit2 = MyLabel(leftFrame)
labelEdit3 = MyLabel(leftFrame)
labelEdit4 = MyLabel(leftFrame)
labelEdit5 = MyLabel(leftFrame)
labelEdit6 = MyLabel(leftFrame)
labelOrder = Label(
    topFrame, text="Amount in kg:", font=("courier", 25, "bold"), width=15
)
entryFieldEdit1 = MyEntry(leftFrame)
entryFieldEdit2 = MyEntry(leftFrame)
entryFieldEdit3 = MyEntry(leftFrame)
entryFieldEdit4 = MyEntry(leftFrame)
entryFieldEdit5 = MyEntry(leftFrame)
entryFieldEdit6 = MyEntry(leftFrame)
entryFieldOrder = Entry(topFrame, font=("courier", 25, "bold"), width=15)
recipe_list = ttk.Combobox(
    topFrame, width=12, font=("courier", 25, "bold"), state="readonly"
)
processTable = ttk.Treeview(
    leftFrame,
    columns=("id", "Process", "Material", "Efficiency kg/h"),
    show="headings",
    height=8,
)
recipeTable = ttk.Treeview(
    leftFrame,
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
storageTable = ttk.Treeview(
    leftFrame, columns=("id", "Name", "Amount kg"), show="headings", height=8
)

menu.add_cascade(label="Menu", menu=submenu)
submenu.add_command(label="Back to main", command=back_to_main)
submenu.add_separator()
submenu.add_command(label="Exit", command=window.destroy)

buttonAddOrder.grid(row=0, column=0)
buttonProcesses.grid(row=1, column=1)
buttonRecipies.grid(row=2, column=1)
buttonStorage.grid(row=3, column=1)
topFrame.pack(side=TOP, expand=True)
leftFrame.pack(side=LEFT)

window.mainloop()
