import http.server
import socketserver

# Define the port for the proxy server to listen on
PORT = 8080

# Read filtered sites information from the file
def read_filtered_sites():
    filtered_sites = []
    with open("filtered_sites.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                filtered_sites.append(line)
    return filtered_sites

# Check if a URL matches any of the filtered sites
def is_filtered(url, filtered_sites):
    for filtered_site in filtered_sites:
        if filtered_site.startswith("*"):
            if url.endswith(filtered_site[1:]):
                return True
        else:
            if url == filtered_site:
                return True
    return False

# Custom request handler to handle incoming HTTP requests
class ProxyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        filtered_sites = read_filtered_sites()
        destination_url = self.path[1:]  # Remove the leading '/'
        if is_filtered(destination_url, filtered_sites):
            # URL is filtered, send a filtering error response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Filtering Error</h1></body></html>")
        else:
            # URL is not filtered, forward the request to the destination server
            self.proxy_request()

    def proxy_request(self):
        # Implement the logic to forward the request to the destination server here
        # You can use libraries like `requests` or low-level socket programming to establish a connection
        pass

# Create the proxy server and set the request handler
with socketserver.ThreadingTCPServer(("", PORT), ProxyRequestHandler) as server:
    print("Proxy server running on port", PORT)
    server.serve_forever()
