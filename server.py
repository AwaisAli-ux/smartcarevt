import http.server
import socketserver
import os

PORT = 8000

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Strip query parameters if any
        url_path = self.path.split('?')[0].rstrip('/')
        
        # If url_path without leading slash + .html exists, rewrite
        if url_path:
            clean_name = url_path.lstrip('/')
            potential_file = clean_name + '.html'
            if os.path.isfile(potential_file):
                # Preserve query string
                query = ('?' + self.path.split('?')[1]) if '?' in self.path else ''
                self.path = '/' + potential_file + query
                
        return super().do_GET()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving clean URLs on port {PORT}...")
        httpd.serve_forever()
