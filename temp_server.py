
import http.server
import socketserver
PORT = 5501
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print('Serving at: http://localhost:' + str(PORT))
    print('Serving on LAN: http://192.168.0.214:' + str(PORT))
    httpd.serve_forever()
