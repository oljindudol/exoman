function getmymsg(cmd, param) {
    var arrret = [];
    var arrpres = [];
    var rawhtml = "";
    try {
        rawhtml = org.jsoup.Jsoup.connect("https://exoman.herokuapp.com/kakaocmd" + cmd + "/" + param.replace(" ", "%20")).get();
        arrpres = html.select("pre");
        arrret = arrpres

    } catch (e) {
        arrret.push("서버와 연결할 수 없읍니다.");
        nally {
            return arrret;
        }
    }
};


function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) {
    var cmd = msg.split(" ")[0];
    var param = msg.replace(cmd + " ", "");
    var mymsg = "";
    if (cmd.startsWith("/")) {
        mymsg = getmymsg(cmd, param);
        if (mymsg.length() > 0) {
            mymsg.forEach(e => replier.reply(e));
        }
}