import http.server
import socketserver
import os
import requests

class MyIPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('styles.css', 'rb') as file:
                self.wfile.write(file.read())
        else:
            client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])

            iprequest = requests.get("https://api.myip.com").json()
            ip = iprequest["ip"]
            country = iprequest["country"]
            cc = iprequest["cc"]

            html_response = f"""
                <html>
                <head>
                    <title>Client IP Address</title>
                    <link rel="stylesheet" type="text/css" href="styles.css">
                </head>
                <body>
                    <h1>Client IP Address</h1>
                    <div id="ip-container">
                        <p id="ip-address">{client_ip}</p>
                        <p>Country: {country}</p>
                        <p>Country Code: {cc}</p>
                    </div>
                </body>
                </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_response.encode())

PORT = 8000
Handler = MyIPHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Server running on port {PORT}")
httpd.serve_forever()
