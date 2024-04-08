import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# PostgreSQL connection details
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')

# SQL query to check if the current node is the master
SQL_QUERY = "SELECT pg_is_in_recovery()"

class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('/')[-1]
        if path == '/is_master':
            try:
                # Connect to PostgreSQL
                conn = psycopg2.connect(
                    host=POSTGRES_HOST,
                    user=POSTGRES_USER,
                    password=POSTGRES_PASSWORD,
                    database=POSTGRES_DB
                )
                cursor = conn.cursor()

                # Execute the SQL query
                cursor.execute(SQL_QUERY)
                is_in_recovery = cursor.fetchone()[0]

                # Check if the node is the master
                if not is_in_recovery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(bytes("This node is the master", "utf-8"))
                else:
                    self.send_response(503)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(bytes("This node is not the master", "utf-8"))

                cursor.close()
                conn.close()
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes(f"Error: {str(e)}", "utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Not Found", "utf-8"))

def run():
    server_address = ('', 8080)  # Serve on port 8080
    httpd = HTTPServer(server_address, HealthCheckServer)
    print('Health check server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

