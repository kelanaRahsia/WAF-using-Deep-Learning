import http.server
import socketserver
import requests
import mysql.connector
import urllib.parse
import datetime

# MySQL configuration
db_config = {
    'host' : 'localhost',
    'port' : '3306',
    'user' : 'root',
    'password' : '',
    'database' : 'psm_waf'
}

# HTTP proxy configuration
class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Get the URL from the user's request
        user_url = self.path[0:]  # Remove the leading slash
        test_url = self.path[1:]
        print("user_url: ",user_url)

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Request Time (24-hour format):", formatted_time)

        # http_method = self.command  # Get the HTTP method (GET, POST, etc.)
        http_method = "GET"
        print(f"HTTP Method: {http_method}")

        headers = dict(self.headers)
        headers['Host'] = urllib.parse.urlparse(user_url).netloc
        destination = headers['Host']
        
        source_ip, source_port = self.client_address
        source = (f"{source_ip}:{source_port}")
    
        # Parse the URL to extract parameters
        parsed_url = urllib.parse.urlparse(user_url)
        query_parameters = urllib.parse.parse_qs(parsed_url.query)
        print("parsed_url:",parsed_url)
        print("query_parameters:",query_parameters)

        user_input = "-"
        input_length = "0"
        # Access and print parameters
        for key, value in query_parameters.items():
            user_input = value[0]
            input_length = len(user_input)
            # Store the URL in the MySQL database
            self.store_url(source, destination, user_url, http_method, user_input, input_length, formatted_time)

        # Forward the request to the user's URL destination
        self.forward_request(user_url)

    def do_POST(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Request Time (24-hour format):", formatted_time)

        # Get the content length from headers
        content_length = int(self.headers['Content-Length'])
        print("content_length: ", content_length)

        # Get the POST data
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        print("post_data: ", post_data)
        print("parsed_data: ", parsed_data)
        for key, value in parsed_data.items():
            print("values:", value)
            print("param name :", key)
            user_input = value[0]
            print("user_input :", user_input)
            input_length = len(user_input)
            print("input_length:", input_length)

        source = self.client_address


        # http_method = self.command  # Get the HTTP method (GET, POST, etc.)
        http_method = "POST"
        print(f"HTTP Method: {http_method}")

        # Extract the URL from POST data
        user_url = self.path[0:]
        print("user_url: ",user_url)

        headers = dict(self.headers)
        headers['Host'] = urllib.parse.urlparse(user_url).netloc
        destination = headers['Host']

        source_ip, source_port = self.client_address
        source = (f"{source_ip}:{source_port}")

        # Store the URL in the MySQL database
        self.store_url(source, destination, user_url, http_method, user_input, input_length, formatted_time)

        # Forward the POST request to the user's URL destination
        self.forward_request(user_url, method='POST', data=post_data.encode('utf-8'))

        # return email_value,email_length 

    def store_url(self, source, destination, url, method,user_input, input_length, timedate):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            insert_query = "INSERT INTO request_logs (source, destination, url, method,user_input, input_length, timedate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (source, destination, url, method,user_input, input_length, timedate))
            connection.commit()

            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")

    def forward_request(self, url, method='GET', data=None):
        try:
            headers = dict(self.headers)

            headers['Host'] = urllib.parse.urlparse(url).netloc
            
            response = requests.request(method, url, headers=headers, data=data)

            self.send_response(response.status_code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.content)
        except requests.RequestException as err:
            print("error :", err)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error accessing URL")

# Set up the proxy server
PORT = 8085
Handler = ProxyHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Proxy server listening on port", PORT)
    httpd.serve_forever()
