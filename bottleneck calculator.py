import os
import time
import psutil
import requests
import subprocess
import socket
import json

# Define an animation function
def loading_animation(seconds, message):
    for _ in range(seconds):
        print(f"{message}{'.' * _}{' ' * (seconds - _)}", end='\r')
        time.sleep(3)
    print(" " * (seconds + len(message)), end='\r')

def calculate_bottleneck(cpu_speed, gpu_speed):
    if cpu_speed >= gpu_speed:
        bottleneck_percentage = (gpu_speed / cpu_speed) * 100
        return bottleneck_percentage, "CPU is bottlenecking GPU"
    else:
        bottleneck_percentage = (cpu_speed / gpu_speed) * 100
        return bottleneck_percentage, "GPU is bottlenecking CPU"

def get_system_info():
    try:
        os_info = os.popen("systeminfo").read()

        # Detect CPU clock speed
        cpu_speed = psutil.cpu_freq().current

        # Detect GPU clock speed (NVIDIA-specific)
        try:
            nvidia_smi_output = subprocess.check_output(["nvidia-smi", "--query-gpu=clocks.gr", "--format=csv,noheader,nounits"], encoding="utf-8")
            gpu_speed = int(nvidia_smi_output.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            gpu_speed = 0  # Default to 0 if NVIDIA GPU or nvidia-smi is not available

        # Add a 3-second delay with animation
        loading_animation(3, "Detecting CPU and GPU Clock Speeds")

        # Detect network provider settings
        network_provider = get_isp_name()
        # Add a 3-second delay with animation
        loading_animation(3, "Detecting PC Information and Network Information")

        # Make an API request to get your public IPv4 address
        response = requests.get("https://ipinfo.io")
        ip_info = response.text

        return os_info, cpu_speed, gpu_speed, network_provider, ip_info
    except Exception as e:
        return str(e)

def get_isp_name():
    try:
        # Make an API request to get details about your IP address
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data.get("org", "Not Available")
    except Exception as e:
        return str(e)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    pc_info, cpu_speed, gpu_speed, network_provider, ip_info = get_system_info()

    print("PC Info:")
    print(pc_info)

    print("\nCPU Clock Speed (GHz):", cpu_speed)
    if gpu_speed > 0:
        print("GPU Clock Speed (MHz):", gpu_speed)
    else:
        print("GPU Clock Speed: Not Available")

    print("Network Provider:", network_provider)

    print("\nIPv4 Address:")
    print(ip_info)

    time.sleep(4)  # Add a 4-second delay

    bottleneck_percentage, message = calculate_bottleneck(cpu_speed, gpu_speed)

    print(f"\nBottleneck Percentage: {bottleneck_percentage:.2f}%")
    print(message)

    feedback = input("\nHave you been satisfied with our product? (Y/N): ").strip().lower()
    if feedback == 'y':
        print("Thank you for your feedback!")
    elif feedback == 'n':
        print("We appreciate your feedback and will strive to improve our product.")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the display
        print("Go away")

    print("\nContact the Developer for any help!:")
    print("Email: apostoloff420@proton.me")

if __name__ == "__main__":
    main()