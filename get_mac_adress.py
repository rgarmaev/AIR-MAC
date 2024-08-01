import subprocess


def get_mac_address(ip):
    try:
        # Выполняем команду nbtstat -A {ip}
        result = subprocess.run(['nbtstat', '-A', ip], capture_output=True, text=True, encoding='cp866')
        output = result.stdout

        # Добавляем отладочный вывод
        print(f"Вывод команды для {ip}:\n{output}\n")

        # Ищем строку с MAC-адресом
        for line in output.split('\n'):
            if 'MAC Address' in line or 'Адрес платы (MAC)' in line or 'Ї« вл (MAC)' in line:
                return line.split('=')[-1].strip()
    except Exception as e:
        print(f"Ошибка при выполнении команды для {ip}: {e}")
    return None


def main():
    ip_file = 'ips.txt'
    output_file = 'mac_addresses.txt'

    with open(ip_file, 'r') as file:
        ips = file.readlines()

    with open(output_file, 'w') as file:
        for ip in ips:
            ip = ip.strip()
            if ip:
                mac_address = get_mac_address(ip)
                if mac_address:
                    file.write(f"{ip}: {mac_address}\n")
                    print(f"{ip}: {mac_address}")
                else:
                    print(f"MAC-адрес для {ip} не найден")


if __name__ == "__main__":
    main()
