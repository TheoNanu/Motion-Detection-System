#include "WiFi.h"
#include "SPIFFS.h"
#include "ESPAsyncWebServer.h"
#include "NTPClient.h"
#include "WiFiUdp.h"
#include "param.h"
#include "initWebServer.h"
#include <SimpleTimer.h>
#include <ArduinoJson.h>

extern "C"{
  #include "Neural Nets\output\ESP_NN.c"
};

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

SimpleTimer timer;
 
void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len){
 
  if(type == WS_EVT_CONNECT){
    Serial.println("Websocket client connection received");
    globalClient = client;
  } else if(type == WS_EVT_DISCONNECT){
    Serial.println("Websocket client connection finished");
    globalClient = NULL;
  }
  else if(type == WS_EVT_DATA){
    Serial.print("Data received: ");
    for(int i = 0; i < len; i++)
      Serial.print((char)data[i]);

    Serial.println();
    processMessage(data, len);
  }
}
 
void setup(){
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
 
  if(!SPIFFS.begin()){
     Serial.println("An Error has occurred while mounting SPIFFS");
     return;
  }

  initWebServer();
  ws.onEvent(onWsEvent);
  server.begin();

  header = "PeakLeft,ActivationLeft,DeactivationLeft,PeakRight,ActivationRight,DeactivationRight,MeanLeft,MeanRight";

  writeHeaderIfFileEmpty("/features.csv", header);

  timeClient.begin();
  timeClient.setTimeOffset(10800);

  timer.setInterval(86400000, writeInLogFile);

  leftSensorValuesFiltered = (unsigned int*) malloc(1 * sizeof(unsigned int));
  rightSensorValuesFiltered = (unsigned int*) malloc(1 * sizeof(unsigned int));
}


void loop(){
   while(!timeClient.update()){
      timeClient.forceUpdate();
   }
   
   formattedDate = currentYear + "," + currentMonth + "," + currentDay;
   
   String date = timeClient.getFormattedDate();
   //Serial.println(date);

   currentYear = date.substring(0, 4);
   currentMonth = date.substring(5, 7);
   currentDay = date.substring(8, 10);
   
   timer.run();

    while(Serial2.available() > 0){
      received = flag;
      flag = (unsigned int)Serial2.read();
    }
   
   // due to sensors interfering problems, read one sensor in one iteration and the second one the next iteration
   if(flag == 0)
   {
    // read the value
    distanceLeftFiltered = received;
   }
   else
   {
    // read the value
    distanceRightFiltered = received;
   }

//  Serial.print(distanceLeftFiltered);
//  Serial.print(",");
//  Serial.print(distanceRightFiltered);
//  Serial.println(",");

//    Serial.println("Reference left " + String(prevDistanceLeft));
//    Serial.println("Reference right " + String(prevDistanceRight));

  // the logic for detecting if there is something moving in front of the sensors
  if(prevDistanceRight !=0 && prevDistanceLeft != 0)  // if the sensors were initialized and they are functioning check if there is motion
  {
    leftMovement = ((int)distanceLeftFiltered < (int)prevDistanceLeft - epsilon);
    rightMovement = ((int)distanceRightFiltered < (int)prevDistanceRight - epsilon);
    if(leftMovement || rightMovement) // if there is a change in the value read, then motion
    {
        movement = true;
        state = "movement";
    }
    else   // if there is no change in the value read for any of the sensors
    {
        movement = false;
        state = "no movement";
    }
  }
    
  if(movement == true)  // if we are in the movement state
  {
    // if there is movement put values in arrays
    if(putValueInArrayAtIndex(1, distanceRightFiltered, counterRight) == true)
      counterRight++;
    if(putValueInArrayAtIndex(0, distanceLeftFiltered, counterLeft) == true)
      counterLeft++;

    state = "movement";
  }
  
  if(movement == false && prevMovement == true)
  {
    state = "right after the movement";
    counter += 1;
    // put one more value in the arrays in order to get the deactivation index for the sensor which deactivated last
    if(putValueInArrayAtIndex(1, distanceRightFiltered, counterRight) == true)
      counterRight++;
    if(putValueInArrayAtIndex(0, distanceLeftFiltered, counterLeft) == true)
      counterLeft++;
      
    //printLeftArray();
    //printRightArray();
    
    int rightIndex = indexOfMinElem(rightSensorValuesFiltered, counterRight);
    int leftIndex = indexOfMinElem(leftSensorValuesFiltered, counterLeft);

    int offset = abs(rightIndex - leftIndex);

    differenceArray = (int*) malloc(counterLeft  * sizeof(int));
    
    for(int i = 0; i < counterLeft; i++)
    {
      differenceArray[i] = (int)(rightSensorValuesFiltered[i] - leftSensorValuesFiltered[i]);
    }

    int activRight = getActivationIndex(rightSensorValuesFiltered, prevDistanceRight, counterRight);
    int activLeft = getActivationIndex(leftSensorValuesFiltered, prevDistanceLeft, counterLeft);
    int deactivRight = getDeactivationIndex(rightSensorValuesFiltered, prevDistanceRight, counterRight);
    int deactivLeft = getDeactivationIndex(leftSensorValuesFiltered, prevDistanceLeft, counterLeft);

    int len = counterLeft;

    int firstHalfDifference[len/2];
    int secondHalfDifference[len - (len / 2)];

    int j = 0;
    //Serial.println("Values in the first half of the difference:");
    for(int i = 0; i < len/2; i++)
    {
      firstHalfDifference[i] = differenceArray[j];
      j++;
      //Serial.print(String(firstHalfDifference[i]) + " ");
    }

    //Serial.println("Values in the second half of the difference:");
    for(int i = 0; i < len - (len / 2); i++)
    {
      secondHalfDifference[i] = differenceArray[j];
      j++;
      //Serial.print(String(secondHalfDifference[i]) + " ");
    }

    //Serial.println();

    float meanRight = meanValueArray(firstHalfDifference, len/2);
    float meanLeft = meanValueArray(secondHalfDifference, len - (len /2));

    int lenLeft = counterLeft;
    int lenRight = counterRight;

    float maxVal = abs(meanLeft) > abs(meanRight) ? meanLeft : meanRight;

    if(!lenLeft)
    {
      leftIndexFeature = 0;
      activLeftFeature = 0;
      deactivLeftFeature = 0;
    }
    else
    {
      leftIndexFeature = (float)leftIndex / lenLeft;
      activLeftFeature = (float)activLeft / lenLeft;
      deactivLeftFeature = (float)deactivLeft / lenLeft;
    }

    if(!lenRight)
    {
      rightIndexFeature = 0;
      activRightFeature = 0;
      deactivRightFeature = 0;
    }
    else
    {
      rightIndexFeature = (float)rightIndex / lenRight;
      activRightFeature = (float)activRight / lenRight;
      deactivRightFeature = (float)deactivRight / lenRight;
    }

    if(!maxVal)
    {
      meanLeftFeature = 0;
      meanRightFeature = 0;
    }
    else
    {
      meanLeftFeature = meanLeft / maxVal;
      meanRightFeature = meanRight / maxVal;
    }

    String features = String(leftIndexFeature) + "," + String(activLeftFeature) + "," + String(deactivLeftFeature) + "," + 
                      String(rightIndexFeature) + "," + String(activRightFeature) + "," + String(deactivRightFeature) + "," + 
                      String(meanLeftFeature) + "," + String(meanRightFeature);

    if(datasetWritingEnabled)
    {
      writeHeaderIfFileEmpty("/features.csv", header);
      writeStringInFile("/features.csv", features);
    }

    const float input[8] = {leftIndexFeature, activLeftFeature, deactivLeftFeature, rightIndexFeature, 
                            activRightFeature, deactivRightFeature, meanLeftFeature, meanRightFeature};
    
//    Serial.println("Inputs: " + String(input[0]) + " " + String(input[1]) + " "  + String(input[2]) + " " + String(input[3]) + " " + String(input[4]) + " " + String(input[5])
//                  + " " + String(input[6]) + " " + String(input[7]));
    
    float output[1] = {-1};
    int out = -1;

    ESP_NN(input, output);

    if(output[0] > 0.7)
    {
      out = 1;
//    Serial.println("Miscare din dreapta");
    }
    else
    {
      out = 0;
//    Serial.println("Miscare din stanga");
    }

    if(out == 1)
    {
      inside += 1;
      total += 1;
    }
    else if(out == 0)
    {
      outside += 1;
      total += 1;
    }
    else
    {
        Serial.println("There was a problem running the algorithm.");
    }

    if(globalClient != NULL)
    {
      String message = "l" + String(total) + "," + String(inside) + "," + String(outside);
      globalClient->text(message);
    }

//    Serial.println("Freeing memory...");
    
    free(leftSensorValuesFiltered);
    free(rightSensorValuesFiltered);
    free(differenceArray);

//    Serial.println("Freeing memory...");
    leftSensorValuesFiltered = (unsigned int*) malloc(1 * sizeof(unsigned int));
    rightSensorValuesFiltered = (unsigned int*) malloc(1 * sizeof(unsigned int));
    
    counterLeft = 0;
    counterRight = 0;
  }
  
  prevMovement = movement;
   
//  Serial.println(state);
//  Serial.println("Counter: " + String(counter));

  // get reference value in the first iterations when reads get to a stable value
  if(!flag)
  {
    if(prevDistanceLeft == distanceLeftFiltered && distanceLeftFiltered != 0)
      fixedLeft = true;
  }
  else
  {
    if(prevDistanceRight == distanceRightFiltered && distanceRightFiltered != 0)
      fixedRight = true;
  }
  
  if(!(fixedRight && fixedLeft))
  {
    prevDistanceRight = distanceRightFiltered;
    prevDistanceLeft = distanceLeftFiltered;
  }
  
  delay(10);
}

void processMessage(uint8_t *msg, size_t len) {
  switch((char)msg[0])
  {
    case 'c':  // server received user credentials
    {
      String str = "";
      String toCompare = username;
      for(int i = 1; i < len; i++)
      {
        if((char)msg[i] == ';')
        {
          if(str != toCompare)
          {
              isLogged = false;
              break;
          }
          else
          {
              str = "";
              toCompare = pass;
              isLogged = true;
              continue;
          }
        }
        str += (char)msg[i];
      }
      break;
    }
    
    case 'l': // client logged out
    {
      Serial.println("Client logged out");
      isLogged = false;
      if(globalClient != NULL)
      {
        String message = "p" + String(isLogged);
        globalClient->text(message);
      }
      break;
    }
    
    case 'r':  // client requested data from the log file
    {
      readFromLogFile();
      if(globalClient != NULL)
      {
        if(dataFromFile != "")
        {
            Serial.print(dataFromFile);
            String message = "d" + dataFromFile + " ";
            globalClient->text(message);
            dataFromFile = "";
        }
        else
        {
            Serial.print("Did not read anything from the file.");
        }
      }
      else
      {
        Serial.print("The client is not connected.");
      }
      break;
    }
    
    case 'u': // client requested info about the state of the user
    {
      if(globalClient != NULL)
      {
        String message = "p" + String(isLogged);
        globalClient->text(message);
      }
      break;
    }
    
    case 'i': // client requested data related to a specific day
    {
      Serial.println("Recived req. from calendar");
      String recvDate = "";

      for(int i = 1; i < len; i++)
      {
        recvDate += (char)msg[i];
      }

      Serial.println("Received date: " + recvDate);

      File logfile = SPIFFS.open("/log.txt", FILE_READ);

      if(!logfile)
      {
        Serial.println("Error while opening the file");
        return;
      }

      String line = "";
      bool found = false;

      while(logfile.available())
      {
        char c = (char)logfile.read();
        if(c != '\n')
        {
          line += c;
        }
        else
        {
          int index = 0;
          for(int i = 0; i < 3; i++)
          {
            index = line.indexOf(',', index + 1);
          }
          String dateInFile = line.substring(0, index);
          String pers = line.substring(index + 1);

          int strEqual = dateInFile.compareTo(recvDate);

          Serial.println(dateInFile.length());
          Serial.println(recvDate.length());
          

          Serial.println("Date read from file: " + dateInFile + " .Date received: " + recvDate + " .They are different: " + String(strEqual));

          if(dateInFile.compareTo(recvDate) == 0)
          {
            Serial.println("It's a match!");
            found = true;
            if(globalClient != NULL)
            {
              globalClient->text("i" + pers);
              break;
            }
          }
          else
          {
            line = "";
          }
        }
      }
      logfile.close();
      if(found == false)
      {
        globalClient->text("iThere is no info for the selected day.");
      }
      break;
    }

    case 'e':
    {
      datasetWritingEnabled = !datasetWritingEnabled;
      break;
    }

    case 'w':
    {
      if(globalClient != NULL)
      {
        globalClient->text("w" + String(datasetWritingEnabled));
      }
      break;
    }
   
    case 'a':
    {
      if((char)msg[1] == '0')
        networkType = 0;
      else if((char)msg[1] == '1')
        networkType = 1;
      else if((char)msg[1] == '2')
        networkType = 2;
      break;
    }

    case 'v':
    {
      if(globalClient != NULL)
      {
        String message = "l" + String(total) + "," + String(inside) + "," + String(outside);
        globalClient->text(message);
      }
      break;
    }

    case 'f':
    {
      if(SPIFFS.remove("/features.csv") == true)
      {
        Serial.println("File was removed.");
        writeHeaderIfFileEmpty("/features.csv", header);
      }
    }
  }
}

void writeHeaderIfFileEmpty(String filePath, String header)
{
  bool empty = false;

  File file;

  if(SPIFFS.exists(filePath) == false)
  {
    Serial.println("Creating the file...");
    file = SPIFFS.open(filePath, FILE_WRITE);
    
    if (!file) 
    {
      Serial.println("There was an error opening the file for writing");
      return;
    }
    file.close();
  }

  file = SPIFFS.open(filePath, FILE_READ);

  if(!file){
    Serial.println("There was an error opening the file.");
    return;
  }

  if(file.available() == 0){
      Serial.println("The file is empty");
      empty = true; 
  }

  file.close();

  if(empty == true)
  {
    writeStringInFile(filePath, header);
  }
}

void initArray(unsigned int *arr)
{
  for(int i = 0; i < ARR_LEN; i++)
  {
    arr[i] = 9999;
  }
}

bool putValueInArrayAtIndex(int arr, unsigned int value, int index)
{
  if(arr == 1)
  {
    rightSensorValuesFiltered = (unsigned int*) realloc(rightSensorValuesFiltered, (index + 1) * sizeof(unsigned int));
  
    if(rightSensorValuesFiltered == NULL)
      return false;
  
    rightSensorValuesFiltered[index] = value;
  
    return true;
  }
  else
  {
    leftSensorValuesFiltered = (unsigned int*) realloc(leftSensorValuesFiltered, (index + 1) * sizeof(unsigned int));
  
    if(leftSensorValuesFiltered == NULL)
      return false;
  
    leftSensorValuesFiltered[index] = value;
  
    return true;
  }
}

int indexOfMinElem(unsigned int *arr, int len)
{
  int min_elem = 9999;
  int index = 0;
  for(int i = 0; i < len; i++)
  {
    if(arr[i] < min_elem)
    {
      index = i;
      min_elem = arr[i];
    }
  }
  return index;
}

int getActivationIndex(unsigned int *arr, int value, int len)
{
  for(int i = 0; i < len; i++)
  {
    if(arr[i] < value - epsilon)
      return i;
  }

  return -1;
}

int getDeactivationIndex(unsigned int *arr, int value, int len)
{
  int ind = 0;
  bool afterPeak = false;


  for(int i = 0; i < len; i++)
  {
    if((arr[i] >= value - epsilon) && (arr[i] <= value + epsilon) && afterPeak == true)
      return i;
    if(arr[i] < value - epsilon)
      afterPeak = true;
  }
  return -1;
}

int lenDifferenceArray()
{
  int len = 0;

  while(differenceArray[len] != 0)
  {
    len++;
  }

  return len;
}

float meanValueArray(int *arr, int len)
{
  //Serial.println("Computing the mean value...");
  if(len == 0)
    return 0;
  else
  {
    int sum = 0;
    for(int i = 0; i < len; i++)
    {
      sum += arr[i];
    }

    return (float)sum / len;
  }
}

void writeInLogFile(){
  File logfile = SPIFFS.open("/log.txt", FILE_APPEND);

   if(!logfile){
    Serial.println("There was an error opening the file.");
    return;
   }

   if(logfile.print(formattedDate + "," + String(total) + "," + String(inside) + "," + String(outside) + '\n')){
    Serial.println("File was written");
   }
   else{
    Serial.println("File write failed");
   }

   logfile.close();

   inside = 0;
   outside = 0;
   total = 0;
}

void readFromLogFile(){
  File logfile = SPIFFS.open("/log.txt", FILE_READ);

  if(!logfile){
    Serial.println("There was an error opening the file.");
    return;
  }

  while(logfile.available()){
    dataFromFile += (char)logfile.read();
    //Serial.write(logfile.read());
  }

  logfile.close();
}

void writeStringInFile(String filename, String str)
{
   File file = SPIFFS.open(filename, FILE_APPEND);

   if(!file){
    Serial.println("There was an error opening the file.");
    return;
   }

   if(file.print(String(str) + '\n')){
//    Serial.println("Wrote in features file.");
   }
   else{
    Serial.println("File write failed");
   }

   //logfile.println();

   file.close();
}

bool isArrayFull(unsigned int* arr, int len)
{
  if(arr[len - 1] == 9999)
  {
    return false;
  }
  else
  {
    return true;
  }
}
