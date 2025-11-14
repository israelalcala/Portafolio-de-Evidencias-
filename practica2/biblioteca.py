import json
from abc import ABC, abstractmethod


GENRES = ["Ficción", "No Ficción", "Ciencia", "Historia", "Fantasía", "Biografía", "Otro"]


class Item(ABC):
    def __init__(self, item_id, title, year, quantity):
        self._id = item_id
        self._title = title
        self._year = year
        self._quantity = quantity

    @abstractmethod
    def display_info(self):
        pass

    def is_available(self):
        return self._quantity > 0

    def lend(self):
        if self._quantity > 0:
            self._quantity -= 1
            return True
        return False

    def return_item(self):
        self._quantity += 1

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "year": self._year,
            "quantity": self._quantity,
            "type": self.__class__.__name__
        }


class Book(Item):
    def __init__(self, item_id, title, author, year, genre, quantity):
        super().__init__(item_id, title, year, quantity)
        self._author = author
        self._genre = genre

    def display_info(self):
        print(f"[Libro] ID: {self._id}, Título: {self._title}, Autor: {self._author}, Año: {self._year}, Género: {self._genre}, Cantidad: {self._quantity}")

    def to_dict(self):
        data = super().to_dict()
        data.update({"author": self._author, "genre": self._genre})
        return data


class Magazine(Item):
    def __init__(self, item_id, title, year, issue, quantity):
        super().__init__(item_id, title, year, quantity)
        self._issue = issue

    def display_info(self):
        print(f"[Revista] ID: {self._id}, Título: {self._title}, Año: {self._year}, Edición: {self._issue}, Cantidad: {self._quantity}")

    def to_dict(self):
        data = super().to_dict()
        data.update({"issue": self._issue})
        return data


class User:
    def __init__(self, user_id, name):
        self._id = user_id
        self._name = name
        self._borrowed_items = []

    def borrow_item(self, item_id):
        self._borrowed_items.append(item_id)

    def return_item(self, item_id):
        if item_id in self._borrowed_items:
            self._borrowed_items.remove(item_id)
            return True
        return False

    def display_info(self):
        print(f"Usuario ID: {self._id}, Nombre: {self._name}, Préstamos: {self._borrowed_items}")

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "borrowed_items": self._borrowed_items
        }


class Library:
    def __init__(self):
        self.items = []
        self.users = []

    def add_item(self, item):
        self.items.append(item)

    def add_user(self, user):
        self.users.append(user)

    def find_item(self, item_id):
        return next((i for i in self.items if i._id == item_id), None)

    def find_user(self, user_id):
        return next((u for u in self.users if u._id == user_id), None)

    def lend_item(self, user_id, item_id):
        user = self.find_user(user_id)
        item = self.find_item(item_id)
        if user and item and item.lend():
            user.borrow_item(item_id)
            print("Préstamo exitoso.")
        else:
            print("No se pudo realizar el préstamo.")

    def return_item(self, user_id, item_id):
        user = self.find_user(user_id)
        item = self.find_item(item_id)
        if user and item and user.return_item(item_id):
            item.return_item()
            print("Devolución exitosa.")
        else:
            print("No se pudo realizar la devolución.")

    def search_items(self, keyword):
        results = [i for i in self.items if keyword.lower() in i._title.lower()]
        for item in results:
            item.display_info()

    def search_users(self, keyword):
        results = [u for u in self.users if keyword.lower() in u._name.lower()]
        for user in results:
            user.display_info()

    def save_to_file(self):
        with open("items.json", "w") as f:
            json.dump([i.to_dict() for i in self.items], f, indent=2)
        with open("users.json", "w") as f:
            json.dump([u.to_dict() for u in self.users], f, indent=2)

    def load_from_file(self):
        try:
            with open("items.json") as f:
                data = json.load(f)
                for d in data:
                    if d["type"] == "Book":
                        self.items.append(Book(d["id"], d["title"], d["author"], d["year"], d["genre"], d["quantity"]))
                    elif d["type"] == "Magazine":
                        self.items.append(Magazine(d["id"], d["title"], d["year"], d["issue"], d["quantity"]))
            with open("users.json") as f:
                data = json.load(f)
                for d in data:
                    user = User(d["id"], d["name"])
                    user._borrowed_items = d["borrowed_items"]
                    self.users.append(user)
        except FileNotFoundError:
            print("Archivos no encontrados, iniciando con datos vacíos.")


def menu():
    lib = Library()
    lib.load_from_file()

    while True:
        print("\n--- Menú Biblioteca ---")
        print("1. Registrar libro")
        print("2. Registrar revista")
        print("3. Registrar usuario")
        print("4. Mostrar ítems")
        print("5. Mostrar usuarios")
        print("6. Prestar ítem")
        print("7. Devolver ítem")
        print("8. Buscar ítem")
        print("9. Buscar usuario")
        print("10. Guardar y salir")
        choice = input("Opción: ")

        if choice == "1":
            i = int(input("ID: "))
            t = input("Título: ")
            a = input("Autor: ")
            y = int(input("Año: "))
            g = input("Género: ")
            q = int(input("Cantidad: "))
            lib.add_item(Book(i, t, a, y, g, q))

        elif choice == "2":
            i = int(input("ID: "))
            t = input("Título: ")
            y = int(input("Año: "))
            ed = input("Edición: ")
            q = int(input("Cantidad: "))
            lib.add_item(Magazine(i, t, y, ed, q))

        elif choice == "3":
            i = int(input("ID: "))
            n = input("Nombre: ")
            lib.add_user(User(i, n))

        elif choice == "4":
            for item in lib.items:
                item.display_info()

        elif choice == "5":
            for user in lib.users:
                user.display_info()

        elif choice == "6":
            uid = int(input("ID usuario: "))
            iid = int(input("ID ítem: "))
            lib.lend_item(uid, iid)

        elif choice == "7":
            uid = int(input("ID usuario: "))
            iid = int(input("ID ítem: "))
            lib.return_item(uid, iid)

        elif choice == "8":
            kw = input("Buscar título: ")
            lib.search_items(kw)

        elif choice == "9":
            kw = input("Buscar nombre: ")
            lib.search_users(kw)

        elif choice == "10":
            lib.save_to_file()
            print("Datos guardados. ¡Hasta luego!")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
