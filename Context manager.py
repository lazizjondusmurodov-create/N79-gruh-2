import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
""")

conn.commit()


class Product:

    def __init__(self, name=None, price=None):
        self.name = name
        self.price = price

        self.conn = sqlite3.connect("shop.db")
        self.cursor = self.conn.cursor()

    def save(self):

        self.cursor.execute(
            "INSERT INTO products(name, price) VALUES(?, ?)",
            (self.name, self.price)
        )

        self.conn.commit()

        print("Mahsulot saqlandi")

    def get_all_users(self):

        self.cursor.execute("SELECT * FROM products")

        return self.cursor.fetchall()

    def get_object(self, product_id):

        self.cursor.execute(
            "SELECT * FROM products WHERE id=?",
            (product_id,)
        )

        return self.cursor.fetchone()

    def delete(self, product_id):

        self.cursor.execute(
            "DELETE FROM products WHERE id=?",
            (product_id,)
        )

        self.conn.commit()

        print("O'chirildi")

    def update(self, product_id, new_name, new_price):

        self.cursor.execute(
            "UPDATE products SET name=?, price=? WHERE id=?",
            (new_name, new_price, product_id)
        )

        self.conn.commit()

        print("Yangilandi")


# TEST

p1 = Product("Telefon", 300)
p1.save()

p = Product()

print(p.get_all_users())

print(p.get_object(1))

p.update(1, "iPhone", 1200)

p.delete(1)