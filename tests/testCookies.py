import cgi
import http.cookies
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

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
users = []
counter = 0
class MainHandler(BaseHTTPRequestHandler):
  def do_GET(self):
      print("I am here")
      params = {'lang':'en','tag':'python'}
      url_parts = list(urlparse.urlparse(self.path))
      query = dict(urlparse.parse_qsl(url_parts[4]))
      query.update(params)
      # print(query)
      print(url_parts)
      self.path = url_parts[2]

      if self.path == '/index.html':
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          global counter
          cookie = http.cookies.SimpleCookie()
          counter = counter + 1
          users.append(counter)
          cookie['user_id'] = str(counter)

          self.send_header("Set-Cookie", cookie.output(header='', sep=''))

          self.end_headers()
          self.wfile.write(bytes(PAGE, 'utf-8'))



    # do stuff...

  def do_POST(self):
      print("ok")
      C = http.cookies.SimpleCookie(self.headers["Cookie"])
      print(C['user_id'].value)
     # Pretty much the same as do_READ()
     # call WriteCookie() or DoSomethingWithUploadedFile()...
     # other stuff....
  def DoSomethingWithUploadedFile(self, groupId):
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    query = cgi.parse_multipart(self.rfile, pdict)
    self.send_response(200)
    self.end_headers()
    fileContent = query.get('file')[0]
    # do something with fileContent
    self.wfile.write("POST OK.")

  def RedirectTo(self, url, timeout=0):
    self.wfile.write("""<html><head>
      <meta HTTP-EQUIV="REFRESH"
            content="%i; url=%s"/></head>""" % (timeout, url))

  def WriteCookie(self):
    # Shows how to read form values from a POST request
    # and write a cookie with a value from the form
    form = cgi.FieldStorage(headers=self.headers, fp=self.rfile,
    environ={'REQUEST_METHOD':'POST',
             'CONTENT_TYPE':self.headers['Content-Type']})

    val = form.getfirst('myvalue', None)
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    if val:
      c = Cookie.SimpleCookie()
      c['value'] = val
      self.send_header('Set-Cookie', c.output(header=''))
      self.end_headers()
      self.RedirectTo(form.getfirst('follow', '/'))
    else:
      self.end_headers()
      self.wfile.write("No username ?".encode("utf-8"))

  def ReadCookie(self):
    if "Cookie" in self.headers:
      c = Cookie.SimpleCookie(self.headers["Cookie"])
      return c['value'].value
    return None

def main():
  try:
    server = HTTPServer(('', int(8000)), MainHandler)
    print ('started httpserver...')
    server.serve_forever()
  except KeyboardInterrupt:
    print ('^C received, shutting down server')
    server.socket.close()

if __name__ == '__main__':
  main()
