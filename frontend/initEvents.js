function initEvents() {


    addEventListener('input', function (e) {

        if (e.target.classList.contains("settings") == true) {

            exportMaze();
        }

    });
    //
    // document.getElementById("importMazeData").onclick = function(e) {
    //
    //     importMaze();
    //
    // }

    document.getElementById("showSettings").onclick = function(e) {

        toggleSettings();

        e.preventDefault();
    }

    document.getElementById("importMazeData").onclick = function() {

        var mazeDataJson = document.getElementById("mazeDataJson").value;
        try {
            importMaze(mazeDataJson);
        }
        catch (SyntaxError) {
            alert("Not a maze:\n" + document.getElementById("mazeDataJson").value)
            document.getElementById("mazeDataJson").value = ""
        }
    }

}
