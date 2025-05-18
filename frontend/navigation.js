document.onkeydown = function(event) {

    switch (event.keyCode) {
        // esc key to display settings overlay
        case 27:

            toggleSettings();
            break;

        // enter key revelas maze and starts stop watch
        case 13:
            document.getElementById("maze").style.visibility = "visible";
            stopWatchActive = true;
            startTime = new Date().getTime();
            interval = setInterval(startStopWatch, 1); // 1: millisecond
            break;

        // i k j l keys to change width / height u o for both, width and height
        case 73:
        case 74:
        case 75:
        case 76:
        case 79:
        case 85:

            changeDimensions(event.keyCode);

            break;
        // r key re-creates maze and hides it
        case 82:
            if (r_reload) {
                location.reload();
            }
            initMaze();
            break;

        case 37:
        case 65:

            paintTrace("left");
            break;

        case 38:
        case 87:

            paintTrace("top");
            break;

        case 39:
        case 68:

            paintTrace("right");
            break;

        case 40:
        case 83:

            paintTrace("bottom");
            break;

    }


    if (cursorKeyCodes.includes(event.keyCode)) {

        if (stopWatchActive == false && rowPosition != mazeHeight && colPosition != mazeWidth) {

            stopWatchActive = true;
            startTime = new Date().getTime();
            interval = setInterval(startStopWatch, 1); // 1: millisecond

        } else {

            if (rowPosition == mazeHeight && colPosition == mazeWidth) {

                stopWatchActive = false;
                stopStopWatch();
                showResults();
                uploadPath();

            }

        }

    }

};


function paintTrace(direction) {

    var lastCell = document.getElementById("cell_" + rowPosition + "_" + colPosition);
    lastCell.style.backgroundColor = backgroundColorTrace;

    switch (direction) {

        case "right":

            if (currentCell.style.borderRight != "") {
                colPosition++;
                path += "r"
            }

            break;

        case "left":

            if (currentCell.style.borderLeft != "") {
                colPosition--;
                path += "l"
            }
            break;

        case "top":

            if (currentCell.style.borderTop != "") {
                rowPosition--;
                path += "t"
            }

            break;

        case "bottom":

            if (currentCell.style.borderBottom != "") {
                rowPosition++;
                path += "b"
            }
            break;

    }

    currentCell = document.getElementById("cell_" + rowPosition + "_" + colPosition);
    currentCell.style.backgroundColor = backgroundColorPosition;

    if (explorerMode == true) {
        revealNeighbourWalls(rowPosition, colPosition);
    }
}

function toggleSettings() {
    if (document.getElementById("controller_container").style.display == "") {
        document.getElementById("controller_container").style.display = "block";

    } else {
        document.getElementById("controller_container").style.display = "";
    }


}

function hideResults() {
    document.getElementById("results_container").style.visibility = "hidden";
}

function showResults() {
    console.log("show results");
    document.getElementById("results_container").style.visibility = "visible";
    var time = document.getElementById("stopwatch").innerHTML;

    document.getElementById("timeResults").innerHTML = time;
    if (path !== optimalPath) {
        document.getElementById("isOptimal").innerHTML = "not ";
    }
}

function revealNeighbourWalls(rowPosition, colPosition) {
    // first row
    if (rowPosition - 1 == 0) {
        // first col
        if (colPosition - 1 == 0) {

            // right cell
            removeInvisibleWallClass(rowPosition, colPosition + 1);
            // bottom-right cell
            removeInvisibleWallClass(rowPosition + 1, colPosition + 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        // last col
        } else if (colPosition + 1 > mazeWidth) {
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);
            // bottom-left cell
            removeInvisibleWallClass(rowPosition + 1, colPosition - 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        // middle col
        } else {
            console.log("middle");
            // left cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);
            // bottom-left cell
            removeInvisibleWallClass(rowPosition + 1, colPosition - 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);
            // bottom-right cell
            removeInvisibleWallClass(rowPosition + 1, colPosition + 1);
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition);
        }

    // last row
    } else if (rowPosition + 1 > mazeHeight)  {
        // first col
        if (colPosition - 1 == 0) {
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // top-right cell
            removeInvisibleWallClass(rowPosition - 1, colPosition + 1);
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition + 1);
            // bottom-right cell
            removeInvisibleWallClass(rowPosition + 1, colPosition + 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        // last col
        } else if (colPosition + 1 > mazeWidth) {
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // top-left cell
            removeInvisibleWallClass(rowPosition - 1, colPosition - 1);
            // left cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);

        // middle col
        } else {
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // top-right cell
            removeInvisibleWallClass(rowPosition - 1, colPosition + 1);
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition + 1);
            // top-left cell
            removeInvisibleWallClass(rowPosition - 1, colPosition - 1);
            // left cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);
        }

    // middle row
    } else {
        // first col
        if (colPosition - 1 == 0) {
            console.log("first");
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // top-right cell
            removeInvisibleWallClass(rowPosition - 1, colPosition + 1);
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition + 1);
            // bottom-right cell
            removeInvisibleWallClass(rowPosition + 1, colPosition + 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        // last col
        } else if (colPosition + 1 > mazeWidth) {
            console.log("last");
            // top-left cell
            removeInvisibleWallClass(rowPosition - 1, colPosition - 1);
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // left cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);
            // bottom-left cell
            removeInvisibleWallClass(rowPosition + 1, colPosition - 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        // middle col
        } else {
            // top cell
            removeInvisibleWallClass(rowPosition - 1, colPosition);
            // top-right cell
            removeInvisibleWallClass(rowPosition - 1, colPosition + 1);
            // right cell
            removeInvisibleWallClass(rowPosition, colPosition + 1);
            // bottom-right cell
            removeInvisibleWallClass(rowPosition + 1, colPosition + 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);
            // top-left cell
            removeInvisibleWallClass(rowPosition - 1, colPosition - 1);
            // left cell
            removeInvisibleWallClass(rowPosition, colPosition - 1);
            // bottom-left cell
            removeInvisibleWallClass(rowPosition + 1, colPosition - 1);
            // bottom cell
            removeInvisibleWallClass(rowPosition + 1, colPosition);

        }
    }
}

function removeInvisibleWallClass(rowPosition, colPosition) {
    neighbourCell = document.getElementById("cell_" + (rowPosition) + "_" + (colPosition));
    neighbourCell.classList.remove("invisibleWall");
}

function uploadPath() {
    if (!uploadUrl) {
        return
    }

    const without_path = document.getElementById("mazeDataJson").value;
    let data = without_path.slice(0, -1) + ', "path": "' + path + '"}'

    fetch(uploadUrl, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/json'
        },
        body: data
    }).then(data => console.log(data)).catch(err => console.log(err));
}
