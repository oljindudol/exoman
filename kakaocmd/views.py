from django.db.models import Q
from django.shortcuts import render
from .models import Bschedule
from datetime import datetime
from datetime import timedelta

# Create your views here.


mslist = []
cmdlist = ["일정", "ㅇㅈ", "일정등록", "ㅇㅈㄷㄹ", "일정삭제", "ㅇㅈㅅㅈ"]
shortweeklist = ["월", "화", "수", "목", "금", "토", "일"]
longweeklist = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
bsslist = ["루윌", "하루윌", "스데", "스데미", "하스데", "듄더", "진듄더", "검마", "검멘"]

# main함수
def home(request, cmd, cmdpram):
    global mslist
    mslist = []

    # 대응 커맨드인가 확인한다
    if cmd not in cmdlist:
        mslist.append("Not a command")
        return render(request, "home.html", {"mslist": mslist})

    # 일정등록
    if cmd in ["일정등록", "ㅇㅈㄷㄹ"]:
        createschedule(cmdpram)
        selectschedule("none")

    # 일정삭제
    if cmd in ["일정삭제", "ㅇㅈㅅㅈ"]:
        deleteschedule(cmdpram)
        selectschedule("none")

    # 일정조회
    if cmd in ["일정", "ㅇㅈ"]:
        selectschedule(cmdpram)

    return render(request, "home.html", {"mslist": mslist})


# 일정등록
def createschedule(strparam):
    global mslist
    objtoday = datetime.now()
    # 날짜 필드 설정용 'yyyy-mm-dd'
    strfulldate = ""
    # 요일 필드 설정용 ex)'월'
    strday = ""
    # 시간 필드 설정용 hh:mm (24시간제)
    strtime = ""
    # 보스 필드 설정용 ex)하루윌
    strbss = ""
    # 보스 참가자1~6 설정용
    stratendee = []

    tempcmd = strparam.split(" ")

    # 인수 최소4개인것 확인
    # 3개 이하 일경우 에러메세지 등록후 끝
    if hasEnoughParam(4, len(tempcmd)) == False:
        mslist.append(
            "ex1)일정등록 07/18 01:30 하스데 모밀\nex2)일정등록 07/18 01:00 하루윌 가람 보곰 요정\nex3)ㅇㅈㄷㄹ 목 하루윌 조아 요정"
        )
        return 0

    ##날짜,요일설정블록
    # 짧은요일형식일경우
    # 가장가까운 요일에 해당하는 날짜를 설정
    if tempcmd[0] in shortweeklist:
        strfulldate = findnextweekday(objtoday, tempcmd[0])
        strday = tempcmd[0]

    # 긴요일형식일경우
    # 가장가까운 요일에 해당하는 날짜를 설정(X요일중 'X'만설정)
    elif tempcmd[0] in longweeklist:
        strfulldate = findnextweekday(objtoday, tempcmd[0])
        strday = tempcmd[0][:1]
    # 요일형식이 아닌경우
    else:
        temprtn = tofulldate(tempcmd[0])
        # 날짜형식이 유효할시
        # 날짜,요일 설정
        if temprtn != "err":
            strfulldate = temprtn
            strday = shortweeklist[datetime.strptime(temprtn, "%Y/%m/%d").weekday]

        # 날짜가 유효하지 않을 시
        # 에러메세지 설정하고 함수끝
        else:
            mslist.append("날짜형식이 유효하지않습니다.\nex1)월\nex2)화요일\nex3)7-8\nex4)07/08 ")
            return 0

    ##시간설정블록
    # 시간이 유효할시
    # 시간 설정
    strtime = totime(tempcmd[1])
    if strtime == "err":
        mslist.append("시간형식이 유효하지 않습니다.\nex1)월\nex2)화요일\nex3)7-8\nex4)07/08 ")
        return 0

    ##보스설정블록
    # 보스가 유효할시
    # 보스 설정
    if isValidbss(tempcmd[2] == True):
        strbss = tempcmd[2]
    # 보스가 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
        mslist.append("시간형식이 유효하지 않습니다.5글자이내.\nex1)하루윌\nex2)하스데\nex3)진듄더")
        return 0

    ##참가자설정블록
    # 참가자가 "모두" 유효할시
    # 참가자 설정
    if False in list(isValidattendee(tempcmd[i]) for i in range(3, len(tempcmd))):
        for i in range(3, len(tempcmd)):
            stratendee.append(tempcmd[i])
    # 참가자가 "하나라도" 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
        return 0

    # DBinsert
    bssch = Bschedule()
    bssch.bdate = strfulldate
    bssch.bday = strday
    bssch.btime = strtime
    bssch.bbname = strbss
    bssch.bone = stratendee[0]
    if len(stratendee) > 1:
        bssch.btwo = bssch[1]
    if len(stratendee) > 2:
        bssch.bthree = bssch[2]
    if len(stratendee) > 3:
        bssch.bfour = bssch[3]
    if len(stratendee) > 4:
        bssch.bfive = bssch[4]
    if len(stratendee) > 5:
        bssch.bsix = bssch[5]

    bssch.save()
    mslist.append(
        stratendee[0] + "님의" + strbss + "일정(" + strday + " " + strtime + ")이 등록되었읍니다."
    )
    selectschedule("none")

    return 0


def deleteschedule(pram):
    return 0


def selectschedule(pram):
    global mslist
    schedules = ""
    strtoday = datetime.today().strftime("%Y/%m/%d")

    if pram == "none":
        schedules = Bschedule.objects.order_by("date", "time").all()
        mslist.append(viewformatter("A", pram, schedules))

    elif pram in bsslist:
        schedules = schedules.filter(bbname=pram).order_by("date", "time")
        mslist.append(viewformatter("C", pram, schedules))

    else:
        schedules = Bschedule.objects.filter(bdate__gte=strtoday)
        schedules = schedules.filter(bsisdeleted=0)
        schedules = schedules.filter(
            Q(bone=pram)
            | Q(btwo=pram)
            | Q(bthree=pram)
            | Q(bfour=pram)
            | Q(bfive=pram)
            | Q(bsix=pram)
        ).order_by("date", "time")
        mslist.append(viewformatter("C", pram, schedules))

    return 0


# 쿼리의 결과 값을 받아서 메세지용 포맷(날짜별 그룹화)으로 바꾼다
# 인수1: 메세지 타입(조건) A: 전체(조건없음) B: 보스 C:참가자
# 인수2: 조건인자
# 인수3: 오브젝트리스트
# 반환: 메세지용 문자열
def viewformatter(charmsgtype, strparam, objlist):
    strtemp = ""
    if charmsgtype == "A":
        strtemp = "이번주 등록된 전체 일정입니다.\n\n"
    if charmsgtype == "B":
        strtemp = "이번주 " + strparam + " 일정입니다.\n\n"
    if charmsgtype == "C":
        strtemp = "이번주 " + strparam + "님의 일정입니다.\n\n"

    if len(objlist) == 0:
        strtemp = "일정이 없읍니다."
        return strtemp

    ozro = objlist[0]
    strtemp = ozro.bday + " " + ozro.bdate[5:7] + "/" + ozro.bdate[8:10] + "\n"
    strtemp = strtemp + ozro.btime + " " + ozro.bbname + "\n"
    strtemp = (
        strtemp
        + "            "
        + ozro.bone
        + " "
        + ozro.btwo
        + " "
        + ozro.bthree
        + " "
        + ozro.bfour
        + " "
        + ozro.bfive
        + " "
        + ozro.bsix
    )
    strtemp = strtemp.rstrip(" ") + "\n"

    if len(objlist) < 2:
        strtemp = strtemp.rstrip("\n")
        return strtemp

    for i in range(1, len(objlist)):
        oj = objlist[i]
        if oj.bdate != objlist[i - 1].date:
            strtemp = (
                strtemp
                + oj.bday
                + " "
                + oj.bdate[5:7].lstrip("0")
                + "/"
                + oj.bdate[8:10].lstrip("0")
                + "\n"
            )
        strtemp = strtemp + oj.btime + " " + oj.bbname + "\n"
        strtemp = (
            strtemp
            + "            "
            + oj.bone
            + " "
            + oj.btwo
            + " "
            + oj.bthree
            + " "
            + oj.bfour
            + " "
            + oj.bfive
            + " "
            + oj.bsix
        )
        strtemp = strtemp.rstrip(" ") + "\n"

    strtemp = strtemp.rstrip("\n")
    return strtemp


# 인수의 갯수를 체크한다.
# 인수 minparam:최소 인수 갯수
# 인수 paramlenth:받은 인수 갯수
# 반환 인수갯수가 최소갯수보다 크거나 같을시 True를 반환
def hasEnoughParam(minparam, paramlenth):
    global mslist
    if paramlenth >= minparam:
        mslist.append("인수 갯수가 부족합니다.")
        return True
    else:
        return False


# 인수를 날짜로 변환한다
# 인수 날짜부
# 반환 날짜가 유효할시 날짜(yyyy/mm/dd)
# 반환 날짜가 유효하지 않을 시 err
# 가능포맷1 MM/DD or M/D
# 가능포맷2 MM-DD or M-D
# 가능포맷3 MM월DD일 or M월D일
# 가능포맷4 MMDD
def tofulldate(dparam):
    strtyear = str(datetime.now().year)
    strtnowmon = str(datetime.now().month)
    strtmon = ""
    strtdate = ""
    strrtn = ""

    # 구분자가 '월'일경우 ex)m월d일
    # 파라미터 분리
    # 월,일부분이 없을 경우 에러 설정
    if "월" in dparam:
        ttemp = dparam.splite("월")
        if len(ttemp) > 1:
            strtmon = ttemp[0]
            strtdate = ttemp[1].splite("일")[0]
        else:
            strrtn = "err"

    # 구분자가 '-'일경우 ex)m-d일
    # 파라미터 분리
    # 월,일부분이 없을 경우 에러 설정
    elif "-" in dparam:
        ttemp = dparam.splite("-")
        if len(ttemp) > 1:
            strtmon = ttemp[0]
            strtdate = ttemp[1]
        else:
            strrtn = "err"
    # 구분자가 '/'일경우 ex)m/d일
    # 월,일부분이 없을 경우 에러 설정
    elif "/" in dparam:
        ttemp = dparam.splite("/")
        if len(ttemp) > 1:
            strtmon = ttemp[0]
            strtdate = ttemp[1]
        else:
            strrtn = "err"
    # mmdd형식일시
    elif len(dparam) == 4:
        strtmon = dparam[:2]
        strtdate = dparam[2:]
    # md형식일시
    elif len(dparam) == 2:
        strtmon = dparam[0]
        strtdate = dparam[1]
    #  mdd or mmd 형식일시
    #  1월01~09일 vs 10월1~9
    #  1월11~19일 vs 11월1~9
    #  1월21~29일 vs 12월1~9
    # 의 이중의미를 가지나,
    # 운용상 일주일내의 일정등록을 가정으로 하고
    # 이중날짜중 가장차이 적게차이나는것이 20일 내외이므로
    # 두가지모두 날짜로 변환해 오늘날짜에 더 가까운것을 선택
    elif len(dparam) == 3:
        bdate1 = isdate(strtyear, dparam[:1], dparam[1:])
        bdate2 = isdate(strtyear, dparam[:2], dparam[2:])
        # 둘다 유효한 날짜가 아닐시
        if (bdate1 == False) and (bdate2 == False):
            strrtn = "err"
        # 첫 번째 날짜만 유효할시
        elif (bdate1 == True) and (bdate2 == False):
            strtmon = dparam[:1]
            strtdate = dparam[1:]
        # 두 번째 날짜만 유효할시
        elif (bdate1 == False) and (bdate2 == True):
            strtmon = dparam[:2]
            strtdate = dparam[2:]
        else:
            snmd = selectnearestmonanddate(
                strtyear + "/" + dparam[:1] + "/" + dparam[1:],
                strtyear + "/" + dparam[:2] + "/" + dparam[2:],
            )
            strtmon = snmd.splite("/")[0]
            strtdate = snmd.splite("/")[1]

    # 대응 포맷이 아닐시
    else:
        strrtn = "err"

    # 설정된 에러가 없을시
    if strrtn == "":
        # 이번달이 12월이고 입력받은 달이 1월일경우
        # 년도 +1
        if (strtnowmon == "12") and (strtmon == "1" or strtmon == "01"):
            strtyear = str(int(strtyear) + 1)
        try:
            strrtn = datetime.strptime(
                strtyear + "/" + strtmon + "/" + strtdate, "%Y/%m/%d"
            ).strftime("%Y/%m/%d")
        except:
            strrtn = "err"

    return strrtn


# 날짜 두개를 받아서 가장 가까운 날짜를 반환
# 인수1 yyyy/MM/D
# 인수2 yyyy/M/DD
# 반환 MM/DD문자열
def selectnearestmonanddate(strdt1, strdt2):
    objdt1 = datetime.strptime(strdt1, "%Y/%m/%d")
    objdt2 = datetime.strptime(strdt2, "%Y/%m/%d")
    objdttoday = datetime.now()

    intdt_t1 = (objdt1 - objdttoday).days
    intdt_t2 = (objdt2 - objdttoday).days

    strrtn1 = str(objdt1.month) + "/" + str(objdt1.date)
    strrtn2 = str(objdt2.month) + "/" + str(objdt2.date)

    if intdt_t1 == 0:
        return strrtn1
    if intdt_t2 == 0:
        return strrtn2

    # 둘다 미래일경우
    if (intdt_t1 > 0) and (intdt_t2 > 0):
        return strrtn1
    # t1보단미래 t2보단 과거
    elif (intdt_t1 < 0) and (intdt_t2 > 0):
        return strrtn2
    # 둘다 과거
    else:
        return strrtn1


# 날짜 인지 체크
# 인수 연,월,일
# 반환 True or False
def isdate(year, mon, date):
    rtn = ""
    try:
        datetime.strptime(year + "/" + mon + "/" + date, "%Y/%m/%d")
        rtn = True
    except:
        rtn = False
    return rtn


# 시간포맷으로 변환한다
# 인수 시간부
# 반환 시간이 유효할시 True를 반환
# 반환 시간이 유효하지 않을 시 "err"를 반환
# 대응포맷 hh:mm (24시간제)
# 대응포맷 hhmm (24시간제)
def totime(time):
    rtn = "err"
    reg1 = re.compile(r"^([1-9]|[01][0-9]|2[0-3]):([0-5][0-9])$")
    ttime = ""

    if (":" in time) and (1 < len(time.splite(":"))):
        str00hh = time.splite(":")[0].zfill(2)
        str00mm = time.splite(":")[1].zfill(2)

    if (":" not in time) and (2 < len(time) < 5):
        str00hh = time[:-2].zfill(2)
        str00mm = time[-2:].zfill(2)

    ttime = str00hh + ":" + str00mm

    if reg1.match(ttime):
        rtn = ttime

    return rtn


# 보스이름 길이체크
# 인수 보스이름
# 반환 길이가 최대길이 보다 작거나 같으면 True
def isValidbss(bs):
    if len(bs < 5):
        return True
    else:
        return False


# 닉네임 길이체크
# 인수 닉네임
# 반환 길이가 최대길이 보다 작거나 같으면 True
def isValidattendee(at):
    if len(at < 6):
        return True
    else:
        return False


# 인수1:오늘날짜 오브젝트
# 인수2:찾는 요일
# 반환값: 지정한요일이 돌아오는 가장 빠른날짜(당일포함) YYYY/MM/DD
def findnextweekday(objnowdate, strseekweekday):
    wdidx = shortweeklist.find(strseekweekday)
    # 지정요일이 오늘 요일과 같을때
    if objnowdate.weekday == wdidx:
        return objnowdate.strftime("%Y/%m/%d")
    # 요일이 오는 가장빠른 날짜 구하기
    else:
        intdt = ((objnowdate.weekday + 7) % 7) - wdidx
        return (objnowdate + deltatime(days=intdt)).strftime("%Y/%m/%d")
