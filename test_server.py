import http.server
import socketserver
import os

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/static/index.html'
        return super().do_GET()

os.chdir('/Users/alejandromarianamunoz/Desktop/Curso Agentes IA/agents/sourcing-evaluator')
handler = MyHTTPRequestHandler
with socketserver.TCPServer(("", 8001), handler) as httpd:
    print("Server running at http://localhost:8001")
    httpd.serve_forever()
