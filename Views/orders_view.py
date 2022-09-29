from utils import *
from datetime import datetime


class OrderViews:
    def fill_orders_data_box(self):
        """
        Atstato pradinę lango būseną su Orders duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.ordersTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.ordersTable.get_children():
            self.ordersTable.delete(i)
        for i, col_heading in enumerate(
            ["ID", "Date", "Recipe", "Amount, kg", "Manufacturing Cost", "Selling price"], 1
        ):
            self.ordersTable.column(f"# {i}", anchor=tk.CENTER, width=120)
            self.ordersTable.heading(f"# {i}", text=col_heading)
        self.currency_list.bind('<<ComboboxSelected>>', self.refresh_orders)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in Control.get_orders_data():
            self.ordersTable.insert(
                "",
                "end",
                values=(
                    i.id,
                    i.date,
                    i.recipe_info.name,
                    round((i.amount * rate), 2),
                    round((i.man_cost * rate), 2),
                    round((i.sell_price * rate), 2),
                ),
            )
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(state=tk.DISABLED, bg="gray")

    def refresh_orders(self, event):
        for i in self.ordersTable.get_children():
            self.ordersTable.delete(i)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in Control.get_orders_data():
            self.ordersTable.insert(
                "",
                "end",
                values=(
                    i.id,
                    i.date,
                    i.recipe_info.name,
                    i.amount,
                    round((i.man_cost * rate), 2),
                    round((i.sell_price * rate), 2),
                ),
            )

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
        self.recipe_list.place(x=330, y=170)
        self.buttonAddOrder.place_forget()
        self.entryFieldOrder.place(x=590, y=170)
        self.labelOrder.place(x=589, y=130)
        self.labelRecipe.place(x=330, y=130)
        self.buttonConfirmOrder.place(x=895, y=110)
        self.buttonCancelOrder.place(x=895, y=191)

    def cancel_order(self):
        """
        Atšaukia užsakymo pridėjimą, pašalina ir išvalo laukus
        """
        self.buttonAddOrder.place(x=585, y=130)
        self.entryFieldOrder.place_forget()
        self.entryFieldOrder.delete(0, tk.END)
        self.labelOrder.place_forget()
        self.labelRecipe.place_forget()
        self.buttonCancelOrder.place_forget()
        self.buttonConfirmOrder.place_forget()
        self.recipe_list.place_forget()
        self.recipe_list.set("")

    def recipe_calculation(self):
        """
        Tikrina ar pasirinktas receptas, tada ar užsakymo vertė daugiau už 0,
        jei taip, skaičiuoja iš recepto reikalingą žaliavų dalį, jei ne meta ERROR
        """
        try:
            if self.recipe_list.get() != "":
                if float(self.entryFieldOrder.get()) > 0:
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
                        selected_recipe, float(self.entryFieldOrder.get())
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

    def calculate_required_materials(self, selected_recipe, order_amount):
        """
        Skaičiuoja reikiamą žaliavų kiekį užsakymui įvykdyti
        :param selected_recipe: pasirinktas receptas užsakymui
        :param order_amount: užsakymo dydis
        """
        required_materials = [i * order_amount for i in selected_recipe]
        self.calculate_storage_remainder(required_materials)

    def calculate_storage_remainder(self, required_materials):
        storage = Control.get_storage_amount()
        storage_list = []
        for i in storage:
            storage_list.append(i[0])
        storage_remaining = [i - j for (i, j) in zip(storage_list, required_materials)]
        self.order_calculation(storage_remaining)

    def order_calculation(self, storage_remaining):
        """
        Tikrina ar sandėlio žaliavų likutis yra neigiamas, jei taip, apskaičiuoja
        kiek reikės darbo valandų kad pasiekti teigiamą kiekį, jei ne, surašo į DB
        :param storage_remaining: priima sandėlio likutį
        """
        num = 0
        if min(storage_remaining) < 0:
            efficiency = Control.get_process_efficiency()
            efficiency_list = []
            for i in efficiency:
                efficiency_list.append(i[0])
            check_remainder = [
                i + j for (i, j) in zip(efficiency_list, storage_remaining)
            ]
            while min(check_remainder) < 0:
                check_remainder = [
                    i + j for (i, j) in zip(efficiency_list, check_remainder)
                ]
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
            recipe = (
                Control.session.query(Control.Recipe)
                .filter_by(name=self.recipe_list.get())
                .one()
            )
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_id = recipe.id
            recipe_amount = float(self.entryFieldOrder.get())
            prices = Control.get_material_price_list()
            man_cost = round(sum([i * recipe_amount for i in prices]), 2)
            sell_price = round((man_cost * 1.3), 2)
            Control.add_order(
                order_date, recipe_id, recipe_amount, man_cost, sell_price
            )
            Control.session.commit()
