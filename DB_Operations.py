import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',  # sesuaikan dengan username database Anda
        password='',  # sesuaikan dengan password database Anda
        database='webkonsultasi'  # sesuaikan dengan nama database Anda
    )

def fetch_all_items():
    connect = connect_db()
    try:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM dokter")
            rows = cursor.fetchall()
        return rows
    finally:
        connect.close()

def fetch_all_konsultasi():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM konsultasi")
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def insert_consultation(nama, keluhan):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO konsultasi (nama, keluhan, tanggal_konsultasi) VALUES (%s, %s, NOW())"
            cursor.execute(query, (nama, keluhan))
            conn.commit()
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
    conn = connect_db()
    cursor = conn.cursor()
    
    sql = "UPDATE konsultasi SET balasan = %s WHERE id = %s"
    cursor.execute(sql, (balasan, id_konsultasi))
    conn.commit()
    conn.close()

def get_konsultasi():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nama, keluhan, tanggal_konsultasi, balasan FROM konsultasi")
    data = cursor.fetchall()
    
    conn.close()
    return data


def validate_user(username, password):
    """Validasi username dan password dari database."""
    connection = connect_db() 
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM dokter WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone() 
            return user  
    finally:
        connection.close()

def get_dokter_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dokter")
    rows = cursor.fetchall()
    
    columns = [column[0] for column in cursor.description]  # Mendapatkan nama kolom
    data = [dict(zip(columns, row)) for row in rows]  # Menggabungkan kolom dengan data menjadi dictionary
    
    cursor.close()
    conn.close()
    
    return data

# Function to update a consultation (e.g., reply from doctor)
def update_konsultasi_balasan(konsultasi_id, balasan):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE konsultasi
                SET balasan = %s
                WHERE id = %s
            """, (balasan, konsultasi_id))
            connection.commit()
    finally:
        connection.close()

# Function to delete a consultation
def delete_konsultasi(konsultasi_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM konsultasi WHERE id = %s", (konsultasi_id,))
            connection.commit()
    finally:
        connection.close()