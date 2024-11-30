import sqlite3
from datetime import datetime

# Inisialisasi database
conn = sqlite3.connect("habit_tracker.db")
cursor = conn.cursor()

# Membuat tabel untuk kebiasaan
cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATE NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES habits (id)
)
""")
conn.commit()

# Fungsi untuk menambahkan kebiasaan baru
def add_habit(name):
    cursor.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, datetime.now().date()))
    conn.commit()
    print(f"Kebiasaan '{name}' berhasil ditambahkan.")

# Fungsi untuk melihat semua kebiasaan
def view_habits():
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    if habits:
        print("Daftar Kebiasaan:")
        for habit in habits:
            print(f"- {habit[0]}. {habit[1]} (dibuat pada {habit[2]})")
    else:
        print("Belum ada kebiasaan.")

# Fungsi untuk menandai kebiasaan selesai
def mark_habit_done(habit_id):
    today = datetime.now().date()
    cursor.execute("INSERT INTO habit_logs (habit_id, date) VALUES (?, ?)", (habit_id, today))
    conn.commit()
    print(f"Kebiasaan ID {habit_id} telah ditandai selesai untuk hari ini.")

# Fungsi untuk melihat riwayat kebiasaan
def view_habit_logs(habit_id):
    cursor.execute("SELECT date FROM habit_logs WHERE habit_id = ?", (habit_id,))
    logs = cursor.fetchall()
    if logs:
        print(f"Riwayat Kebiasaan ID {habit_id}:")
        for log in logs:
            print(f"- {log[0]}")
    else:
        print(f"Tidak ada log untuk kebiasaan ID {habit_id}.")

# Menu interaktif
def menu():
    while True:
        print("\n=== Habit Tracker ===")
        print("1. Tambah Kebiasaan")
        print("2. Lihat Kebiasaan")
        print("3. Tandai Kebiasaan Selesai")
        print("4. Lihat Riwayat Kebiasaan")
        print("5. Keluar")
        choice = input("Pilih opsi: ")

        if choice == "1":
            name = input("Masukkan nama kebiasaan: ")
            add_habit(name)
        elif choice == "2":
            view_habits()
        elif choice == "3":
            habit_id = int(input("Masukkan ID kebiasaan: "))
            mark_habit_done(habit_id)
        elif choice == "4":
            habit_id = int(input("Masukkan ID kebiasaan: "))
            view_habit_logs(habit_id)
        elif choice == "5":
            print("Terima kasih telah menggunakan Habit Tracker!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

# Menjalankan menu
menu()

# Menutup koneksi database
conn.close()