import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Algoritma enkripsi
# caesar
def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Vigenere
def vigenere_encrypt(text, key):
    result, key_idx = "", 0
    key = key.lower()
    for ch in text:
        if ch.isalpha():
            k = ord(key[key_idx % len(key)]) - 97
            base = 65 if ch.isupper() else 97
            result += chr((ord(ch) - base + k) % 26 + base)
            key_idx += 1
        else:
            result += ch
    return result

def vigenere_decrypt(text, key):
    result, key_idx = "", 0
    key = key.lower()
    for ch in text:
        if ch.isalpha():
            k = ord(key[key_idx % len(key)]) - 97
            base = 65 if ch.isupper() else 97
            result += chr((ord(ch) - base - k) % 26 + base)
            key_idx += 1
        else:
            result += ch
    return result

# XOR
def xor_encrypt(text, key):
    key = key.encode('utf-8')
    text = text.encode('utf-8')
    result = bytearray()
    for i in range(len(text)):
        result.append(text[i] ^ key[i % len(key)])
    return base64.b64encode(result).decode('utf-8')

def xor_decrypt(cipher, key):
    data = base64.b64decode(cipher)
    key = key.encode('utf-8')
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ key[i % len(key)])
    return result.decode('utf-8')

# Block Cipher
def block_encrypt(text, key):
    key_bytes = key.encode('utf-8').ljust(16, b'0')[:16]
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def block_decrypt(cipher, key):
    key_bytes = key.encode('utf-8').ljust(16, b'0')[:16]
    cipher_aes = AES.new(key_bytes, AES.MODE_ECB)
    ct = base64.b64decode(cipher)
    pt = unpad(cipher_aes.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# Super Enkrip
def super_encrypt(text, caesar_shift, vig_key, xor_key, block_key):
    step1 = caesar_encrypt(text, caesar_shift)
    step2 = vigenere_encrypt(step1, vig_key)
    step3 = xor_encrypt(step2, xor_key)
    step4 = block_encrypt(step3, block_key)
    return step4

def super_decrypt(cipher, caesar_shift, vig_key, xor_key, block_key):
    step1 = block_decrypt(cipher, block_key)
    step2 = xor_decrypt(step1, xor_key)
    step3 = vigenere_decrypt(step2, vig_key)
    step4 = caesar_decrypt(step3, caesar_shift)
    return step4

# GUI
def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)
    shift_entry.delete(0, tk.END)
    status_label.config(text="Siap untuk digunakan", foreground="black")

def copy_output():
    output = output_text.get("1.0", tk.END).strip()
    if output:
        root.clipboard_clear()
        root.clipboard_append(output)
        messagebox.showinfo("✓ Berhasil", "Output berhasil disalin ke clipboard!", parent=root)
    else:
        messagebox.showwarning("⚠️ Peringatan", "Output masih kosong!", parent=root)

def on_algo_change(event=None):
    algo = algo_choice.get()
    descriptions = {
        "Caesar": "🔢 Geser huruf dengan angka tertentu\nContoh: A→D (shift 3)",
        "Vigenere": "🔤 Menggunakan kata kunci huruf (A-Z)\nKey harus huruf saja!",
        "XOR": "⚡ XOR sederhana\nKey boleh huruf, angka, simbol",
        "Block": "🧱 Block Cipher (AES-128, ECB)\nKey otomatis dipotong/panjangin jadi 16 byte",
        "Super": "🚀 Kombinasi Caesar → Vigenere → XOR → Block\nPaling aman!"
    }
    algo_info_label.config(text=descriptions.get(algo, ""))

    if algo in ["Caesar", "Super"]:
        shift_entry.config(state="normal")
        shift_label.config(foreground="black")
    else:
        shift_entry.delete(0, tk.END)
        shift_entry.config(state="disabled")
        shift_label.config(foreground="gray")

    if algo in ["Vigenere", "XOR", "Block", "Super"]:
        key_entry.config(state="normal")
        key_label.config(foreground="black")
    else:
        key_entry.delete(0, tk.END)
        key_entry.config(state="disabled")
        key_label.config(foreground="gray")

def process():
    algo = algo_choice.get()
    mode = mode_choice.get()
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    shift_input = shift_entry.get().strip()

    try:
        if not text:
            raise ValueError("Input teks tidak boleh kosong!")

        shift = int(shift_input) if shift_input else 0

        if algo == "Caesar":
            result = caesar_encrypt(text, shift) if mode == "Encrypt" else caesar_decrypt(text, shift)
        elif algo == "Vigenere":
            if not key.isalpha():
                raise ValueError("Key Vigenere harus berupa huruf saja!")
            result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)
        elif algo == "XOR":
            if not key:
                raise ValueError("Key XOR tidak boleh kosong!")
            result = xor_encrypt(text, key) if mode == "Encrypt" else xor_decrypt(text, key)
        elif algo == "Block":
            if not key:
                raise ValueError("Key Block Cipher tidak boleh kosong!")
            result = block_encrypt(text, key) if mode == "Encrypt" else block_decrypt(text, key)
        elif algo == "Super":
            if not key.isalpha():
                raise ValueError("Key Super harus berupa huruf saja!")
            result = super_encrypt(text, shift, key, key, key) if mode == "Encrypt" else super_decrypt(text, shift, key, key, key)
        else:
            raise ValueError("Algoritma tidak dikenali!")

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        status_label.config(text=f"✓ {mode} berhasil! | Algoritma: {algo}", foreground="green")

    except Exception as e:
        output_text.delete("1.0", tk.END)
        status_label.config(text="✗ Terjadi kesalahan!", foreground="red")
        messagebox.showerror("Error", str(e), parent=root)

# GUI Utama
root = tk.Tk()
root.title("🔐 Aplikasi Kriptografi")
root.configure(bg="#eaeaea")

style = ttk.Style()
style.theme_use('clam')

main_frame = ttk.Frame(root, padding="15 15 15 15")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Header
header_frame = tk.Frame(main_frame, bg="#3498db", relief=tk.RIDGE, bd=3)
header_frame.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
header_label = tk.Label(header_frame, text="🔐 APLIKASI KRIPTOGRAFI", 
                        font=("Arial", 18, "bold"), fg="white", bg="#3498db", pady=10)
header_label.pack()

# Frame
algo_frame = ttk.LabelFrame(main_frame, text="⚙️ Pengaturan Algoritma", padding="12 8 12 8", relief="groove")
algo_frame.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
ttk.Label(algo_frame, text="Pilih Algoritma:", font=("Arial", 10, "bold")).grid(column=0, row=0, padx=5, pady=5, sticky="w")
algo_choice = ttk.Combobox(algo_frame, values=["Caesar", "Vigenere", "XOR", "Block", "Super"], state="readonly", width=25)
algo_choice.grid(column=1, row=0, padx=5, pady=5, sticky="ew")
algo_choice.current(0)
algo_choice.bind("<<ComboboxSelected>>", on_algo_change)
algo_info_label = ttk.Label(algo_frame, text="", font=("Arial", 9), foreground="#555", wraplength=400)
algo_info_label.grid(column=0, row=1, columnspan=2, padx=5, pady=(0, 10), sticky="w")
ttk.Label(algo_frame, text="Pilih Mode:", font=("Arial", 10, "bold")).grid(column=0, row=2, padx=5, pady=5, sticky="w")
mode_choice = ttk.Combobox(algo_frame, values=["Encrypt", "Decrypt"], state="readonly", width=25)
mode_choice.grid(column=1, row=2, padx=5, pady=5, sticky="ew")
mode_choice.current(0)

# Input
input_frame = ttk.LabelFrame(main_frame, text="✍️ Masukkan Teks", padding="12 8 12 8", relief="groove")
input_frame.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
input_text = scrolledtext.ScrolledText(input_frame, width=65, height=5, font=("Consolas", 10), wrap=tk.WORD)
input_text.grid(column=0, row=0, padx=5, pady=5)

# Key
key_frame = ttk.LabelFrame(main_frame, text="🔑 Key (Kunci Rahasia)", padding="12 8 12 8", relief="groove")
key_frame.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
key_label = ttk.Label(key_frame, text="Key:", font=("Arial", 10, "bold"))
key_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
key_entry = ttk.Entry(key_frame, width=40, font=("Arial", 11))
key_entry.grid(column=1, row=0, padx=5, pady=5, sticky="ew")
key_info = ttk.Label(key_frame, 
                     text="💡 Vigenere/Super: HURUF saja | XOR/Block: Semua karakter", 
                     font=("Arial", 8), foreground="#555", justify="left")
key_info.grid(column=1, row=1, padx=5, pady=0, sticky="w")

# Shift
shift_frame = ttk.LabelFrame(main_frame, text="🔢 Shift (Pergeseran)", padding="12 8 12 8", relief="groove")
shift_frame.grid(column=0, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
shift_label = ttk.Label(shift_frame, text="Shift:", font=("Arial", 10, "bold"))
shift_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
shift_entry = ttk.Entry(shift_frame, width=40, font=("Arial", 11))
shift_entry.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

# Tombol
button_frame = ttk.Frame(main_frame, padding="5")
button_frame.grid(column=0, row=5, columnspan=2, pady=10)
ttk.Button(button_frame, text="🔄 Proses", command=process, width=15).grid(column=0, row=0, padx=5)
ttk.Button(button_frame, text="📋 Salin Output", command=copy_output, width=15).grid(column=1, row=0, padx=5)
ttk.Button(button_frame, text="🗑️ Bersihkan", command=clear_all, width=15).grid(column=2, row=0, padx=5)

# Output
output_frame = ttk.LabelFrame(main_frame, text="📄 Output", padding="12 8 12 8", relief="groove")
output_frame.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
output_text = scrolledtext.ScrolledText(output_frame, width=65, height=5, font=("Consolas", 10), wrap=tk.WORD, bg="#f8f9fa")
output_text.grid(column=0, row=0, padx=5, pady=5)

# Status bar
status_label = tk.Label(main_frame, text="Siap untuk digunakan", font=("Arial", 9), anchor="w", relief=tk.SUNKEN)
status_label.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

on_algo_change()

root.update_idletasks()
root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
root.mainloop()
