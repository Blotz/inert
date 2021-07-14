/*This code checks for cookies. probably */
function check_for_cookie() {
    var cookieArr = document.cookie.split(";");
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        if ('code' == cookiePair[0].trim()) {
            window.location.href = "https://temp-web.skunkwork.live/dashboard";
        }
    }
};
/*This code runs when user loads the website. it should check for cookies and redirect to /dashboard */
/*Replace this in check_for_cookie(); */
window.onload = function startup() {
   /* document.getElementById('token').innerHTML = document.cookie;*/
};

window.addEventListener("message", (event) => {
    /*This code triggers on successful auth*/
    check_for_cookie();
});
function login() {
    window.open(
        "https://discord.com/api/oauth2/authorize?client_id=853387310016102431&redirect_uri=https%3A%2F%2Ftemp-web.skunkwork.live%2Fapi&response_type=code&scope=identify%20guilds", 
        "_blank", 
        "width=500,height=777"
        );
};