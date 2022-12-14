from utils import *
from datetime import datetime
from Control import send_email


def write_order_to_txt(text):
    with open("orders.txt", "a", encoding="utf-8") as record_order:
        record_order.write(text)


class OrderViews(widgets.Widgets):
    """
    Visi metodai valdantys Orders laukus
    """

    def fill_orders_data_box(self):
        """
        Atstato pradinę lango būseną su Orders duomenų lentele
        """
        self.default_button_layouts()
        self.forget_tables()
        self.ordersTable.grid(row=1, rowspan=4, column=2, columnspan=3, sticky=tk.NSEW)
        for i in self.ordersTable.get_children():
            self.ordersTable.delete(i)
        self.ordersTable.column(f"# {1}", anchor=tk.CENTER, width=40)
        self.ordersTable.heading(f"# {1}", text="ID")
        for i, col_heading in enumerate(
            [
                "Date",
                "Recipe",
                "Amount, kg",
                "Manufacturing Cost",
                "Selling price",
            ],
            2,
        ):
            self.ordersTable.column(f"# {i}", anchor=tk.CENTER, width=136)
            self.ordersTable.heading(f"# {i}", text=col_heading)
        self.currency_list.bind("<<ComboboxSelected>>", self.refresh_orders_event)
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
        self.buttonEdit.config(state=tk.DISABLED, bg="white", activebackground="gray")
        self.buttonFilterOrders.grid(row=3, column=6)
        self.buttonFilterOrders.config(
            text="Filter",
            command=self.filter_orders_buttons,
            activebackground="#75C1BF",
        )
        scrollbar_orders = tk.Scrollbar(
            self.ordersTable, orient=tk.VERTICAL, command=self.ordersTable.yview
        )
        scrollbar_orders.place(x=705, y=27, height=175)
        self.ordersTable.configure(yscrollcommand=scrollbar_orders.set)

    def refresh_orders(self):
        """
        Atnaujina Orders lentelės įrašus
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

    def refresh_orders_event(self, _event):
        """
        Atnaujina Orders lentelės įrašus
        :param _event: aktyvuojamas currency combobox pasikeitimu
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
        self.recipe_list.config(values=control.check_for_duplicates("Recipe"))
        self.recipe_list.set("")

    def order_adding_widgets(self):
        """
        Sukuria užsakymo pridėjimo laukus ir atnaujina receptų sąrašą
        """
        self.refresh_recipe_list()
        self.buttonCancelOrder.config(activebackground="red")
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
        days_to_complete = control.days_to_complete_order(storage_remaining)
        if days_to_complete != 0:
            logging.critical("Not enough material in storage to complete an order")
            ErrorWindow(
                f"Not enough materials to complete the order,\n"
                f"it would take {days_to_complete} working hours to get enough material"
            )
            write_order_to_txt(
                f"{date_now} - Order of {selected_recipe} - {order_amount}kg could not "
                f"be completed, not enough materials. "
                f"It would take {days_to_complete} working hours to complete this order.\n"
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
        self.filtered_orders_profit()
        self.buttonEdit.config(
            text="Send to Email",
            bg="white",
            activebackground="#00A650",
            state=tk.NORMAL,
            command=self.email_filtered,
        )
        self.buttonFilterOrders.config(
            text="Cancel", activebackground="red", command=self.cancel_filtering
        )
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
        self.currency_list.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.year_list_from.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.month_list_from.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.day_list_from.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.year_list_to.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.month_list_to.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.day_list_to.bind("<<ComboboxSelected>>", self.filter_orders, add="+")
        self.currency_list.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.year_list_from.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.month_list_from.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.day_list_from.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.year_list_to.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.month_list_to.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )
        self.day_list_to.bind(
            "<<ComboboxSelected>>", self.filtered_orders_profit_change, add="+"
        )

    def filter_orders(self, _event):
        """
        Filtruoja Orders pagal datų ruožą
        :param _event aktyvuojama datų filtrų combobox pasikeitimu
        """
        date_from = (
            f"{self.year_list_from.get()}"
            f"-{self.month_list_from.get()}"
            f"-{self.day_list_from.get()} 00:00:01"
        )
        date_to = (
            f"{self.year_list_to.get()}"
            f"-{self.month_list_to.get()}"
            f"-{self.day_list_to.get()} 23:59:59"
        )
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
        date_from = (
            f"{self.year_list_from.get()}"
            f"-{self.month_list_from.get()}"
            f"-{self.day_list_from.get()}"
        )
        date_to = (
            f"{self.year_list_to.get()}"
            f"-{self.month_list_to.get()}"
            f"-{self.day_list_to.get()}"
        )
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
        total_profit = f"Total period profit: {self.labelOrderProfit2.cget('text')}"
        text += total_profit
        if text != total_profit:
            send_email(subject, text)
        else:
            ErrorWindow("No orders to send!")

    def cancel_filtering(self):
        """
        Atšaukia Orders filtravimą ir atstato mygtukus
        """
        self.cancel_editing()
        self.refresh_orders()
        self.buttonFilterOrders.grid(row=3, column=6)
        self.buttonFilterOrders.config(
            text="Filter",
            command=self.filter_orders_buttons,
            activebackground="#75C1BF",
        )
        self.buttonEdit.config(
            state=tk.DISABLED, bg="white", text="Edit", activebackground="gray"
        )

    def filtered_orders_profit(self):
        """
        Apskaičiuoja Orders lentelės įrašų pelną
        atimant iš selling price manufacturing price,
        prideda tekstą šalia datų filtrų
        """
        profit_total = 0
        for i in self.ordersTable.get_children():
            t_man_cost = float(self.ordersTable.item(i)["values"][4])
            t_sell_price = float(self.ordersTable.item(i)["values"][5])
            profit = t_sell_price - t_man_cost
            profit_total += profit
        self.labelOrderProfit2.config(
            text=f"{round(profit_total, 2)}{self.currency_list.get()}"
        )
        self.labelOrderProfit1.grid(row=1, column=10, sticky="W")
        self.labelOrderProfit2.grid(row=2, column=10)

    def filtered_orders_profit_change(self, _event):
        """
        Apskaičiuoja Orders lentelės įrašų pelną
        atimant iš selling price manufacturing price.
        :param _event: Aktyvuojamas valiutų arba datų filtrų
        combobox pasikeitimu.
        """
        profit_total = 0
        for i in self.ordersTable.get_children():
            t_man_cost = float(self.ordersTable.item(i)["values"][4])
            t_sell_price = float(self.ordersTable.item(i)["values"][5])
            profit = t_sell_price - t_man_cost
            profit_total += profit
        self.labelOrderProfit2.config(
            text=f"{round(profit_total, 2)}{self.currency_list.get()}"
        )
