from flask import *
from pwd_hashing import hashing
from make_variant_time import variant_time, time_of_order
import json


class PizzaApp:
    """
    Класс для реализации веб-приложения пиццерии.

    Этот класс содержит методы для обработки запросов и логики веб-приложения пиццерии,
    включая аутентификацию пользователей, формирование заказов, отображение истории заказов и т.д.

    Attributes
    ----------
    name_of_user : str
        Имя текущего пользователя.
    login_of_user : str
        Логин текущего пользователя.
    current_order_pizza : dict
        Текущий заказ пиццы в формате {"название пиццы": {"количество": количество}}.
    delivery_time : str
        Время доставки текущего заказа в формате "чч:мм".
    order_time : str
        Время оформления текущего заказа в формате "чч:мм".
    current_order_history : dict
        История заказов текущего пользователя в формате {"дата": {"время заказа": "время доставки"}}.
    app : Flask
        Экземпляр Flask приложения.

    Methods
    -------
    login()
        Обработка запроса на страницу входа в приложение.
    registration()
        Обработка запроса на страницу регистрации в приложение.
    making_order()
        Обработка запроса на добавление пиццы в текущий заказ.
    show_cart(order_status=None, message=None)
        Обработка запроса на страницу отображения текущего заказа.
    make_order()
        Обработка запроса на оформление текущего заказа.
    make_order_history(self)
        Метод для формирования истории заказов текущего пользователя.
    show_order_history()
        Обработка запроса на страницу отображения истории заказов текущего пользователя.
    run()
        Запуск Flask приложения.

    """

    def __init__(self):
        self.name_of_user = ''
        self.login_of_user = ''
        self.current_order_pizza = {}
        self.delivery_time = ''
        self.order_time = ''
        self.current_order_history = {}
        self.app = Flask(__name__)

        @self.app.route("/", methods=["POST", "GET"])
        def login():
            """
            Обработка запроса на страницу входа в приложение.

            Этот метод обрабатывает запросы на страницу входа в приложение и проверяет
            введенные пользователем логин и пароль. В случае успешной авторизации,
            пользователь перенаправляется на главное меню приложения.

            Parameters
            ----------
            None

            Returns
            -------
            str
                HTML-код страницы входа в приложение или главного меню приложения.

            Notes
            -----
            - Для проверки пароля используется функция hashing, отвечающая за хеширование пароля.
            - В случае неуспешной авторизации, пользователю выводится сообщение об ошибке.
            """
            if request.method == "POST":
                login = request.form.get("login")
                password = request.form.get("password")
                with open("data/user_data.json") as user_data:
                    user_info = json.load(user_data)
                    if login not in user_info.keys():
                        return render_template("login.html",
                                               error="Пользователя с таким логином не существует. Пройдите регистрацию.")
                    elif user_info[login]["password"] != hashing(password):
                        return render_template("login.html", error="Неправильный пароль.")
                    else:
                        self.name_of_user = user_info[login]["name"]
                        self.login_of_user = login
                        return render_template("main_menu.html")

            return render_template("login.html")

        @self.app.route("/registration", methods=["POST", "GET"])
        def registration():
            """
            Обработка запроса на страницу регистрации в приложение.

            Этот метод обрабатывает запросы на страницу регистрации в приложение и
            регистрирует нового пользователя с введенными именем, логином и паролем.
            В случае успешной регистрации, пользователь перенаправляется на главное меню приложения.

            Parameters
            ----------
            None

            Returns
            -------
            str
                HTML-код страницы регистрации в приложение или главного меню приложения.

            Notes
            -----
            - Для сохранения пароля используется хеш-функция.
            - В случае, если пользователь с таким логином уже существует,
              пользователю выводится сообщение об ошибке.
            """
            if request.method == "POST":
                name = request.form.get("name")
                login = request.form.get("login")
                password = request.form.get("password")
                with open("data/user_data.json") as user_data:
                    user_info = json.load(user_data)
                if login not in user_info.keys():
                    user_info[login] = {"name": name, "password": hashing(password)}
                    with open("data/user_data.json", "w") as user_data:
                        json.dump(user_info, user_data)
                    self.name_of_user = name
                    self.login_of_user = login
                    return render_template("main_menu.html")
                else:
                    return render_template("registration.html", error="Пользователь с таким логином уже существует :(")
            else:
                return render_template("registration.html")
            
        @self.app.route("/add_to_cart", methods=["POST", "GET"])
        def making_order():
            """
            Обработка запроса на добавление пиццы в текущий заказ.

            Этот метод обрабатывает запросы на добавление пиццы в текущий заказ и
            обновляет текущий заказ в соответствии с введенными данными.

            Parameters
            ----------
            None

            Returns
            -------
            str
                HTML-код главного меню приложения.

            Notes
            -----
            - Если пицца уже добавлена в текущий заказ, то ее количество обновляется.
            - Если пицца уже добавлена в текущий заказ и ее количество не изменилось,
              то пользователь остается на главном меню приложения.
            """
            if request.method == "POST":
                pizza = request.form["pizza"]
                count = request.form["count"]
                if pizza not in self.current_order_pizza.keys():
                    self.current_order_pizza[pizza] = {"quantity": count}
                elif pizza in self.current_order_pizza.keys() and self.current_order_pizza[pizza]["quantity"] == count:
                    return render_template("main_menu.html")
                else:
                    self.current_order_pizza[pizza] = {"quantity": count}
            return render_template("main_menu.html")

        @self.app.route("/cart", methods=["POST", "GET"])
        def show_cart(order_status=None, message=None):
            """
            Обработка запроса на просмотр текущего заказа.

            Этот метод обрабатывает запросы на просмотр текущего заказа и
            отображает информацию о заказанных пиццах, их количестве, цене и общий счет.
            Также пользователь может удалить пиццу из текущего заказа.

            Parameters
            ----------
            order_status : str, optional
                Статус заказа. По умолчанию равен None.
            message : str, optional
                Сообщение, которое будет отображено пользователю. По умолчанию равен None.

            Returns
            -------
            str
                HTML-код страницы с информацией о текущем заказе.

            Notes
            -----
            - Если заказ уже оформлен, то отображается пустая корзина.
            - Если пользователь удаляет пиццу из текущего заказа, то информация о ней
              удаляется из словаря `current_order_pizza`.
            """
            full_price = 0
            if request.method == "POST":
                if order_status == "Oформлен":
                    return render_template("cart.html", username=self.name_of_user, final_order=[], full_price=0,
                                           order_times=variant_time(), message=message)
                elif not order_status:
                    bad_pizza = request.form["remove"]
                    if bad_pizza in self.current_order_pizza.keys():
                        del self.current_order_pizza[bad_pizza]
            final_order = []
            with open("data/pizza_price.json", "r") as pizza_price:
                price_list = json.load(pizza_price)
            for pizza_name in self.current_order_pizza.keys():
                info_one_pizza = {}
                info_one_pizza["name"] = pizza_name
                info_one_pizza["quantity"] = self.current_order_pizza[pizza_name]["quantity"]
                info_one_pizza["price"] = price_list[pizza_name] * int(info_one_pizza["quantity"])
                full_price += info_one_pizza["price"]
                final_order.append(info_one_pizza)
            return render_template("cart.html", username=self.name_of_user, final_order=final_order,
                                   full_price=full_price,
                                   order_times=variant_time())
            
            
            
    def run(self):
        """
        Запуск приложения.

        Этот метод запускает приложение Flask.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        - Для запуска приложения необходимо вызвать этот метод после создания
            экземпляра класса `PizzaApp`.
        """
        self.app.run()


if __name__ == "__main__":
    my_site = PizzaApp()
    my_site.run()
