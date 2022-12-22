from data import For_db
from data.UserUser import Users
from data.product import Product
"Импорты"
from tabulate import tabulate

For_db.global_init("data/ETO_BAZA.db")
db_sess = For_db.create_session()


class User:
    """Create a user"""
    def __init__(self, id, name, password, role):
        """
        Создание экземплера класса
        :param id: айди
        :param name: имя
        :param password: пароль
        :param role: роль
        """
        self.id_use = int(id)
        self.name = name
        self.password = password
        self.role = int(role)

    def products(self):
        """
        Продуктики
        :return: None
        """
        prods = db_sess.query(Product)
        headers = []
        haracteristics = []

        for i in prods:
            head = []
            har = []
            for j in i.to_dict().keys():
                head.append(j)
                har.append(i.to_dict()[j])

            headers = head
            haracteristics.append(har)

        print(tabulate(haracteristics, headers=headers))

    def change_password(self):
        """
        Позволяет менять пороль
        :return: None
        """
        new_pass = input("Input a new password: ")
        db_sess.query(Users).filter(Users.id == self.id_use).update(
            {Users.password: new_pass}, synchronize_session=False
        )
        db_sess.commit()
        print("Done")


class Admin(User):
    "Admin role"
    def add_product(self):
        """
        Позволяет добавить новый продукт и забить его в бд
        :return: None
        """
        try:
            new_prod = Product()
            new_prod.name = input("New product: ")
            new_prod.description = input("Description: ")
            new_prod.postav = input("Company: ")
            new_prod.price = int(input("Price: "))
            new_prod.count = int(input("finished goods: "))

            db_sess.add(new_prod)
            db_sess.commit()
            db_sess.rollback()

        except (Exception):
            print("Error")

    def delete(self, id):
        try:

            db_sess.query(Product).filter(Product.id == id).delete(synchronize_session=False)
            db_sess.commit()
            print("Done")

        except (Exception):
            print("Error")

    def change_somthing_product(self, id):
        """
        Позволяет менять продукт
        :param id: Айдишник продукта
        :return: None
        """
        try:
            prod = db_sess.query(Product).filter(Product.id == id).one()
            atribute = input("choose atribute: ")

            if atribute == "description":
                new = input("New description: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.description: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Done")

            elif atribute == "company":
                new = input("New company: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.postav: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Done")

            elif atribute == "count":
                new = int(input("New count: "))
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.count: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Done")

            elif atribute == "price":
                new = int(input("New price: "))
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.price: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Done")

            elif atribute == "name":
                new = input("New name: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.name: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Done")

            else:
                print("Error")
        except (Exception):
            print("Error")


def autorize():
    """
    Процесс авторизации
    :return: None
    """
    name = input("Name: ")
    password = input("Password: ")
    again_password = input("Again password: ")

    if password == again_password:
        try:
            user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()
            if user:
                print('hh')
                return (user, 1)
            else:
                return (0, 0)

        except (Exception):
            return (0, 0)

    else:
        return (0, 0)


def reg():
    """
    Регистрация нового пользователя с передачей в бд
    :return: None
    """
    name = input("Name: ")
    password = input("Password: ")

    try:
        user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()
        if str(user.name) == name:
            print("Error")
            return autorize()

    except (Exception):
        new_user = Users()
        new_user.name = name
        new_user.password = password
        new_user.role = 0

        db_sess.add(new_user)
        db_sess.commit()
        db_sess.rollback()

        return (new_user, 1)


def interface_admin(adm):
    """
    Реализация интерфейса для админа
    :param adm:
    :return: None
    """
    while (True):
        adm.products()
        print()
        print("Choise: 1 - reduct, 2 - delete, 3 - add: ")
        inp = int(input("Input: "))
        try:
            if inp == 1:
                id_of_prod = int(input("ID product: "))
                adm.change_somthing_product(id_of_prod)

            elif inp == 2:
                id_of_prod = int(input(" ID product: "))
                adm.delete(id_of_prod)

            elif inp == 3:
                adm.Add_User()

            else:
                print("Error")

        except (Exception):
            print("Error")


def interface_for_user(use):
    """
    Интерфейс для смертных
    :param use: Данные юзера
    :return:
    """
    while (True):
        use.products()
        print()
        print("Choose: 1 - change pass: ")
        inp = int(input("inp: "))
        try:
            if inp == 1:
                use.change_password()
                print("all good")

            else:
                print("Error")

        except (Exception) as e:
            print(e)


def main():
    """
    Основной модуль запускающий весь процесс
    :return:
    """
    print("Choose: 1 - auhth, 2 - sing in")
    inp = int(input())
    if inp == 1:
        res_aut = autorize()
        if res_aut[1] == 1:
            if res_aut[0].role == 0:
                user = User(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
                interface_for_user(user)
            elif res_aut[0].role == 1:
                admin = Admin(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
                interface_admin(admin)

        else:
            print("Error")

    elif inp == 2:
        res_reg = reg()
        if res_reg[1] == 1:
            if res_reg[0].role == 0:
                user = User(res_reg[0].id, res_reg[0].name, res_reg[0].password, res_reg[0].role)
                interface_for_user(user)
            elif res_reg[0].role == 0:
                admin = Admin(res_reg[0].id, res_reg[0].name, res_reg[0].password, res_reg[0].role)
                interface_admin(admin)

        else:
            print("Error")


if __name__ == "__main__":
    main()