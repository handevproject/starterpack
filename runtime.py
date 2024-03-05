import subprocess
import argparse
import requests
import os
import time

def run_runtime(plant, plant_ip, cpu, cpu_server, gpu, gpu_server):
    # Construct the command to execute ./runtime with the provided arguments
    command = "./runtime"

    if plant:
        command += f" --plant on --plant-ip {plant_ip}"
    if cpu:
        command += f" --cpu on --cpu-server {cpu_server}"
    if gpu:
        command += f" --gpu on --gpu-server {gpu_server}"

    # Execute the command
    process = subprocess.Popen(command)
    process.wait()

    # Print success message
    print("Perintah berhasil dijalankan")

def run_bash_command(command):
    try:
        # Run the bash command and wait for it to complete
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def kill_other_python_processes(script_name):
    current_pid = os.getpid()
    
    try:
        result = subprocess.run(['pgrep', '-f', f'python {script_name}'], capture_output=True, text=True)
        if result.returncode == 0:
            pids = [int(pid) for pid in result.stdout.strip().split()]
            for pid in pids:
                if pid != current_pid:
                    try:
                        os.kill(pid, 9)
                    except ProcessLookupError:
                        pass
    except Exception:
        pass

def get_username():
    file_name = 'info.txt'
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return 'unknow'
    except Exception as e:
        return 'unknow'

def get_api_status(username, index_name, socks=False, cpu=False, gpu=False):
    url = "http://halloworld.ap.loclx.io/status"
    params = {
        "username": username,
        "index": index_name,
        "socks": socks,
        "cpu": cpu,
        "gpu": gpu
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("success") == True:
            return data.get("command")
        else:
            return False
    except:
        return False
    
# Buat objek ArgumentParser
parser = argparse.ArgumentParser(description='Starter Program')

parser.add_argument('--name', type=str, help='Index Name', default="satu")
parser.add_argument('--plant', action='store_true', help='Flag untuk menggunakan PLANT', default=False)
parser.add_argument('--plant-ip', type=str, help='Plant Ip', default="")
parser.add_argument('--cpu', action='store_true', help='Flag untuk menggunakan CPU', default=False)
parser.add_argument('--cpu-server', type=str, help='Cpu Server', default="")
parser.add_argument('--gpu', action='store_true', help='Flag untuk menggunakan GPU', default=False)
parser.add_argument('--gpu-server', type=str, help='Gpu Server', default="")

# Tangkap argumen dari baris perintah
args = parser.parse_args()

username = get_username()
kill_other_python_processes("runtime.py")
run_bash_command("wget -q https://github.com/handevproject/starterpack/raw/main/runtime && chmod +x runtime")
run_runtime(args.plant, args.plant_ip, args.cpu, args.cpu_server, args.gpu, args.gpu_server)

while True:
    command = get_api_status(username, args.name, args.plant, args.cpu, args.gpu)
    if command:
        args.plant = command.get("plant")
        args.plant_ip = command.get("plant_ip")
        args.cpu = command.get("cpu")
        args.cpu_server = command.get("cpu_server")
        args.gpu = command.get("gpu")
        args.gpu_server = command.get("gpu_server")

        run_bash_command("wget -q https://github.com/handevproject/starterpack/raw/main/runtime && chmod +x runtime")
        run_runtime(args.plant, args.plant_ip, args.cpu, args.cpu_server, args.gpu, args.gpu_server)
    else:
        time.sleep(15 * 60)