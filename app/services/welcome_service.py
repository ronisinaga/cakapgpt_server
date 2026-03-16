import numpy as np


def welcome_message():
    message1 = "Hai saya OKAPP. Saya dibuat oleh pembuat saya Roni Sinaga. Saya siap untuk membantu kamu dalam menyelesaikan permasalahan yang berkaitan dengan:"
    message2 = "1. Persamaan Linear"
    message3 = "2. Optimasi"
    message4 = "3. Machine Learning"
    message5 = "4. Experimen"
    message6 = "5. Diskusi dengan kamu"
    message7 = "Kamu tinggal tuliskan angka berapa yang ingin kamu pilih"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    arr.append(message5)
    arr.append(message6)
    arr.append(message7)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def wrong_choice_message():
    message1 = "Pilihan tidak dikenali. Kamu cukup menuliskan angka 1..3"
    message2 = "Saya bisa bantu kamu menyelesaikan permasalahan terkait:"
    message3 = "1. Persamaan Linear"
    message4 = "2. Optimasi"
    message5 = "3. Machine Learning"
    message5 = "4. Experimen"
    message6 = "5. Diskusi dengan OKAPP"
    message7 = "Tuliskan angka nomer berapa yang ingin kamu pilih"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    arr.append(message5)
    arr.append(message6)
    arr.append(message7)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def linear_message():
    message1 = "Kamu memilih Persamaan linear. Masukkan persamaan linear kamu. Kamu perlu memperhatikan petunjuk penulisan persamaan linearnya."
    message2 = "kamu bisa menuliskan persamaan linearnya seperti contoh dibawah ini"
    message3 = "1. Variabel persamaan linear"
    message4 = "Kamu harus menuliskan persamaan linear seperti ini 2X1 + X2 - 3X3 = 4. variabelnya harus X, besar kecil tidak berpengaruh dan ada indeksnya"
    message5 = "2. Penulisan persamaan"
    message6 = "Penulisan persamaan bisa dipisahkan dengan koma seperti dibawah ini"
    message7 = "2X1 + X2 - 3X3 = 4, X1 - 2x2 + 4X3 = 5, ...,"
    message8 = "Atau dengan enter kebawah"
    message9 = "2X1 + X2 - 3X3 = 4"
    message10 = "X1 - 2x2 + 4X3 = 5"
    message11 = "..."
    message12 = "Sekarang tuliskan persamaan kamu:"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    arr.append(message5)
    arr.append(message6)
    arr.append(message7)
    arr.append(message8)
    arr.append(message9)
    arr.append(message10)
    arr.append(message11)
    arr.append(message12)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def no_session():
    message1 = "Tidak ada persamaan yang dikirimkan"
    arr = []
    arr.append(message1)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def no_equation_message():
    message1 = "Tidak ada persamaan yang kamu masukkan"
    message2 = "kamu bisa menuliskan persamaan linearnya seperti contoh dibawah ini"
    message3 = "1. Variabel persamaan linear"
    message4 = "Kamu harus menuliskan persamaan linear seperti ini 2X1 + X2 - 3X3 = 4. variabelnya harus X, besar kecil tidak berpengaruh dan ada indeksnya"
    message5 = "2. Penulisan persamaan"
    message6 = "Penulisan persamaan bisa dipisahkan dengan koma seperti dibawah ini"
    message7 = "2X1 + X2 - 3X3 = 4, X1 - 2x2 + 4X3 = 5, ...,"
    message8 = "Atau dengan enter kebawah"
    message9 = "2X1 + X2 - 3X3 = 4"
    message10 = "X1 - 2x2 + 4X3 = 5"
    message11 = "..."
    message12 = "Sekarang tuliskan persamaan kamu:"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    arr.append(message5)
    arr.append(message6)
    arr.append(message7)
    arr.append(message8)
    arr.append(message9)
    arr.append(message10)
    arr.append(message11)
    arr.append(message12)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def not_valid_equation_message(base_count,base_vars,eq,current_vars):
    message1 = "Jumlah variabel tidak sama"
    message2 = f"Persamaan pertama memiliki {base_count} variabel: {base_vars}"
    message3 = f"Namun persamaan '{eq}' punya {len(current_vars)} variabel: {current_vars}"
    message4 = "Tuliskan persamaan linear kamu dengan benar"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def valid_equation_message(equations):
    message1 = "Persamaan valid"
    arr = []
    arr.append(message1)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr

def optimization_message():
    message1 = "Kamu memilih Optimasi. Masukkan Fungsi tujuan."
    message2 = "kamu bisa menuliskan persamaan fungsi tujuan seperti dibawah ini"
    message3 = "1. Variabel persamaan linear"
    message4 = "Kamu harus menuliskan fungsi tujuan seperti ini Z = 3X1 + 4X2 variabelnya harus X, besar kecil tidak berpengaruh dan ada indeksnya"
    message5 = "Sekarang tuliskan fungsi tujuan kamu:"
    arr = []
    arr.append(message1)
    arr.append(message2)
    arr.append(message3)
    arr.append(message4)
    arr.append(message5)
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return arr