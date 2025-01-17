from flask import Flask, render_template, request, redirect, url_for, session
from DB_Operations import fetch_all_konsultasi, insert_balasan, connect_db, validate_user, fetch_all_items,delete_konsultasi,update_konsultasi_balasan,insert_consultation

import pymysql
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Route untuk halaman Beranda
@app.route('/')
def beranda():
    items = fetch_all_items()
    return render_template('beranda.html', items=items)

# Route untuk halaman Tentang
@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/formkonsultasi', methods=['GET', 'POST'])
def formKonsul():
    if request.method == 'POST':
        nama = request.form['nama']
        keluhan = request.form['keluhan']
        
        # Simpan data ke database menggunakan fungsi insert_consultation
        insert_consultation(nama, keluhan)
        
        # Redirect ke halaman sukses atau halaman konsultasi
        return redirect('/konsultasi')  # Redirect ke halaman konsultasi setelah berhasil input
    
    # Jika metode GET, tampilkan halaman form
    return render_template('formKonsultasi.html')

# konsultasi
@app.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi():
    connection = connect_db()
    cursor = connection.cursor()

    # Menampilkan data konsultasi
    cursor.execute("SELECT id, nama, keluhan, tanggal_konsultasi, balasan FROM konsultasi")
    data_konsultasi = cursor.fetchall()

    if request.method == 'POST':
        id_konsultasi = request.form['id_konsultasi']
        balasan_dokter = request.form['balasan']    

        # Menyimpan balasan ke database
        insert_balasan(id_konsultasi, balasan_dokter)
    
    connection.close()
    return render_template('konsultasi.html', data=data_konsultasi)

# form login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = validate_user(username, password)
        if user:
            session['username'] = username
            return redirect('/konsultasidokter')  
        else:
            error = "Username dan Password Tidak Tersedia."

    return render_template('login.html', error=error)

# Route untuk halaman konsultasi dokter setelah login
@app.route('/konsultasidokter')
def konsultasidokter():
    if 'username' not in session:
        return redirect(url_for('login'))  # Pastikan user login sebelum mengakses halaman

    connection = connect_db()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id, nama, keluhan, tanggal_konsultasi, balasan FROM konsultasi")
            data_konsultasi = cursor.fetchall()
    finally:
        connection.close()

    return render_template('dokter/konsultasidokter.html', data=data_konsultasi)


# Route untuk logout
@app.route('/logout')
def logout():
    session.pop('username', None) 
    items = fetch_all_konsultasi()
    return render_template('beranda.html', items=items)

@app.route('/konsultasidokter/<int:id>/balas', methods=['POST'])
def balas_konsultasi(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    balasan = request.form['balasan']
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            query = "UPDATE konsultasi SET balasan = %s WHERE id = %s"
            cursor.execute(query, (balasan, id))
            connection.commit()
    finally:
        connection.close()

    return redirect('/konsultasidokter')

# Route untuk mengedit konsultasi
@app.route('/konsultasidokter/<int:id>/edit', methods=['GET', 'POST'])
def edit_konsultasi(id):
    connection = connect_db()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Ambil data konsultasi berdasarkan ID
            cursor.execute("SELECT id, nama, keluhan, tanggal_konsultasi, balasan FROM konsultasi WHERE id = %s", (id,))
            konsultasi = cursor.fetchone()
            
            if not konsultasi:
                return "Data konsultasi tidak ditemukan.", 404
            
            if request.method == 'POST':
                # Ambil data dari form
                balasan = request.form['balasan']
                
                # Perbarui data di database
                cursor.execute("UPDATE konsultasi SET balasan = %s WHERE id = %s", (balasan, id))
                connection.commit()
                return redirect(url_for('konsultasidokter'))  # Kembali ke halaman konsultasi dokter
    finally:
        connection.close()

    return render_template('dokter/edit_konsultasi.html', konsultasi=konsultasi)



# Route untuk menghapus konsultasi
@app.route('/konsultasidokter/<int:id>/hapus', methods=['GET'])
def hapus_konsultasi(id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # Query untuk menghapus konsultasi berdasarkan ID
            cursor.execute("DELETE FROM konsultasi WHERE id = %s", (id,))
            connection.commit()  # Pastikan perubahan disimpan ke database
    finally:
        connection.close()

    # Setelah penghapusan, kembali ke halaman konsultasi dokter
    return redirect('/konsultasidokter')


if __name__ == '__main__':
    app.run(debug=True)
