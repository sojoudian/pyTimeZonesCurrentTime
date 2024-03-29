import http.server
import json
from datetime import datetime, timezone, timedelta

class TimeAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response status code
        self.send_response(200)
        # Set response headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Get current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        utcTime = datetime.utcnow()
        torontoTime = utcTime - timedelta(hours=5)

        # Prepare response data
        time_zones = {
            'UTC': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            'Toronto': torontoTime.strftime('%Y-%m-%d %H:%M:%S'),
            # Add more time zones as needed
            # 'EST': datetime.now(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S'),
            # 'PST': datetime.now(timezone(timedelta(hours=-8))).strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Convert data to JSON with each city in a separate line
        response_data = ""
        for city, time in time_zones.items():
            response_data += f'"{city}": "{time}",\n'

        # Remove the trailing comma and newline character from the last line
        response_data = response_data.rstrip(",\n")

        # Add enclosing braces
        response_data = "{" + response_data + "}"

        # Send JSON response
        self.wfile.write(response_data.encode('utf-8'))

def run(server_class=http.server.HTTPServer, handler_class=TimeAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
