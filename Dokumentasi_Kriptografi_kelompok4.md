# Dokumentasi Aplikasi Kriptografi Kelompok 4

### 123230092(Martin Aji Nugraha)
### 123230097(Faisal Dani Noto Legowo)
### 123230108(Muhammad Furaihan)

## 1. Deskripsi Program

Aplikasi ini adalah **aplikasi GUI kriptografi** berbasis Python dengan
library **Tkinter**.
Pengguna dapat melakukan **enkripsi** dan **dekripsi** teks menggunakan
beberapa algoritma klasik maupun modern.
Aplikasi ini ditujukan sebagai media pembelajaran kriptografi dasar dan
demonstrasi cara kerja berbagai algoritma.


## 2. Fitur Utama

-   **Pilihan Algoritma**:
    1.  Caesar Cipher
    2.  Vigenere Cipher
    3.  XOR Cipher
    4.  Block Cipher (AES, mode ECB)
    5.  Super Encryption (kombinasi Caesar → Vigenere → XOR → Block)
-   **Mode Operasi**:
    -   `Encrypt` → mengenkripsi teks input
    -   `Decrypt` → mendekripsi ciphertext
-   **Input dan Output**:
    -   Input teks bebas
    -   Key (berbeda aturan sesuai algoritma)
    -   Shift (khusus untuk Caesar dan Super)
    -   Output dapat disalin ke clipboard
-   **Validasi Input**:
    -   Tidak boleh kosong
    -   Key Vigenere/Super harus huruf
    -   Key XOR/Block bebas (huruf, angka, simbol)
    -   Shift harus berupa angka


## 3. Algoritma yang Digunakan

### 🔹 Caesar Cipher

Metode enkripsi klasik dengan pergeseran huruf sejauh nilai **shift**
tertentu.
Contoh: `A` dengan shift 3 → `D`.

### 🔹 Vigenere Cipher

Menggunakan kata kunci (**key**) untuk menentukan pergeseran tiap
huruf.
Lebih aman dibanding Caesar karena setiap huruf dapat digeser berbeda.

### 🔹 XOR Cipher

Menggunakan operasi **bitwise XOR** antara teks dan kunci.
Kunci bisa berupa huruf, angka, maupun simbol.
Enkripsi dan dekripsi dilakukan dengan operasi yang sama.

### 🔹 Block Cipher (AES, ECB)

Menggunakan algoritma modern AES (Advanced Encryption Standard).
Key diatur agar panjangnya **16 byte** (AES-128).
Teks dipecah menjadi blok-blok untuk dienkripsi.

### 🔹 Super Encryption

Kombinasi berurutan dari beberapa algoritma: 1. Caesar → 2. Vigenere →
3. XOR → 4. Block (AES)
Tujuannya memperkuat keamanan dengan beberapa lapisan enkripsi.


## 4. Struktur Program

1.  **Import Library**
    -   `tkinter`, `ttk`, `scrolledtext`, `messagebox` → GUI
    -   `base64` → encoding hasil XOR/Block
    -   `AES`, `pad`, `unpad` → Block Cipher
2.  **Definisi Algoritma**
    -   Fungsi `caesar_encrypt`, `vigenere_encrypt`, `xor_encrypt`,
        `block_encrypt`, `super_encrypt`
    -   Fungsi dekripsi untuk masing-masing algoritma
3.  **Fungsi Pendukung GUI**
    -   `clear_all()` → menghapus input/output
    -   `copy_output()` → menyalin hasil ke clipboard
    -   `on_algo_change()` → menyesuaikan tampilan input sesuai
        algoritma
    -   `process()` → menjalankan proses enkripsi/dekripsi
4.  **Layout GUI**
    -   Frame utama
    -   Header aplikasi
    -   Dropdown algoritma & mode
    -   Input teks, key, shift
    -   Tombol proses, clear, copy
    -   Output area dan status bar
5.  **Main Loop**
    -   `root.mainloop()` untuk menjalankan aplikasi.


## 5. Cara Menjalankan

1.  Pastikan Python sudah terinstall.

2.  Install library tambahan:

    ``` bash
    pip install pycryptodome
    ```

3.  Simpan kode Python sebagai `app.py`.

4.  Jalankan dengan:

    ``` bash
    python app.py
    ```

5.  GUI aplikasi akan muncul di layar.


## 6. Aturan Penggunaan

-   **Caesar** → membutuhkan input **Shift (angka 1--25)**.
-   **Vigenere** → membutuhkan **Key berupa huruf saja (A--Z)**.
-   **XOR** → membutuhkan **Key bebas (huruf, angka, simbol)**.
-   **Block** → membutuhkan **Key bebas**, otomatis dipotong/ditambah
    menjadi 16 byte.
-   **Super** → membutuhkan **Shift (angka)** dan **Key berupa huruf
    saja**.


## 7. Tampilan GUI

-   Header aplikasi dengan judul
-   Area pilihan algoritma dan mode
-   Kolom input teks, key, dan shift
-   Tombol `Proses`, `Salin Output`, dan `Bersihkan`
-   Output area untuk menampilkan hasil
-   Status bar untuk menunjukkan status proses

