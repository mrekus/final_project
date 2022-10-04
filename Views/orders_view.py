import tkinter

from utils import *
from datetime import datetime
from Control import send_email


def write_order_to_txt(text):
    with open("orders.txt", "a", encoding="utf-8") as record_order:
        record_order.write(text)


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
            [
                "ID",
                "Date",
                "Recipe",
                "Amount, kg",
                "Manufacturing Cost",
                "Selling price",
            ],
            1,
        ):
            self.ordersTable.column(f"# {i}", anchor=tk.CENTER, width=120)
            self.ordersTable.heading(f"# {i}", text=col_heading)
        self.currency_list.bind("<<ComboboxSelected>>", self.refresh_orders)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in control.get_table_data("Orders"):
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
        self.buttonAddRecipe.grid_forget()
        self.buttonEdit.config(state=tk.DISABLED, bg="gray")
        self.buttonFilterOrders.grid(row=3, column=6)
        self.buttonFilterOrders.config(
            text="Filter", command=self.filter_orders_buttons
        )

    def refresh_orders(self, event):
        """
        Atnaujina Orders lentelės įrašus
        :param event: aktyvuojamas currency combobox pasikeitimu
        """
        for i in self.ordersTable.get_children():
            self.ordersTable.delete(i)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in control.get_table_data("Orders"):
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
        Atjauniną receptų combobox sąrašą
        """
        self.recipe_list.config(values=control.check_for_duplicates_recipe())
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
        jei taip, paima iš recepto reikalingą žaliavų dalį, jei ne meta ERROR
        """
        try:
            order_amount = float(self.entryFieldOrder.get())
            selected_recipe = self.recipe_list.get()
            if selected_recipe != "":
                if order_amount > 0:
                    recipe_data = control.get_recipe_materials_list(selected_recipe)
                    self.calculate_required_materials(recipe_data, order_amount)
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
            ErrorWindow("Wrong value type entered!")

    def calculate_required_materials(self, selected_recipe, order_amount):
        """
        Skaičiuoja reikiamą žaliavų kiekį užsakymui įvykdyti
        :param selected_recipe: pasirinktas receptas užsakymui
        :param order_amount: užsakymo dydis
        """
        required_materials = [i * order_amount for i in selected_recipe]
        self.calculate_storage_remainder(required_materials)

    def calculate_storage_remainder(self, required_materials):
        storage = control.get_storage_amount()
        storage_list = []
        for i in storage:
            storage_list.append(i[0])
        storage_remaining = [i - j for (i, j) in zip(storage_list, required_materials)]
        self.order_calculation(storage_remaining)

    def order_calculation(self, storage_remaining):
        """
        Tikrina ar sandėlio žaliavų likutis yra neigiamas, jei taip, apskaičiuoja
        kiek reikės darbo valandų kad pasiekti teigiamą kiekį, jei ne, surašo į DB
        ir išsiunčia laišką su užsakymu jei send mail laukas yra YES
        :param storage_remaining: priima sandėlio likutį
        """
        order_amount = float(self.entryFieldOrder.get())
        selected_recipe = self.recipe_list.get()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        num = 0
        if min(storage_remaining) < 0:
            efficiency = control.get_process_efficiency()
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
            write_order_to_txt(
                f"{date_now} - Order of {selected_recipe} - {order_amount}kg could not "
                f"be completed, not enough materials. It will take {num} working hours to complete this order.\n"
            )
        else:
            write_order_to_txt(
                f"{date_now} - Order of {selected_recipe} - {order_amount}kg completed.\n"
            )
            control.update_storage_after_order(storage_remaining)
            control.add_order(selected_recipe, order_amount)
            self.send_order_mail(date_now, selected_recipe, order_amount)

    def send_order_mail(self, date, recipe, amount):
        subject = f"{date} - Order {recipe} - {amount}kg"
        text = f"{date} - Order of recipe {recipe} - {amount}kg has just been completed"
        mail_state = self.mail_list.get()
        if mail_state == "YES":
            send_email(subject, text)

    def filter_orders_buttons(self):
        """
        Sudeda laukus ir labels Orders filtravimui
        """
        self.buttonEdit.config(
            text="Send to Email",
            bg="#00A650",
            state=tkinter.NORMAL,
            command=self.email_filtered,
        )
        self.buttonFilterOrders.config(text="Cancel", command=self.cancel_filtering)
        self.labelEdit1.grid(row=1, column=7, sticky="W")
        self.labelEdit2.grid(row=2, column=7, sticky="W")
        self.labelEdit3.grid(row=3, column=7, sticky="W")
        self.labelEdit1.config(text="Year: ")
        self.labelEdit2.config(text="Month: ")
        self.labelEdit3.config(text="Day: ")
        self.year_list_from.grid(row=1, column=8, sticky="W")
        self.month_list_from.grid(row=2, column=8, sticky="W")
        self.day_list_from.grid(row=3, column=8, sticky="W")
        self.year_list_to.grid(row=1, column=9, sticky="W")
        self.month_list_to.grid(row=2, column=9, sticky="W")
        self.day_list_to.grid(row=3, column=9, sticky="W")
        self.labelFilterFrom.place(x=1044, y=320)
        self.labelFilterTo.place(x=1219, y=320)
        self.currency_list.bind("<<ComboboxSelected>>", self.filter_orders)
        self.year_list_from.bind("<<ComboboxSelected>>", self.filter_orders)
        self.month_list_from.bind("<<ComboboxSelected>>", self.filter_orders)
        self.day_list_from.bind("<<ComboboxSelected>>", self.filter_orders)
        self.year_list_to.bind("<<ComboboxSelected>>", self.filter_orders)
        self.month_list_to.bind("<<ComboboxSelected>>", self.filter_orders)
        self.day_list_to.bind("<<ComboboxSelected>>", self.filter_orders)

    def filter_orders(self, event):
        """
        Filtruoja Orders pagal datų ruožą
        :param event aktyvuojama datų filtrų combobox pasikeitimu
        """
        date_from = f"{self.year_list_from.get()}-{self.month_list_from.get()}-{self.day_list_from.get()} 00:00:01"
        date_to = f"{self.year_list_to.get()}-{self.month_list_to.get()}-{self.day_list_to.get()} 23:59:59"
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            date_to = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        filtered = control.search_order_by_date(date_from, date_to)
        for i in self.ordersTable.get_children():
            self.ordersTable.delete(i)
        chosen_currency = self.currency_list.get()
        rate = self.rates[chosen_currency]
        for i in filtered:
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

    def email_filtered(self):
        """
        Nusiunčia e-mail su nufiltruotais Orders laukais
        """
        date_from = f"{self.year_list_from.get()}-{self.month_list_from.get()}-{self.day_list_from.get()}"
        date_to = f"{self.year_list_to.get()}-{self.month_list_to.get()}-{self.day_list_to.get()}"
        subject = f"Orders from: {date_from} to {date_to}"
        text = ""
        for i in self.ordersTable.get_children():
            t_data = self.ordersTable.item(i)["values"]
            text += (
                f"ID: {t_data[0]} "
                f"Date: {t_data[1]} "
                f"Recipe: {t_data[2]} "
                f"Amount: {t_data[3]}kg "
                f"Manufacturing cost: {t_data[4]}{self.currency_list.get()} "
                f"Selling price: {t_data[5]}{self.currency_list.get()}\n"
            )
        if text != "":
            send_email(subject, text)
            ErrorWindow("Orders sent!")
        else:
            ErrorWindow("No orders to send!")

    def cancel_filtering(self):
        """
        Atšaukia Orders filtravimą ir atstato mygtukus
        """
        self.cancel_editing()
        self.buttonFilterOrders.grid(row=3, column=6)
        self.buttonFilterOrders.config(
            text="Filter", command=self.filter_orders_buttons
        )
        self.buttonEdit.config(state=tk.DISABLED, bg="gray", text="Edit")
