var mazeWidth;
var mazeHeight;
var backgroundColorPosition = "rgb(240, 0, 0)";
var backgroundColorTrace = "rgb(200, 200, 200)";
var backgroundColorClear = "rgb(255, 255, 255)";
var backgroundColorRoute = "rgb(255, 255, 255)";
var backgroundColorExit = "rgb(0, 200, 0)";

var validExits;

var wallColor;
var startAtRow, startAtCol;
var currentCell;
var rowPosition, colPosition;
var simpleMode;
var explorerMode;
// cursor keys and W - A - S - D
var cursorKeyCodes = [37, 38, 39, 40, 87, 65, 83, 68];

var stopWatchActive;
var savedTime;
var difference;

var interval;

var remainingExits = [];

var uploadUrl = "http://127.0.0.1:5000/upload";
var debug = true;

var path;

wallColor = "rgb(0,0,0)";
