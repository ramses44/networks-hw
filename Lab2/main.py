import click
import subprocess
import platform

IEIA_PATH = '/proc/sys/net/ipv4/icmp_echo_ignore_all'


def execute_command(command: str) -> subprocess.CompletedProcess:
     return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)


def ping(host: str, package: int) -> bool:
    match platform.system():
        case "Windows":
            command = f"ping -n 1 -M do -s {package} {host}"
        case "Linux":
            command = f"ping -c 1 -M do -s {package} {host}"
        case "Darwin":
            command = f"ping -c 1 -D -s {package} {host}"
        case _:
              return False
         
    res = execute_command(command)
    return res.returncode == 0


def is_host_available(host: str) -> bool:
        res = execute_command(f"ping -{'n' if platform.system() == 'Windows' else 'c'} 1 {host}" )
        return res.returncode == 0


def is_icmp_enabled() -> bool:
        if platform.system() == "Linux":
            res = execute_command("cat " + IEIA_PATH)
            return res.returncode == 0 and int(res.stdout) == 0
        
        return True


def find_mtu(host: str, max_mtu: int) -> int:
        l = -1
        r = max_mtu + 1

        while r - l > 1:
            m = (l + r) // 2

            if ping(host, m):
                l = m
            else:
                r = m

        return l


@click.command()
@click.option("--host", required=True, help="Host address")
@click.option('--max-mtu', type=click.INT, default=2**16, help="Max MTU value for search")
def main(host, max_mtu):
    if not is_host_available(host):
        print("Host is not available!")
        exit(1)
    
    if not is_icmp_enabled():
        print("ICMP is not enabled!")
        exit(1)

    mtu = find_mtu(host, max_mtu)

    if mtu < 0:
        print("Host is not available!")
        exit(1)
    
    print("MTU:", mtu)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
         print("Unexpected error occured:", err)