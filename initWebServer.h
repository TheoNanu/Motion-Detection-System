const char* ssid = "Reee";
const char* password = "teonanu300898";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");
 
AsyncWebSocketClient * globalClient = NULL;

void initWebServer() {
    WiFi.begin(ssid, password);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi..");
    }
 
    Serial.println(WiFi.localIP());
    
    server.addHandler(&ws);
    
    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
        request->send(SPIFFS, "/config.html", "text/html");
    });

//    server.on("/log", HTTP_GET, [](AsyncWebServerRequest *request){
//        request->send(SPIFFS, "/log.txt", "text/plain");
//    });

    server.on("/config", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/config.html", "text/html");
    });

    server.on("/config.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/config.css", "text/css");
    });

    server.on("/login", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/login.html", "text/html");
    });

    server.on("/util.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/util.css", "text/css");
    });

    server.on("/main.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/main.css", "text/css");
    });

    server.on("/table", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/table.html", "text/html");
    });

    server.on("/table.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/table.css", "text/css");
    });

    server.on("/table.js", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/table.js", "text/javascript");
    });

    server.on("/calendar", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/calendar.html", "text/html");
    });

    server.on("/calendar.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/calendar.css", "text/css");
    });

    server.on("/calendar.js", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/calendar.js", "text/javascript");
    });

    server.on("/hella-wall.jpg", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/hella-wall.jpg", "image/jpg");
    });

    server.on("/login.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/login.png", "image/png");
    });

    server.on("/logout.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/logout.png", "image/png");
    });

    server.on("/submit.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/submit.png", "image/png");
    });

    server.on("/down-arrow.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/down-arrow.png", "image/png");
    });

    server.on("/show.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/show.png", "image/png");
    });

    server.on("/ac-logo.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/ac-logo.png", "image/png");
    });

    server.on("/upt-logo.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/upt-logo.png", "image/png");
    });

    server.on("/calendar.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/calendar.png", "image/png");
    });

    server.on("/file.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/file.png", "image/png");
    });

    server.on("/rec.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/rec.png", "image/png");
    });

    server.on("/home.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/home.png", "image/png");
    });

    server.on("/settings.png", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/settings.png", "image/png");
    });

    server.on("/algorithm", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/algorithm.html", "text/html");
    });

    server.on("/algorithm.css", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/algorithm.css", "text/css");
    });

    server.on("/algorithm.js", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, "/algorithm.js", "text/javascript");
    });

    server.on("/download-features", HTTP_GET, [](AsyncWebServerRequest *request) {
        AsyncWebServerResponse *response = request->beginResponse(SPIFFS, "/features.csv", String(), true);
        response->addHeader("Server", "ESP Async Web Server");
        request->send(response);
    });

   server.on("/delete", HTTP_GET, [](AsyncWebServerRequest * request) {
    if(SPIFFS.remove("/features.csv") == true)
      Serial.println("File was removed.");
      
    request->send(SPIFFS, "/config.html", "text/html");
  });
    

    server.on(
        "/post",
        HTTP_POST,
        [](AsyncWebServerRequest * request){request->send(SPIFFS, "/login.html", "text/html");},
        NULL,
        [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {
    });

    server.on("/download", HTTP_GET, [](AsyncWebServerRequest *request) {
        AsyncWebServerResponse *response = request->beginResponse(SPIFFS, "/log.txt", String(), true);
        response->addHeader("Server", "ESP Async Web Server");
        request->send(response);
    });
}
