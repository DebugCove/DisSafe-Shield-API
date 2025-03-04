import netifaces


def get_ip_machine():
    interfaces = netifaces.interfaces()
    IPS = []
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            IP = addresses[netifaces.AF_INET][0]['addr']
            IPS.append(IP)

    return IPS
