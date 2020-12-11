import http.client
conn = http.client.HTTPConnection("localhost:5000")
conn.request("GET", "/lights/living_room_led")