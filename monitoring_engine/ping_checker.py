from ping3 import ping


def check_ping(ip):

    delay = ping(ip, timeout=1)

    if delay is None:
        return "DOWN", None

    else:
        latency = delay * 1000
        return "UP", latency


if __name__ == "__main__":

    ip = "8.8.8.8"

    status, latency = check_ping(ip)

    print("Status:", status)
    print("Latency:", latency)