function getmymsg(cmd, param) {
  var arrret = [];
  var arrpres = [];
  var rawhtml = "";
  var eurl = "";
  try {
    eurl = "https://exoman.herokuapp.com/kakaocmd" + cmd + "/" + param.replace(" ", "%20");
    rawhtml = org.jsoup.Jsoup.connect(eurl).get();
    arrpres = rawhtml.select("pre");
    arrret.push(arrpres);
  }  catch (e) {
  arrret.push("서버와 연결할 수 없읍니다.");
  arrret.push(e);
}
 finally   {
    return arrret;
  }
}
function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) {
  var cmd = msg.split(" ")[0];
  var param = msg.toString().replace(cmd, "").trim();
  var mymsg=[];
  if (param === undefined) {
    param = "none"
    ;}
  if (cmd.startsWith("/")) {
    mymsg = getmymsg(cmd, param);
    if (Object.keys(mymsg).length> 0) {
      mymsg.forEach(e => replier.reply(e.toString().replace(/<[^>]+>/g,"").trim()));
    }
  }
}
