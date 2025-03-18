try:
    import usocket as socket
except:
    import socket


from time import sleep


def web_page(tank_volume: float = 0.0, tank_percentage: float = 0.0):

    with open("index.html") as f:
        html = f.read()

    html = html.replace("TANK_VOLUME", str(tank_volume))
    html = html.replace("TANK_PERCENT", str(tank_percentage))

    return html


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("", 80))
    except OSError as e:
        print(e)
        return

    print("Server is running on port 80...")
    s.listen(5)

    tank_volume = 0
    try:
        while True:
            conn, addr = s.accept()
            print("Got a connection from %s" % str(addr))
            request = conn.recv(1024)
            request = str(request)
            response = web_page(tank_volume=tank_volume, tank_percentage=tank_volume / 10)
            conn.send("HTTP/1.1 200 OK\n")
            conn.send("Content-Type: text/html\n")
            conn.send("Connection: close\n\n")
            conn.sendall(response)
            conn.close()
            sleep(0.5)
            tank_volume += 25
    except OSError as e:
        print(e)

    finally:
        s.close()


if __name__ == "__main__":
    main()
