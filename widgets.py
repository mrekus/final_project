class Widgets:
    """
    Visi programos widgets kuriuos paveldi views klasės,
    kad matytų visą programą
    """
    def __init__(self):
        self.materialsTable = None
        self.storageTable = None
        self.recipeTable = None
        self.ordersTable = None
        self.processTable = None

        self.labelEdit1 = None
        self.labelEdit2 = None
        self.labelEdit3 = None
        self.labelEdit4 = None
        self.labelEdit5 = None
        self.labelEdit6 = None
        self.labelFilterFrom = None
        self.labelFilterTo = None
        self.labelOrderProfit1 = None
        self.labelOrderProfit2 = None
        self.labelOrder = None
        self.labelRecipe = None

        self.entryFieldEdit1 = None
        self.entryFieldEdit2 = None
        self.entryFieldEdit3 = None
        self.entryFieldEdit4 = None
        self.entryFieldEdit5 = None
        self.entryFieldEdit6 = None
        self.entryFieldOrder = None

        self.buttonAddRecipe = None
        self.buttonEdit = None
        self.buttonDelete = None
        self.buttonAddOrder = None
        self.buttonConfirmOrder = None
        self.buttonCancelOrder = None
        self.buttonFilterOrders = None
        self.buttonCancelEditing = None

        self.idForEdit = None
        self.scrollbar_recipe = None
        self.rates = None
        self.currency_list = None
        self.recipe_list = None
        self.mail_list = None
        self.year_list_from = None
        self.month_list_from = None
        self.day_list_from = None
        self.year_list_to = None
        self.month_list_to = None
        self.day_list_to = None
