from netmiko import ConnectHandler

def read_file(file_path):
    """Reads lines from a file and returns them as a list."""
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def apply_config_to_switch(switch_identifier, commands):
    """Connects to a switch and applies configuration commands."""
    device = {
        'device_type': 'cisco_ios',  # Assuming Cisco IOS devices
        'host': switch_identifier,  # 'host' can be an IP address or an FQDN
        'username': 'your_username',  # Update with your switch's username
        'password': 'your_password',  # Update with your switch's password
        'secret': 'your_secret',  # Update with your switch's secret, if any
    }

    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()  # Entering enable mode
            output = net_connect.send_config_set(commands)
            print(f"Applied config to {switch_ip} successfully.")
            print(output)  # Printing output for verification
    except Exception as e:
        print(f"Failed to apply config to {switch_ip}. Error: {e}")

def main(config_file, switches_file):
    config_commands = read_file(config_file)
    switch_ips = read_file(switches_file)

    for ip in switch_ips:
        apply_config_to_switch(ip, config_commands)

if __name__ == "__main__":
    config_file_path = 'path_to_your_config_file.txt'  # Update this path
    switches_file_path = 'path_to_your_switches_file.txt'  # Update this path
    main(config_file_path, switches_file_path)
