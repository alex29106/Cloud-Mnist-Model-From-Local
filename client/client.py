import socket
import pickle
import cv2
import numpy as np


class Connect():
    def __init__(self, ip, port, formats, size, failing_times=5):
        self.ADDR = (ip, port)
        self.formats = formats
        self.size = size
        self.failing_times = failing_times
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(self.ADDR)

    def send_array(self, array):
        """Send array in batches to the server"""
        data = pickle.dumps(array)
        for i in range(0, len(data), self.size):
            self.server.send(data[i:i + self.size])
            self.server.recv(self.size)


    def image_process(self, file_address):
        """Converting the image into an array of [784,1] so the model can process"""
        x = (255 - cv2.resize(cv2.imread(file_address, cv2.IMREAD_GRAYSCALE),
                              [28, 28])) / 256
        array = np.array(x).reshape(784, 1)
        return array

    def deliver(self, file_address):
        array = self.image_process(file_address=file_address)
        self.send_array(array=array)
        self.server.send('array_end'.encode(self.formats))
        res = self.server.recv(self.size).decode(self.formats)
        self.server.close()
        return res


if __name__ == '__main__':
    IP = input("Input server IP\n")
    # IP = socket.gethostbyname(socket.gethostname())
    # file_loc = input("Input image's address\n")
    file_loc = '../resourses/mnist_first_digit.png'

    # Change the IP and Port to match the server
    server = Connect(ip=IP,
                     port=5000,
                     size=1024,
                     formats="utf-8")
    res = server.deliver(file_address=file_loc)
    print(res)
