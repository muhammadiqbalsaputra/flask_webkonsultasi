from flask import Flask, render_template, request, redirect, url_for, session
from DB_Operations import get_konsultasi_data, update_balasan, get_konsultasi, insert_balasan, connect_db, validate_login

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = validate_login(username, password)
        # Verifikasi username dan password
        if user:
            session['username'] = username
            return redirect(url_for('konsultasidokter'))
        else:
            return "Login gagal! Username atau password salah."
    
    return render_template('login.html')

@app.route('/konsultasidokter')
def konsultasidokter():
    # Halaman setelah login berhasil
    return render_template('dokter/konsultasidokter.html')

if __name__ == '__main__':
    app.run(debug=True)
