import cgi
import http.cookies
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from urllib.parse import urlencode
import socketserver

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
      if self.path == '/':
          self.send_response(301)
          self.send_header('Location', '/mark.html?id=3')
          self.end_headers()
      params = {'lang':'en','tag':'python'}
      url_parts = list(urlparse.urlparse(self.path))
      query = dict(urlparse.parse_qsl(url_parts[4]))
      # query.update(params)
      path = url_parts[2]
      # print(url_parts[2])
      # print(query)
      # url_parts[4] = urlencode(query)
      #
      if len(query) == 0:
          pass
      else:
          print(query["id"])

      # print(url_parts[4])
      # print(urlparse.urlunparse(url_parts))


      if path == '/mark.html':
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes(PAGE, 'utf-8'))

      # self.path = "/index.html?id=14"

      # else:
      #     url_parts = list(urlparse.urlparse(self.path))
      #     query = dict(urlparse.parse_qsl(url_parts[4]))
      #     print(url_parts)
      #     print(query)
      #     if self.path == '/mark.html':
      #         self.send_response(200)
      #         self.send_header("Content-type", "text/html")
      #         self.end_headers()
      #         self.wfile.write(bytes(PAGE, 'utf-8'))
          # print(self.path)



      # print("I am here")
      # print(self.path)
      # url_parts = list(urlparse.urlparse(self.path))
      # query = dict(urlparse.parse_qsl(url_parts[4]))
      # print(query)


      # params = {'lang':'en','tag':'python'}
      # url_parts = list(urlparse.urlparse(self.path))
      # query = dict(urlparse.parse_qsl(url_parts[4]))
      # query.update(params)
      # print(query)
      # print(url_parts)
      # self.path = url_parts[2]
      # if self.path == '/':
      #     # self.path = '/index.html' + '?id=12'
      #     print("change path")
      #     self.send_response(301)
      #     self.send_header('Location','/index.html' + '?id=13')
      #     self.end_headers()

      # else:
      #     print("else")
      #     if self.path == '/index.html':
      #         self.send_response(200)
      #         self.send_header("Content-type", "text/html")
      #         global counter
      #         cookie = http.cookies.SimpleCookie()
      #         counter = counter + 1
      #         users.append(counter)
      #         cookie['user_id'] = str(counter)
      #
      #         self.send_header("Set-Cookie", cookie.output(header='', sep=''))
      #
      #         self.end_headers()
      #         self.wfile.write(bytes(PAGE, 'utf-8'))




    # do stuff...

  # def do_POST(self):
  #     print("ok")
  #     C = http.cookies.SimpleCookie(self.headers["Cookie"])
  #     print(C['user_id'].value)
  #    # Pretty much the same as do_READ()
  #    # call WriteCookie() or DoSomethingWithUploadedFile()...
  #    # other stuff....
  # def DoSomethingWithUploadedFile(self, groupId):
  #   ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
  #   query = cgi.parse_multipart(self.rfile, pdict)
  #   self.send_response(200)
  #   self.end_headers()
  #   fileContent = query.get('file')[0]
  #   # do something with fileContent
  #   self.wfile.write("POST OK.")
  #
  # def RedirectTo(self, url, timeout=0):
  #   self.wfile.write("""<html><head>
  #     <meta HTTP-EQUIV="REFRESH"
  #           content="%i; url=%s"/></head>""" % (timeout, url))
  #
  # def WriteCookie(self):
  #   # Shows how to read form values from a POST request
  #   # and write a cookie with a value from the form
  #   form = cgi.FieldStorage(headers=self.headers, fp=self.rfile,
  #   environ={'REQUEST_METHOD':'POST',
  #            'CONTENT_TYPE':self.headers['Content-Type']})
  #
  #   val = form.getfirst('myvalue', None)
  #   self.send_response(200)
  #   self.send_header('Content-type', 'text/html')
  #   if val:
  #     c = Cookie.SimpleCookie()
  #     c['value'] = val
  #     self.send_header('Set-Cookie', c.output(header=''))
  #     self.end_headers()
  #     self.RedirectTo(form.getfirst('follow', '/'))
  #   else:
  #     self.end_headers()
  #     self.wfile.write("No username ?".encode("utf-8"))
  #
  # def ReadCookie(self):
  #   if "Cookie" in self.headers:
  #     c = Cookie.SimpleCookie(self.headers["Cookie"])
  #     return c['value'].value
  #   return None

class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    try:
        server = StreamingServer(('', 8002), MainHandler)
        print ('Started httpserver on port ' , 8002)#
        server.serve_forever()
    finally:
        #camera.stop_recording()
        server.socket.close()

    # with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    #     output = StreamingOutput()
    #     camera.start_recording(output, format='mjpeg')
    #     try:
    #         server = StreamingServer(('', HTTP_PORT), StreamingHttpHandlerCamera)
    #         print ('Started httpserver on port ' , HTTP_PORT)#
    #         server.serve_forever()
    #     finally:
    #         print("Stopping")
    #         camera.stop_recording()
    #         server.socket.close()
    # try:
	# #Create a web server and define the handler to manage the
	# #incoming request
    #     http_server = HTTPServer(('', HTTP_PORT), StreamingHttpHandler)
    #     print ('Started httpserver on port ' , HTTP_PORT)#
    # # Wait forever for incoming htto requests
    #     http_server.serve_forever()
    # except KeyboardInterrupt:
	#     print ('^C received, shutting down the web server')
	#     http_server.socket.close()
#     http_thread = Thread(target=http_server.serve_forever)
#     address = ('', HTTP_PORT)
# server = StreamingHttpServer(address, StreamingHandler)
# server.serve_forever()
if __name__ == '__main__':
    main()
# def main():
#   try:
#     server = HTTPServer(('', int(8000)), MainHandler)
#     print ('started httpserver...')
#     server.serve_forever()
#   except KeyboardInterrupt:
#     print ('^C received, shutting down server')
#     server.socket.close()
#
# if __name__ == '__main__':
#   main()
