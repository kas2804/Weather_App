from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

API_KEY = "4476f8b0a242a4811af4247e081d8b88"

class WeatherHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        if self.path == '/weather':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                city = data.get('city', '')
                
                if not city:
                    self.wfile.write(json.dumps({"error": "City name is required"}).encode())
                    return
                
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                weather_data = response.json()
                
                if response.status_code == 200:
                    response_data = {
                        "City": weather_data['name'],
                        "Temperature": weather_data['main']['temp'],
                        "Description": weather_data['weather'][0]['description'],
                        "Humidity": weather_data['main']['humidity'],
                        "WindSpeed": weather_data['wind']['speed']
                    }
                    self.wfile.write(json.dumps(response_data).encode())
                else:
                    error_msg = weather_data.get('message', 'Failed to fetch weather data')
                    self.wfile.write(json.dumps({"error": error_msg}).encode())
                    
            except json.JSONDecodeError:
                self.wfile.write(json.dumps({"error": "Invalid JSON data"}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

if __name__ == '__main__':
    port = 8080
    server_address = ('localhost', port)  # Changed to localhost for security
    httpd = HTTPServer(server_address, WeatherHandler)
    print(f"Server running on http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()