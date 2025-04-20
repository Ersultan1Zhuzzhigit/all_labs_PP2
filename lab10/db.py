import psycopg2
import csv

conn = psycopg2.connect(
    dbname="postgres",      
    user="postgres",     
    password="1234",   
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100),
        phone VARCHAR(20) UNIQUE
    );
""")
conn.commit()

def load_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", 
                        (row['username'], row['phone']))
    conn.commit()
    print("✅ CSV файлдан мәлімет жүктелді.")

def insert_manual():
    username = input("👤 Username енгізіңіз: ")
    phone = input("📞 Телефон нөмірін енгізіңіз: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", 
                (username, phone))
    conn.commit()
    print("✅ Мәлімет қосылды.")

def update_data():
    old_username = input("Қай қолданушыны жаңартасыз (username): ").strip()
    cur.execute("SELECT id FROM phonebook WHERE username = %s", (old_username,))
    record = cur.fetchone()
    if not record:
        print(f"❌ Қолданушы '{old_username}' табылмады.")
        return
    user_id = record[0]

    new_username = input("Жаңа username енгізіңіз: ").strip()
    new_phone = input("Жаңа телефон нөмірін енгізіңіз: ").strip()
    cur.execute(
        "UPDATE phonebook SET username = %s, phone = %s WHERE id = %s",
        (new_username, new_phone, user_id)
    )
    conn.commit()
    print("✅ Мәлімет жаңартылды.")


def search_data():
    search_name = input("Іздейтін username: ")
    cur.execute("SELECT * FROM phonebook WHERE username = %s", (search_name,))
    results = cur.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("❌ Қолданушы табылмады.")
        

def show_all_data():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    if rows:
        print("\n📋 Барлық жазбалар:")
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Phone: {row[2]}")
    else:
        print("❗ Мәліметтер базасы бос.")


def delete_data():
    field = input("Неден өшіргіңіз келеді? (username/phone): ")
    value = input("Мәні: ")
    if field == "username":
        cur.execute("DELETE FROM phonebook WHERE username = %s", (value,))
    elif field == "phone":
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (value,))
    else:
        print("❌ Қате өріс!")
        return
    conn.commit()
    print("✅ Мәлімет өшірілді.")

def menu():
    while True:
        print("\n📱 PhoneBook Мәзірі:")
        print("1 - CSV файлдан жүктеу")
        print("2 - Қолмен мәлімет қосу")
        print("3 - Мәлімет жаңарту")
        print("4 - Мәлімет іздеу")
        print("5 - Мәлімет өшіру")
        print("6 - Барлық мәліметтерді көру")
        print("0 - Шығу")
        choice = input("Таңдаңыз: ")

        if choice == "1":
            load_from_csv("C:/HW_Labs/lab10/contacts.csv")
        elif choice == "2":
            insert_manual()
        elif choice == "3":
            update_data()
        elif choice == "4":
            search_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            show_all_data()
        elif choice == "0":
            break
        else:
            print("❗ Дұрыс таңдау енгізіңіз!")

    cur.close()
    conn.close()
    print("🔒 Қосылым жабылды.")

if __name__ == "__main__":
    menu()