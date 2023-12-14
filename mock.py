# mock_server.py
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/app/status':
            self.handle_app_status()
        else:
            self.send_error(404, "File Not Found: %s" % self.path)
    
    def do_POST(self):
        if self.path == '/app/replicas':
            self.handle_post_app_status()
        else:
            self.send_error(404, "File Not Found: %s" % self.path)
    
    def handle_post_app_status(self):
        # Read the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Read the incoming data
        post_data = self.rfile.read(content_length)

        # You can process the data here if needed
        print("Received POST request with data:", post_data.decode())

        # Send a simple response
        self.send_response(200)
        self.end_headers()
        response = bytes("POST request to /app/status received", "utf-8")
        self.wfile.write(response)

    def handle_app_status(self):
        mock_data = {
            "cpu": {
                "highPriority": 0.68
            },
            "replicas": 10
        }

        # Convert your mock data to JSON
        mock_response = json.dumps(mock_data).encode()

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(mock_response)


if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MockServer)
    print("Mock Server running on port 8000...")
    httpd.serve_forever()
