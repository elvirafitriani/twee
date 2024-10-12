import requests
import time

# Fungsi untuk memeriksa ketersediaan email di Twitter tanpa menggunakan proxy
def check_email_availability(email, password):
    url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if not result['valid']:  # Memeriksa apakah email tidak valid
                return f"{email}:{password} - Valid: {result['valid']}, Msg: {result['msg']}"
        return "valid"  # Mengembalikan "valid" jika email tersedia
    except requests.exceptions.RequestException as e:
        print(f"Error saat memeriksa {email}: {e}")
        return None

# Membaca email:password dari file
def load_credentials(file_path):
    credentials = []
    with open(file_path, 'r') as file:
        for line in file:
            email, password = line.strip().split(':')
            credentials.append((email, password))
    return credentials

# File yang berisi daftar email:password
file_path = 'emaillist.txt'

# Muat daftar email:password dan batasi hanya 150 email
credentials = load_credentials(file_path)[:150]

# Mengumpulkan hasil untuk email tidak valid
invalid_results = []
valid_count = 0
for index, (email, password) in enumerate(credentials, start=1):
    result = check_email_availability(email, password)
    if result == "valid":
        valid_count += 1
    elif result is not None:
        invalid_results.append(result)
    
    # Tampilkan progres ke konsol
    print(f"Memeriksa email ke-{index}: {email}")
    
    # Setiap 50 email, berikan jeda 5 detik
    if index % 50 == 0:
        print("Jeda 5 detik untuk setiap 50 email...")
        time.sleep(5)
        print("Lanjutkan pengecekan...")

# Setelah semua 150 email diperiksa, simpan hasil ke file
file_name = "AKUN_AVAILABLE_CHECK.txt"
with open(file_name, 'w') as f:
    for result in invalid_results:
        f.write(result + "\n")

# Tampilkan pesan setelah semua email dicek
total_invalid = len(invalid_results)
print(f"Pengecekan selesai untuk 150 email.")
print(f"Total email valid: {valid_count}")
print(f"Total email tidak valid: {total_invalid}")
print(f"Hasil disimpan dalam '{file_name}'")
