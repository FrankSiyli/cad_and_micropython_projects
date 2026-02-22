
# The MIT License (MIT)
#
# Copyright (c) Sharil Tumin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-----------------------------------------------------------------------------

# site.py MVC - This is the model M of MVC

from uos import urandom as ran
from machine import Pin
from help import Setting as cam
from help import help

class auth: pass

server=''
client=''

def pwd(size=8):
    alfa = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join([alfa[x] for x in [(ran(1)[0] % len(alfa)) for _ in range(size)]])

# These will be set by server script as site.ip and site.camera
ip=''
camera=None

hdr = {
    "stream": """HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame
Connection: keep-alive
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: Thu, Jan 01 1970 00:00:00 GMT
Pragma: no-cache""",
    # live stream -
    # URL:
    "frame": """--frame
Content-Type: image/jpeg""",
}

app={}
def route(p):
    def w(g):
        app[p]=g
    return w

      

@route('/')
def live(cs,v): # live stream
    cs.write(b'%s\r\n\r\n' % hdr['stream'])
    cs.setblocking(True)
    pic=camera.capture
    put=cs.write
    hr=hdr['frame']
    while True:
       try:
          put(b'%s\r\n\r\n' % hr)
          put(pic())
          put(b'\r\n')  # send and flush the send buffer
       except Exception as e:
          print(e)
          break
   
        
        
        
        




