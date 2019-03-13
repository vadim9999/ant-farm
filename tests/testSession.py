from http.cookies import SimpleCookie as cookie
import cgi
import http.cookies
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid
import time
import urllib.parse as urlparse
from urllib.parse import urlencode

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
 <form action="handler.php" method="post">
  <p><input type="text" name="str"></p>
  <p><input type="submit" value="Отправить"></p>
 </form>
</body>
</html>
"""

class ApplicationRequestHandler(BaseHTTPRequestHandler):


    def _session_cookie(self,forcenew=False):
     cookiestring = "\n".join(self.headers.get_all('Cookie',failobj=[]))
     c = cookie()
     c.load(cookiestring)

     # try:
     #  if forcenew or self.sessioncookies[c['session_id'].value]-time() > 3600:
     #      raise ValueError('new cookie needed')
     # except:
     c['session_id']="2232"

     for m in c:
      if m=='session_id':
       self.sessioncookies[c[m].value] = 243
       c[m]["httponly"] = True
       c[m]["max-age"] = 3600
       c[m]["expires"] = 244
       self.sessionidmorsel = c[m]
       break

    sessioncookies = {}
    def do_GET(self):
        params = {'lang':'en','tag':'python'}
        url_parts = list(urlparse.urlparse(self.path))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        # print(query)
        print(url_parts[2])
        self.path = url_parts[2]
        # query = urlparse(self.path).query
        # print(query)
        url_parts[4] = urlencode(query)
        # print(urlparse.urlunparse(url_parts))

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self._session_cookie(self)
            # global counter
            # cookie = http.cookies.SimpleCookie()
            # counter = counter + 1
            # users.append(counter)
            # cookie['user_id'] = str(counter)
            #
            # self.send_header("Set-Cookie", cookie.output(header='', sep=''))

            self.end_headers()
            self.wfile.write(bytes(PAGE, 'utf-8'))








def main():
  try:
    server = HTTPServer(('', int(8000)), ApplicationRequestHandler)
    print ('started httpserver...')
    server.serve_forever()
  except KeyboardInterrupt:
    print ('^C received, shutting down server')
    server.socket.close()

if __name__ == '__main__':
  main()
