class EvenIterator:
    def __init__(self, start=1, end=1_000_000):
        # Eng yaqin juft songa yaxlitlash
        self.current = start if start % 2 == 0 else start + 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 2
        return value


# Ishlatish namunasi
it = EvenIterator(1, 1_000_000)

# Birinchi 5 ta qiymat
for _ in range(5):
    print(next(it))

print("...")

# for loop bilan ham ishlaydi
it2 = EvenIterator(1, 10)
for num in it2:
    print(num, end=" ")



#2. Generator 

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield 


for val in fibonacci(8):
    print(val)   


gen = fibonacci(5)
print(next(gen))  
print(next(gen))  
print(next(gen))  

        
print(list(fibonacci(10)))


#3. Decorator

from email.mime.multipart import MIMEMultipart
import time, functools

def timer(func):

  def wrapper(*args, **kwargs):
    start = time.perf_counter()     
    result = func(*args, **kwargs)
    end = time.perf_counter()      
    ms = (end - start) * 1000
    print(f"[timer] {func.__name__}: {ms:.2f} ms")
    return result
  return wrapper

@timer
def slow_sum(n): return sum(range(n))


#4. Context Manager


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class CustomFileWriter:
    def __init__(self, filename: str, mode: str = "w"):
        self.filename = filename
        self.mode     = mode
        self.file     = None

    def __enter__(self):
        logging.info(f"Fayl ochildi: '{self.filename}' (mode='{self.mode}')")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file                  

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

        if exc_type is not None:
            logging.error(f"Xato yuz berdi → {exc_type.__name__}: {exc_val}")
            return True                   
                                          

        logging.info(f"Fayl muvaffaqiyatli yopildi: '{self.filename}'")
        return False




# 1) Oddiy yozish
with CustomFileWriter("output.txt") as f:
    f.write("Salom, Dunyo!\n")
    f.write("Context manager ishlayapti.")

# 2) Qo'shib yozish (append)
with CustomFileWriter("output.txt", mode="a") as f:
    f.write("\nYangi qator qo'shildi.")

# 3) Xato holati — __exit__ ushlab qoladi
with CustomFileWriter("log.txt") as f:
    f.write("Boshlanmoqda...\n")
    raise ValueError("Noto'g'ri qiymat!")  
    f.write("Bu qator chiqmaydi.")          

# 4) Ko'p satr
lines = ["Python", "Context Manager", "CustomFileWriter"]
with CustomFileWriter("lines.txt") as f:
    f.writelines(line + "\n" for line in lines)


#5. PostgreSQL (psycopg2)
import psycopg2


class UserDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="mydb",
            user="postgres",
            password="Lazizbek2006",
            host="localhost",
            port=5432
        )
        self.cursor = self.conn.cursor()

    def get_users(self):
        query = "SELECT id, name, email FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


# ishga tushirish qismi
if __name__ == "__main__":
    db = UserDB()

    try:
        users = db.get_users()

        print("Users ro'yxati:\n")

        for user in users:
            print(f"ID: {user[0]}")
            print(f"Name: {user[1]}")
            print(f"Email: {user[2]}")
            print("-" * 20)

    except Exception as e:
        print("Xatolik:", e)

    finally:
        db.close()

#6. Requests


import requests

url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # HTTP xatoliklarni tekshirish

    posts = response.json()[:5]  # Birinchi 5 ta post

    for post in posts:
        print(f"Title: {post['title']}")
        print(f"Body:  {post['body']}")
        print("-" * 50)

except requests.exceptions.ConnectionError:
    print("Internetga ulanishda xatolik yuz berdi.")

except requests.exceptions.Timeout:
    print("So'rov vaqti tugadi.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP xatolik: {e}")

except requests.exceptions.RequestException as e:
    print(f"Xatolik yuz berdi: {e}")


#7. Multi Threading

import threading
import time
from concurrent.futures import ThreadPoolExecutor

# ── 1. threading.Thread ──────────────────────────────────
def vazifa(nom, son):
    for i in range(1, son + 1):
        print(f"[{nom}] → {i}")
        time.sleep(0.1)

threads = []
for nom, son in [("A-vazifa", 3), ("B-vazifa", 3), ("C-vazifa", 3)]:
    t = threading.Thread(target=vazifa, args=(nom, son))
    threads.append(t)
    t.start()

for t in threads:
    t.join()  

print("\n── ThreadPoolExecutor ──")

# ── 2. ThreadPoolExecutor ────────────────────────────────
def pool_vazifa(nom):
    for i in range(1, 4):
        print(f"[Pool: {nom}] → {i}")
        time.sleep(0.1)

with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(pool_vazifa, ["X-vazifa", "Y-vazifa", "Z-vazifa"])

print("\nBarcha vazifalar bajarildi!")



#8. Asyncio (Asynchronous)




import asyncio
import time

# ── 3 ta async vazifa ────────────────────────────────────
async def vazifa_a():
    print("[A] boshlandi")
    await asyncio.sleep(2)        # 2 soniya kutish (bloklashmaydi)
    print("[A] tugadi")
    return "A natija"

async def vazifa_b():
    print("[B] boshlandi")
    await asyncio.sleep(3)        # 3 soniya kutish
    print("[B] tugadi")
    return "B natija"

async def vazifa_c():
    print("[C] boshlandi")
    await asyncio.sleep(1)        # 1 soniya kutish
    print("[C] tugadi")
    return "C natija"

# ── Bosh funksiya ─────────────────────────────────────────
async def main():
    boshlandi = time.perf_counter()

    # Uchala vazifa bir vaqtda ishlaydi
    natijalar = await asyncio.gather(
        vazifa_a(),
        vazifa_b(),
        vazifa_c()
    )

    tugadi = time.perf_counter()
    jami   = tugadi - boshlandi

    print("\nNatijalar:", natijalar)
    print(f"Umumiy vaqt: {jami:.2f} soniya")
    print(f"(Ketma-ket bo'lsa: {2+3+1} soniya bo'lardi)")

asyncio.run(main())

#9. SMTP / Gmail
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email: str, subject: str, html_body: str):
    # Email tuzish
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    # HTML body qo'shish
    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    # Gmail SMTP orqali yuborish
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email yuborildi: {to_email}")

# HTML body
html_content = """
<html>
  <body>
    <h2 style="color: #4CAF50;">Salom! 👋</h2>
    <p>Bu <b>Python</b> orqali yuborilgan test email.</p>
    <hr>
    <p style="color: gray; font-size: 12px;">
      Yuborildi: smtplib + Gmail
    </p>
  </body>
</html>
"""

# Ishga tushirish
send_email(
    to_email="qabul@example.com",
    subject="Test Email - Python SMTP",
    html_body=html_content
)


#10-misol
import tkinter as tk

def calculate(op):
    try:
        a = float(entry1.get())
        b = float(entry2.get())

        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        elif op == '*':
            result = a * b
        elif op == '/':
            if b == 0:
                result_label.config(text="Xato: 0 ga bo'lib bo'lmaydi!", fg="red")
                return
            result = a / b

        # Natijani chiroyli ko'rsatish
        if result == int(result):
            result_label.config(text=f"Natija: {int(result)}", fg="green")
        else:
            result_label.config(text=f"Natija: {round(result, 6)}", fg="green")

    except ValueError:
        result_label.config(text="Xato: Son kiriting!", fg="red")


root = tk.Tk()
root.title("Kalkulyator")
root.geometry("300x280")
root.resizable(False, False)


tk.Label(root, text="1-son:", font=("Arial", 11)).pack(pady=(20, 2))
entry1 = tk.Entry(root, font=("Arial", 13), width=20, justify="center")
entry1.pack()

tk.Label(root, text="2-son:", font=("Arial", 11)).pack(pady=(10, 2))
entry2 = tk.Entry(root, font=("Arial", 13), width=20, justify="center")
entry2.pack()


btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

for op, symbol in [('+', '+'), ('-', '−'), ('*', '×'), ('/', '÷')]:
    tk.Button(
        btn_frame,
        text=symbol,
        width=5,
        height=2,
        font=("Arial", 14, "bold"),
        command=lambda o=op: calculate(o)
    ).pack(side="left", padx=4)


result_label = tk.Label(root, text="Natija: —", font=("Arial", 13), fg="gray")
result_label.pack(pady=5)

root.mainloop()



#11Git / GitHub


import os
from  import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

print(db_name, db_user, db_password, db_host, db_port)

#12 misol


from dotenv import load_dotenv
import os
from typing import NamedTuple
from dataclasses import dataclass


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

print("Bot token:", BOT_TOKEN)
print("Database user:", DB_USER)
print("Database password:", DB_PASS)
 

class StudentNT(NamedTuple):
    id: int
    name: str
    age: int

student1 = StudentNT(1, "Lazizjon", 20)
print("NamedTuple student:", student1)


@dataclass
class StudentDC:
    id: int
    name: str
    age: int = 18

student2 = StudentDC(2, "Lazizjon")
student2.age = 21  
print("DataClass student:", student2)

#15 savol

from typing import NamedTuple
from dataclasses import dataclass

# 1. NamedTuple misoli (immutable)
class StudentNT(NamedTuple):
    id: int
    name: str
    age: int

student1 = StudentNT(1, "Lazizjon", 20)
print("NamedTuple student:", student1)



@dataclass
class StudentDC:
    id: int
    name: str
    age: int = 18  

    # Qo‘shimcha metod
    def full_info(self):
        return f"ID: {self.id}, Name: {self.name}, Age: {self.age}"

student2 = StudentDC(2, "Lazizjon")
print("DataClass student:", student2)
student2.age = 21  # ✅ O‘zgartirish mumkin
print("DataClass full info:", student2.full_info())



