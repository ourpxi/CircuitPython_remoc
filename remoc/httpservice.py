from . import globals
from .logger import log
from dispatcher import reset_token, handlejson
from adafruit_httpserver import Server, Request, Response # type: ignore
import wifi # type: ignore
import json

def connect_wifi(ssid, password):
    try:
        wifi.radio.connect(ssid, password)
        log("INFO", f"Conectado a Wi-Fi: {ssid}")
    except Exception as e:
        log("ERROR", f"Error al conectar a Wi-Fi '{ssid}': {e}")

def start_http_server():
    try:
        # Create HTTP server
        server = Server(wifi.radio, port=80)
        log("INFO", "HTTP server created")
        
        @server.route("/token", "GET")
        def handle_get(request: Request):
            try:
                # Reset token and get new one
                token = reset_token()
                log("DEBUG", f"Token reset, sending to client: {token}")
                
                # Return token as JSON
                response_data = {"token": token}
                return Response(
                    request,
                    json.dumps(response_data),
                    content_type="application/json"
                )
            except Exception as e:
                log("ERROR", f"Error handling GET request: {e}")
                error_response = {"error": str(e)}
                return Response(
                    request,
                    json.dumps(error_response),
                    content_type="application/json",
                    status=500
                )
        
        @server.route("/", "POST")
        def handle_post(request: Request):
            try:
                # Get JSON data from request body
                json_data = request.json
                log("DEBUG", f"Received POST data: {json_data}")
                
                # Call handlejson with the received data
                result = handlejson(json.dumps(json_data))
                log("DEBUG", f"Handler returned: {result}")
                
                # Return the result back to client
                return Response(
                    request,
                    result,
                    content_type="application/json"
                )
            except Exception as e:
                log("ERROR", f"Error handling POST request: {e}")
                error_response = {"error": str(e)}
                return Response(
                    request,
                    json.dumps(error_response),
                    content_type="application/json",
                    status=500
                )
        
        # Start the server
        server.serve_forever()
        log("INFO", f"HTTP server started on {wifi.radio.ipv4_address}")
        
    except Exception as e:
        log("ERROR", f"Error starting HTTP server: {e}")