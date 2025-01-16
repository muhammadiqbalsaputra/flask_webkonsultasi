from flask import Flask, render_template, request, redirect, url_for
from DB_Operations import get_konsultasi_data, update_balasan, get_konsultasi, insert_balasan

import pymysql

app = Flask(__name__)

# Route untuk halaman Beranda
@app.route('/')
def beranda():
    return render_template('beranda.html')

# Route untuk halaman Tentang
@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/formkonsultasi')
def formKonsul():
    return render_template('formKonsultasi.html')

# Route untuk halaman Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Proses login (misalnya, validasi dengan data user)
        return f"Login berhasil! Selamat datang, {username}."
    return render_template('login.html')

# konsultasi
@app.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi():
    connection = pymysql.connect(host='localhost', user='root', password='', db='webkonsultasi')
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

if __name__ == '__main__':
    app.run(debug=True)
