import subprocess
import re


def get_ip_from_ping(host):
    try:
        # Выполняем команду ping
        result = subprocess.run(['ping', host, '-n', '1'], capture_output=True, text=True)
        output = result.stdout

        # Ищем IP-адрес в выводе команды ping
        ip_match = re.search(r'\[(.*?)\]', output)
        if ip_match:
            return ip_match.group(1)

        # Альтернативный метод поиска IP-адреса, если вывод не содержит скобок
        ip_match = re.search(r'PING .*? \[(.*?)\]', output) or re.search(r'PING .*? \((.*?)\)', output)
        if ip_match:
            return ip_match.group(1)

    except Exception as e:
        print(f"Ошибка при выполнении команды ping для {host}: {e}")
    return None


def get_mac_address(ip):
    try:
        # Выполняем команду nbtstat -A {ip}
        result = subprocess.run(['nbtstat', '-A', ip], capture_output=True, text=True, encoding='cp866')
        output = result.stdout

        # Ищем строку с MAC-адресом
        for line in output.split('\n'):
            if 'MAC Address' in line or 'Адрес платы (MAC)' in line or 'Ї« вл (MAC)' in line:
                return line.split('=')[-1].strip()
    except Exception as e:
        print(f"Ошибка при выполнении команды nbtstat для {ip}: {e}")
    return None


def main():
    hosts_file = 'hosts.txt'
    output_file = 'mac_addresses.txt'

    with open(hosts_file, 'r') as file:
        hosts = file.readlines()

    with open(output_file, 'w') as file:
        for host in hosts:
            host = host.strip()
            if host:
                ip = get_ip_from_ping(host)
                if ip:
                    print(f"IP-адрес для {host}: {ip}")
                    mac_address = get_mac_address(ip)
                    if mac_address:
                        file.write(f"{host} ({ip}): {mac_address}\n")
                        print(f"{host} ({ip}): {mac_address}")
                    else:
                        file.write(f"{host} ({ip}): MAC-адрес не найден\n")
                        print(f"MAC-адрес для {ip} не найден")
                else:
                    print(f"IP-адрес для {host} не найден")


if __name__ == "__main__":
    main()
