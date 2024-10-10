import Run
import socket
import threading
import pickle


class Host:
    def __init__(self, ip, port, formats, size, failing_times=5):
        self.ADDR = (ip, port)
        self.formats = formats
        self.size = size
        self.failing_times = failing_times
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def main(self):
        self.server.bind(self.ADDR)
        self.server.listen()
        print("Server is listening...")
        while True:
            conn, addr = self.server.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            thread = threading.Thread(target=self.handle_stream, args=(conn,))
            thread.start()

    def handle_stream(self, conn):
        try:
            data = b''
            while True:
                chunk = conn.recv(self.size)
                if chunk.decode(self.formats, errors='ignore') != 'array_end':
                    data += chunk
                    conn.send('True'.encode(self.formats))
                else:
                    break
            array = pickle.loads(data)
            res = Run.main(array)
            conn.send(str(res).encode(self.formats))
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())
    host = Host(ip=IP, port=5000, formats="utf-8", size=1024)
    host.main()
