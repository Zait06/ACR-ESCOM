import argparse
import http.client
REMOTE_SERVER_HOST = '127.0.0.1'
REMOTE_SERVER_PATH = '/'

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST,8080)
conn.request("GET", "/")

r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()  # This will return entire content.
conn.request("GET", "/")
r1 = conn.getresponse()
while True:
     chunk = r1.read(200)  # 200 bytes
     if not chunk:
          break
     print(repr(chunk))