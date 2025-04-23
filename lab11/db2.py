
import psycopg2
from psycopg2.extras import Json
import csv
import os

DSN = {
    "dbname": "Erss",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def get_conn():
    return psycopg2.connect(**DSN)

def ensure_db():
    """
    Drop and recreate the phonebook table & all PL/pgSQL routines
    to avoid signature conflicts.
    """
    ddl = r"""
    -- 0. Table
    CREATE TABLE IF NOT EXISTS phonebook (
        first_name VARCHAR(100),
        surname    VARCHAR(100),
        phone      VARCHAR(20) NOT NULL,
        PRIMARY KEY (first_name, surname)
    );

    -- 1. search by pattern
    DROP FUNCTION IF EXISTS search_phonebook(TEXT);
    CREATE FUNCTION search_phonebook(p_pattern TEXT)
      RETURNS TABLE(first_name VARCHAR, surname VARCHAR, phone VARCHAR)
    LANGUAGE sql AS $$
      SELECT first_name, surname, phone
        FROM phonebook
       WHERE first_name ILIKE '%' || p_pattern || '%'
          OR surname    ILIKE '%' || p_pattern || '%'
          OR phone      LIKE  '%' || p_pattern || '%';
    $$;

    -- 2. upsert
    DROP PROCEDURE IF EXISTS upsert_user(TEXT, TEXT, TEXT);
    CREATE PROCEDURE upsert_user(
      p_fname   TEXT,
      p_surname TEXT,
      p_phone   TEXT
    )
    LANGUAGE plpgsql AS $$
    BEGIN
      IF EXISTS (
        SELECT 1 FROM phonebook
         WHERE first_name = p_fname
           AND surname    = p_surname
      ) THEN
        UPDATE phonebook
           SET phone = p_phone
         WHERE first_name = p_fname
           AND surname    = p_surname;
      ELSE
        INSERT INTO phonebook(first_name, surname, phone)
        VALUES (p_fname, p_surname, p_phone);
      END IF;
    END;
    $$;

    -- 3. bulk insert with validation
    DROP FUNCTION IF EXISTS insert_many_users(JSON);
    CREATE FUNCTION insert_many_users(p_users JSON)
      RETURNS TABLE(bad_fname TEXT, bad_surname TEXT, bad_phone TEXT)
    LANGUAGE plpgsql AS $$
    DECLARE u JSON;
    BEGIN
      FOR u IN SELECT * FROM json_array_elements(p_users) LOOP
        IF (u->>'phone') ~ '^[0-9]{7,15}$' THEN
          CALL upsert_user(
            u->>'first_name',
            u->>'surname',
            u->>'phone'
          );
        ELSE
          bad_fname   := u->>'first_name';
          bad_surname := u->>'surname';
          bad_phone   := u->>'phone';
          RETURN NEXT;
        END IF;
      END LOOP;
    END;
    $$;

    -- 4. pagination
    DROP FUNCTION IF EXISTS list_users(INT, INT);
    CREATE FUNCTION list_users(p_limit INT, p_offset INT)
      RETURNS TABLE(first_name VARCHAR, surname VARCHAR, phone VARCHAR)
    LANGUAGE sql AS $$
      SELECT first_name, surname, phone
        FROM phonebook
       ORDER BY first_name, surname
       LIMIT p_limit
      OFFSET p_offset;
    $$;

    -- 5. delete
    DROP PROCEDURE IF EXISTS delete_user(TEXT);
    CREATE PROCEDURE delete_user(p_id TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
      DELETE FROM phonebook
       WHERE first_name = p_id
          OR surname    = p_id
          OR phone      = p_id;
    END;
    $$;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(ddl)
    print("✅ Table and all routines dropped & recreated.")

def normalize_path(raw: str) -> str:
    p = raw.strip().strip('"').replace('\\', '/')
    return os.path.normpath(p)

def load_from_csv(path: str):
    path = normalize_path(path)
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            fn = r.get("first_name", "").strip()
            ln = r.get("surname", "").strip()
            ph = r.get("phone", "").strip()
            if fn and ln and ph:
                rows.append({"first_name": fn, "surname": ln, "phone": ph})

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM insert_many_users(%s)", (Json(rows),))
        invalid = cur.fetchall()

    if invalid:
        print("⚠️ Invalid rows:")
        for fn, ln, ph in invalid:
            print(f"  • {fn} {ln} → {ph}")
    else:
        print("✅ CSV imported.")

def insert_manual():
    fn = input("👤 First name: ").strip()
    ln = input("👤  Surname: ").strip()
    ph = input("📞 Phone: ").strip()
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "CALL upsert_user(%s::text, %s::text, %s::text)",
            (fn, ln, ph)
        )
        conn.commit()
    print("✅ Upserted.")

def search_data():
    pat = input("🔎 Pattern: ").strip()
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM search_phonebook(%s)", (pat,))
        rows = cur.fetchall()
    if not rows:
        print("❌ No matches.")
    else:
        for fn, ln, ph in rows:
            print(f"  • {fn} {ln} → {ph}")

def paginate():
    try:
        lim = int(input("Limit: "))
        off = int(input("Offset: "))
    except ValueError:
        print("❌ Must be integers.")
        return
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM list_users(%s::integer, %s::integer)",
            (lim, off)
        )
        rows = cur.fetchall()
    for fn, ln, ph in rows:
        print(f"  • {fn} {ln} → {ph}")

def delete_data():
    val = input("🗑️  Delete by (first name, surname, or phone): ").strip()
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("CALL delete_user(%s::text)", (val,))
        conn.commit()
    print("✅ Deleted.")

def show_all():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM list_users(%s::integer, %s::integer)",
            (1000, 0)
        )
        rows = cur.fetchall()
    if not rows:
        print("📭 Empty.")
    else:
        for fn, ln, ph in rows:
            print(f"  • {fn} {ln} → {ph}")

def menu():
    ensure_db()
    while True:
        print("""
📱 PhoneBook CLI
1) Load CSV
2) Insert/Update
3) Search
4) Paginate
5) Delete
6) Show all
0) Exit
""")
        cmd = input("Choice: ").strip()
        if cmd == "1":
            load_from_csv(input("CSV path: "))
        elif cmd == "2":
            insert_manual()
        elif cmd == "3":
            search_data()
        elif cmd == "4":
            paginate()
        elif cmd == "5":
            delete_data()
        elif cmd == "6":
            show_all()
        elif cmd == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
