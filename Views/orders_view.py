from utils import *
from datetime import datetime


class OrderViews:
    def refresh_recipe_list(self):
        """
        Atjauniną receptų sąrašą
        """
        self.recipe_list.config(values=Control.check_for_duplicates_recipe())
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
        self.entryFieldOrder.delete(0, tk.END)
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
                    selected_recipe = str(
                        Control.session.query(Control.Recipe)
                        .filter_by(name=self.recipe_list.get())
                        .one()
                    )
                    selected_recipe = selected_recipe.replace(" ", "")
                    selected_recipe = selected_recipe.replace(";", "-")
                    selected_recipe = selected_recipe.split("-")
                    del selected_recipe[0]
                    selected_recipe = [float(i) for i in selected_recipe]
                    self.calculate_required_materials(
                        selected_recipe, int(self.entryFieldOrder.get())
                    )
                    self.fill_storage_data_box()
                    self.cancel_order()
                else:
                    logging.error(
                        "Order amount entered was less than 0 when trying to submit an order"
                    )
                    ErrorWindow("Order amount must be more than 0!")
            else:
                logging.error("No recipe chosen when trying to submit an order")
                ErrorWindow("No recipe chosen!")
        except ValueError:
            logging.error("Wrong value type entered when trying to add an order")
            ErrorWindow("Amount is not a number!")

    def calculate_required_materials(self, selected_recipe, entry):
        """
        Skaičiuoja reikiamą žaliavų kiekį užsakymui įvykdyti
        :param selected_recipe: pasirinktas receptas užsakymui
        :param entry: užsakymo dydis
        """
        required_materials = [i * entry for i in selected_recipe]
        storage = Control.get_storage_amount()
        storage_list = []
        for i in storage:
            storage_list.append(i[0])
        storage_remaining = [i - j for (i, j) in zip(storage_list, required_materials)]
        self.check_storage_remainder(storage_remaining)

    def check_storage_remainder(self, storage_remaining):
        """
        Tikrina ar sandėlio žaliavų likutis yra neigiamas, jei taip, apskaičiuoja
        kiek reikės darbo valandų kad pasiekti teigiamą kiekį, jei ne, surašo į DB
        :param storage_remaining: priima sandėlio likutį
        """
        num = 0
        if min(storage_remaining) < 0:
            print(storage_remaining)
            efficiency = Control.get_process_efficiency()
            efficiency_list = []
            for i in efficiency:
                efficiency_list.append(i[0])
            check_remainder = [i + j for (i, j) in zip(efficiency_list, storage_remaining)]
            num = 1
            while min(check_remainder) < 0:
                check_remainder = [i + j for (i, j) in zip(efficiency_list, check_remainder)]
                num += 1
            logging.critical("Not enough material in storage to complete an order")
            ErrorWindow(
                f"Not enough materials to complete the order,\n"
                f"it will take {num} working hours to get enough material"
            )
            with open("orders.txt", "a", encoding="utf-8") as record_order:
                record_order.write(
                    f"{datetime.now()} - Order of {self.recipe_list.get()} - {self.entryFieldOrder.get()}kg could not "
                    f"be completed, not enough materials. It will take {num} working hours to complete this order.\n"
                )
        else:
            with open("orders.txt", "a", encoding="utf-8") as record_order:
                record_order.write(
                    f"{datetime.now()} - Order of {self.recipe_list.get()} - "
                    f"{self.entryFieldOrder.get()}kg completed.\n"
                )
            record_id = 1
            for i in storage_remaining:
                record = Control.session.query(Control.Storage).get(record_id)
                record.amount = round(i, 1)
                record_id += 1
            recipe = Control.session.query(Control.Recipe).filter_by(name=self.recipe_list.get()).one()
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_id = recipe.id
            recipe_amount = self.entryFieldOrder.get()
            Control.add_order(order_date, recipe_id, recipe_amount)
            Control.session.commit()
