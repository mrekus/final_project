from Models import Process, Recipe, Storage, Orders, Materials, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()


def get_table_data(table):
    """
    Grąžina visus pasirinktos lentelės įrašus
    :param table: lentelės pavadinimas
    """
    tables = {
        "Orders": Orders,
        "Materials": Materials,
        "Storage": Storage,
        "Recipe": Recipe,
        "Process": Process,
    }
    table_data = session.query(tables[table]).all()
    return table_data


def get_storage_amount():
    """
    :return: grąžina visus storage DB amount
    """
    return session.query(Storage.amount).all()


def get_process_efficiency():
    """
    :return: Grąžina procesų efficiency
    """
    return session.query(Process.efficiency).all()


def delete_recipe_record(deletion_id):
    """
    Ištrina recepto įrašą iš DB pagal ID
    :param deletion_id: trinamo įrašo ID
    """
    deletion_object = session.query(Recipe).get(deletion_id)
    session.delete(deletion_object)
    session.commit()


def add_recipe(name, material1, material2, material3, material4, material5):
    """
    Prideda naują recepto įrašą į DB
    :param name: Recepto avadinimas
    :param material1: Material 1 vieneto dalimis
    :param material2: Material 2 vieneto dalimis
    :param material3: Material 3 vieneto dalimis
    :param material4: Material 4 vieneto dalimis
    :param material5: Material 5 vieneto dalimis
    """
    recipe = Recipe(name, material1, material2, material3, material4, material5)
    session.add(recipe)
    session.commit()


def update_process(update_id, name, efficiency):
    """
    Atnaujiną proceso įrašą pagal ID
    :param update_id: norimo įrašo ID
    :param name: įrašo pavadinimas
    :param efficiency: našumas
    """
    update_object = session.query(Process).get(update_id)
    update_object.name = name
    update_object.efficiency = efficiency
    session.commit()


def update_recipe(
    update_id, name, material1, material2, material3, material4, material5
):
    """
    Atnaujina recepto įrašą pagal ID
    :param update_id: norimo įrašo ID
    :param name: įrašo pavadinimas
    :param material1: material 1 vieneto dalimis
    :param material2: material 2 vieneto dalimis
    :param material3: material 3 vieneto dalimis
    :param material4: material 4 vieneto dalimis
    :param material5: material 5 vieneto dalimis
    """
    update_object = session.query(Recipe).get(update_id)
    update_object.name = name
    update_object.material1 = material1
    update_object.material2 = material2
    update_object.material3 = material3
    update_object.material4 = material4
    update_object.material5 = material5


def update_storage(update_id, amount):
    """
    Atnaujina storage įrašą pagal ID
    :param update_id: įrašo ID
    :param amount: įrašo kiekis
    :return:
    """
    update_object = session.query(Storage).get(update_id)
    update_object.amount = amount
    session.commit()


def update_material(update_id, name, price=False):
    """
    Atnaujiną proceso įrašą pagal ID
    :param update_id: norimo įrašo ID
    :param name: įrašo pavadinimas
    :param price: kaina
    """
    update_object = session.query(Materials).get(update_id)
    update_object.name = name
    if price:
        update_object.price = price
    session.commit()


def check_for_duplicates_process():
    """
    Sukuria process pavadinimų sąrašą
    :return: atiduoda process pavadinimų sąrašą
    """
    process_list = []
    for i in session.query(Process).all():
        process_list.append(i.name)
    return process_list


def check_for_duplicates_recipe():
    """
    Sukuria receptų pavadinimų sąrašą
    :return: atiduoda receptų pavadinimų sąrašą
    """
    recipe_list = []
    for i in session.query(Recipe).all():
        recipe_list.append(i.name)
    return recipe_list


def check_for_duplicates_materials():
    """
    Sukuria materials pavadinimų sąrašą
    :return: atiduoda storage pavadinimų sąrašą
    """
    materials_list = []
    for i in session.query(Materials).all():
        materials_list.append(i.name)
    return materials_list


def get_material_price_list():
    """
    Grąžina material kainų sąrašą
    """
    price_list = []
    for i in session.query(Materials).all():
        price_list.append(i.price)
    return price_list


def search_order_by_date(start, end):
    """
    Grąžina Orders įrašus pagal užduotą datų ruožą
    :param start: nuo kada filtras
    :param end: iki kada filtras
    """
    qry = session.query(Orders).filter(Orders.date.between(start, end))
    return qry


def get_recipe_materials_list(recipe_name):
    """
    Grąžina recepto materials sąrašą
    :param recipe_name: recepto pavadinimas kurio materials ieškosim
    """
    recipe = session.query(Recipe).filter_by(name=recipe_name).one()
    material1 = recipe.material1
    material2 = recipe.material2
    material3 = recipe.material3
    material4 = recipe.material4
    material5 = recipe.material5
    material_list = [material1, material2, material3, material4, material5]
    return material_list


def update_storage_after_order(remaining):
    record_id = 1
    for i in remaining:
        record = session.query(Storage).get(record_id)
        record.amount = round(i, 1)
        record_id += 1
    session.commit()


def add_order(recipe_name, order_amount):
    """
    Prideda įvykdytą užsakymą į DB
    :param recipe_name recepto pavadinimas
    :param order_amount užsakymo kiekis
    """
    recipe = session.query(Recipe).filter_by(name=recipe_name).one()
    order_date = datetime.now().replace(second=0, microsecond=0)
    recipe_id = recipe.id
    recipe_amount = float(order_amount)
    prices = get_material_price_list()
    man_cost = round(sum([i * recipe_amount for i in prices]), 2)
    sell_price = round((man_cost * 1.3), 2)
    order = Orders(order_date, recipe_id, recipe_amount, man_cost, sell_price)
    session.add(order)
    session.commit()


def get_record_by_id(table, record_id):
    """
    Grąžina įrašą iš pasirinktos lentelės su pasirinktu id
    :param table: lentelės pavadinimas
    :param record_id: įrašo id
    """
    tables = {
        "Orders": Orders,
        "Materials": Materials,
        "Storage": Storage,
        "Recipe": Recipe,
        "Process": Process,
    }
    record = session.query(tables[table]).get(record_id)
    return record
