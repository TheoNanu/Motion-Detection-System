#define RXD2 16
#define TXD2 17

#define ARR_LEN  1000
#define MAX_LEN 1000

int epsilon = 5;

unsigned int distanceLeftFiltered = 0;
unsigned int distanceRightFiltered = 0;

unsigned int prevDistanceRight = 0;
unsigned int prevDistanceLeft = 0;

//int differenceArray[ARR_LEN];
//unsigned int rightSensorValuesFiltered[ARR_LEN];
//unsigned int leftSensorValuesFiltered[ARR_LEN];

int* differenceArray;
unsigned int* rightSensorValuesFiltered;
unsigned int* leftSensorValuesFiltered;

int counterLeft = 0;
int counterRight = 0;

bool movement = false;
bool prevMovement = false;

bool leftMovement = false;
bool rightMovement = false;

int networkType = 0;
String state = "";

int inside = 0;
int outside = 0;
int total = 0;

int counter = 0;

bool fixed = false;
bool fixedLeft = false;
bool fixedRight = false;

const char* username = "admin";
const char* pass = "ciocolataculapte23";

bool isLogged = false;

unsigned int flag;
bool datasetWritingEnabled = false;

String formattedDate;
String currentYear;
String currentMonth;
String currentDay;

String dataFromFile = "";

String valuesReceived = "";
unsigned int received = 0;

String header = "";

float leftIndexFeature = 0;
float activLeftFeature = 0;
float deactivLeftFeature = 0;
float rightIndexFeature = 0;
float activRightFeature = 0;
float deactivRightFeature = 0;
float meanLeftFeature = 0;
float meanRightFeature = 0;
