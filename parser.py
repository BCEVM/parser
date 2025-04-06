import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import os
import time

init(autoreset=True)

def is_valid_url_format(line):
    parts = line.split(":")
    return len(parts) >= 3 and parts[0].startswith("http")

def check_url_status(line):
    parts = line.split(":")
    url = parts[0].strip()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[✅] Aktif : {url} | {parts[1]} | {parts[2]}")
            return line
        else:
            print(f"{Fore.RED}[❌] Tidak Aktif : {url}")
    except requests.RequestException:
        print(f"{Fore.RED}[❌] Tidak Aktif : {url}")
    return None

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + "Tools ini dikembangkan oleh bcevm - Hacktivist Indonesia\n")

    input_file = input("Masukkan nama file log (.txt): ")
    output_file = input("Masukkan nama file output hasil: ")

    if not os.path.exists(input_file):
        print(Fore.RED + "File tidak ditemukan!")
        return

    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if is_valid_url_format(line)]

    print(f"\nMemproses {len(lines)} baris valid...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_url_status, lines))

    results = [r for r in results if r is not None]

    with open(output_file, "w") as f:
        for r in results:
            f.write(r + "\n")

    print(f"\n{Fore.GREEN}Selesai! {len(results)} URL aktif disimpan ke {output_file}")
    print(f"Waktu eksekusi: {round(time.time() - start_time, 2)} detik")

if __name__ == "__main__":
    main()
