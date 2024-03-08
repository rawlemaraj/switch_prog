import re
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

# Load device IPs from the YAML file
with open('devices.yaml', 'r') as file:
    devices_list = yaml.safe_load(file)

# Define the statuses to look for and the interface pattern
target_statuses = ['notconnect', 'down', 'disabled']
interface_pattern = r'\S*\/0\/\S+'  # Adjust this pattern as needed
command_to_run = 'shutdown'  # The command to run on the matched ports

def process_device(ip):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'YOUR_USERNAME',
        'password': 'YOUR_PASSWORD',
        'secret': 'YOUR_SECRET',
    }

    down_ports = []
    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command('show interfaces status', delay_factor=2)
            line_re = re.compile(rf'^({interface_pattern})\s+.*\s+(' + '|'.join(target_statuses) + r')\s+', re.IGNORECASE)

            for line in output.splitlines():
                match = line_re.search(line)
                if match:
                    port = match.group(1)
                    down_ports.append(port)
                    
            # Run command on down ports
            for port in down_ports:
                config_commands = [
                    f'interface {port}',
                    command_to_run
                ]
                net_connect.send_config_set(config_commands)
                print(f"{ip}: Command '{command_to_run}' executed on {port}")
                
    except Exception as e:
        print(f"{ip}: An error occurred: {e}")

# Using ThreadPoolExecutor to process devices in parallel
with ThreadPoolExecutor(max_workers=len(devices_list['my_list'])) as executor:
    executor.map(process_device, devices_list['my_list'])
