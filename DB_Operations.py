import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',  # sesuaikan dengan username database Anda
        password='',  # sesuaikan dengan password database Anda
        database='webkonsultasi'  # sesuaikan dengan nama database Anda
    )

def insert_consultation(nama, keluhan):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO konsultasi (nama, keluhan, tanggal_konsultasi) VALUES (%s, %s, NOW())"
            cursor.execute(query, (nama, keluhan))
            conn.commit()
    finally:
        conn.close()

def get_all_consultations():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = "SELECT nama, keluhan, tanggal_konsultasi FROM konsultasi"
            cursor.execute(query)
            return cursor.fetchall()  # Mengembalikan semua hasil query
    finally:
        conn.close()

def get_konsultasi_data():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Query untuk mengambil data konsultasi
            query = "SELECT nama, keluhan, tanggal_konsultasi FROM konsultasi"
            cursor.execute(query)
            
            # Mengambil semua hasil query
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def update_balasan(konsultasi_id, balasan):
    # Koneksi ke database
    conn = connect_db()
    
    try:
        with conn.cursor() as cursor:
            # Query untuk memperbarui balasan konsultasi
            query = "UPDATE konsultasi SET balasan = %s WHERE id = %s"
            cursor.execute(query, (balasan, konsultasi_id))
            conn.commit()
    finally:
        conn.close()

def insert_balasan(id_konsultasi, balasan):
    connection = pymysql.connect(host='localhost', user='root', password='', db='mari_peduli')
    cursor = connection.cursor()
    
    sql = "UPDATE konsultasi SET balasan = %s WHERE id = %s"
    cursor.execute(sql, (balasan, id_konsultasi))
    connection.commit()
    connection.close()

def get_konsultasi():
    connection = pymysql.connect(host='localhost', user='root', password='', db='mari_peduli')
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, nama, keluhan, tanggal_konsultasi, balasan FROM konsultasi")
    data = cursor.fetchall()
    
    connection.close()
    return data