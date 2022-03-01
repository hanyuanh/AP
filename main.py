try:
  import usocket as socket
except:
  import socket

import network
import esp
esp.osdebug(None)
import gc
gc.collect()
# from datetime import datetime
import time
import _thread
# import threading
import select


# by default the AP ip of this board(Heltec WiFi LoRa V2) is 192.168.4.1
# tag_ip = '192.168.4.1'
# tag_port = 8088
# listening_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# listening_sock.bind((tag_ip, tag_port))
# sending_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
AP_SERVER_IP = '192.168.4.1'
AP_SERVER_PORT = 8088
TAG_SERVER_IP = '192.168.4.2'
TAG_SERVER_PORT = 8088
AP1 = 'MicroPython-AP1'
AP2 = 'MicroPython-AP2'

def ap_setup():
  ssid = AP1
  password = '123456789'

  ap = network.WLAN(network.AP_IF)
  ap.active(True)
  ap.config(essid=ssid, password=password)
  ap.config(authmode=3)

  while ap.active() == False:
    pass

  print('Connection successful')
  print(ap.ifconfig())

def run_server(AP_SERVER_IP, AP_SERVER_PORT):
  ping_time = -1
  pong_time = -1
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server.bind((AP_SERVER_IP, AP_SERVER_PORT))
  print("in run_server")
  while True:
    data, addr = server.recvfrom(1024)
    print('addr: {}'.format(addr))
    data_str = data.decode("utf-8").split('!')
    print("data_str: {}".format(data_str))
    if str(data_str[0]) == "FTMRequest":
      # send ping
      ping_time = time.ticks_us()
      # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      print("Trying to send to addr: {}".format(addr[0]))
      server.sendto(bytes("Ping", "utf-8"), (addr[0], TAG_SERVER_PORT))
      # client.close()
    elif str(data_str[0]) == "Pong":
      pong_time = time.ticks_us()
      msg = 'pingpongtime!'
      msg += str(pong_time-ping_time)
      print(msg)
      print('addr[0]: {}'.format(addr[0]))
      # client2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      server.sendto(bytes(msg, "utf-8"), (addr[0], TAG_SERVER_PORT))
      # client2.close()
    else:
      print("unknown error")

def run_server_tcp(AP_SERVER_IP, AP_SERVER_PORT):
  # https://github.com/micropython/micropython/blob/master/examples/network/http_server_simplistic_commented.py

  s = socket.socket()
  ai = socket.getaddrinfo(AP_SERVER_IP, AP_SERVER_PORT)
  print("Bind address info:", ai)
  addr = ai[0][-1]
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  s.bind(addr)
  s.listen(5)
  counter = 0
  while True:
      res = s.accept()
      client_s = res[0]
      client_addr = res[1]
      print("Client address:", client_addr)
      print("Client socket:", client_s)
      while True:
        req = client_s.recv(4096)
        print("Request:")
        print(req)
        client_s.send('TOA')
        # client_s.close()
        counter += 1
        print()
def main():
  ap_setup()  
  run_server_tcp('192.168.4.1', 8088)

main()
