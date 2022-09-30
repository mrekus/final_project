from Models import Process, Recipe, Storage, Orders, Materials, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def get_process_data():
    """
    :return: Grąžina visus process DB įrašus
    """
    return session.query(Process).all()


def get_recipe_data():
    """
    :return: Grąžina visus recipies DB įrašus
    """
    return session.query(Recipe).all()


def get_storage_data():
    """
    :return: grąžina visus storage DB įrašus
    """
    return session.query(Storage).all()


def get_orders_data():
    """
    :return: grąžina visus orders DB įrašus
    """
    return session.query(Orders).all()


def get_materials_data():
    """
    :return: grąžina visus materials DB įrašus
    """
    return session.query(Materials).all()


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


def add_order(date, recipe, amount, man_cost, sell_price):
    """
    Prideda užsakymą į DB
    :param date: užsakymo data
    :param recipe: gamintas receptas
    :param amount: gamintas kiekis
    :param man_cost: gamybos kaina
    :param sell_price: pardavimo kaina
    """
    order = Orders(date, recipe, amount, man_cost, sell_price)
    session.add(order)
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


def check_for_duplicates_storage():
    """
    Sukuria storage pavadinimų sąrašą
    :return: atiduoda storage pavadinimų sąrašą
    """
    storage_list = []
    for i in session.query(Storage).all():
        storage_list.append(i.materials.name)
    return storage_list


def update_material(update_id, name):
    """
    Atnaujina storage DB material pavadinimą pagal process material pavadinimą
    :param update_id: atnaujinamo įrašo ID
    :param name: naujas pavadinimas
    """
    update_object = session.query(Materials).get(update_id)
    update_object.name = name
    session.commit()


def get_material_price_list():
    """
    Grąžina material kainų sąrašą
    """
    price_list = []
    prices = session.query(Materials.price).all()
    for i in prices:
        price_list.append(i[0])
    return price_list


def search_order_by_date(start, end):
    """
    Grąžina Orders įrašus pagal užduotą datų ruožą
    :param start: nuo kada filtras
    :param end: iki kada filtras
    """
    qry = session.query(Orders).filter(Orders.date.between(start, end))
    return qry