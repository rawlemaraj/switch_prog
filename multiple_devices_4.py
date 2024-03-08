import re
from netmiko import ConnectHandler

# Define the devices to connect to
devices = [
    {
        'device_type': 'cisco_ios',
        'ip': 'SWITCH_IP_1',  # Replace with your first switch's IP address
        'username': 'USERNAME',  # Replace with your username
        'password': 'PASSWORD',  # Replace with your password
        'secret': 'SECRET',  # Replace with your enable secret, if required
    },
    # Add more device dictionaries as needed for each switch
]

# Define the command, statuses to look for, and the interface pattern
status_command = 'show interfaces status'
target_statuses = ['notconnect', 'down', 'disabled']
interface_pattern = r'\S*\/0\/\S+'  # Interface pattern variable

def get_down_ports(device, command, statuses, pattern):
    down_ports = []
    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(command, delay_factor=2)

            line_re = re.compile(rf'^({pattern})\s+.*\s+(' + '|'.join(statuses) + r')\s+', re.IGNORECASE)

            for line in output.splitlines():
                match = line_re.search(line)
                if match:
                    port = match.group(1)
                    down_ports.append(port)
    except Exception as e:
        print(f"An error occurred: {e}")

    return down_ports

# Path to the file where the output will be written
output_file = '/tmp/python_changes.txt'

# Iterate over each device and append the output to the file
for device in devices:
    down_ports = get_down_ports(device, status_command, target_statuses, interface_pattern)

    # Open the file in append mode and write the output
    with open(output_file, 'a') as file:
        file.write(f"Switch IP: {device['ip']}\n")
        if down_ports:
            file.write("Down Ports:\n")
            for port in down_ports:
                file.write(f"{port}\n")
        else:
            file.write("No down ports found.\n")
        file.write("\n")  # Add a newline for separation between switch outputs

print(f"Output appended to {output_file}")
