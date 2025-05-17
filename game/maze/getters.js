function getDemoMode() {

    demoMode = document.getElementById("demoMode").checked;

    if (demoMode == false) {

        document.getElementById("notice").innerHTML = "Please wait";
        hideResults();

    } else {

        document.getElementById("maze").style.visibility = "visible";
        stopStopWatch();

    }

}
