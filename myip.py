import http.server
import socketserver
import os
import requests
from pystyle import Write, Colors

# Define the request handler class
class MyIPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.css'):
            # Serve CSS files
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('static/css/styles.css', 'rb') as file:
                self.wfile.write(file.read())
        else:
            # Build the HTML response
            iprequest = requests.get("https://api.myip.com").json()
            ip = iprequest["ip"]
            country = iprequest["country"]
            cc = iprequest["cc"]

            html_response = f"""
                <html>
                <head>
                    <title>MyIP</title>
                    <link rel="stylesheet" type="text/css" href="/static/css/styles.css">
                </head>
                <body>
                    <h1>MyIP</h1>
                    <p>User: {os.getlogin()}</p>
                    <p>IP: {ip}</p>
                    <p>Country: {country}</p>
                    <p>Country Code: {cc}</p>
                </body>
                </html>
            """

            # Send the response headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Send the HTML response
            self.wfile.write(html_response.encode())

# Set up the server
PORT = 8000
Handler = MyIPHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

# Start the server
print(f"Server running on port {PORT}")
httpd.serve_forever()
