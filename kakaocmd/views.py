from django.shortcuts import render
from .models import Bschedule
from datetime import datetime
from datetime import deltatime

# Create your views here.


mslist = []
cmdlist = ["일정", "ㅇㅈ", "일정등록", "ㅇㅈㄷㄹ", "일정삭제", "ㅇㅈㅅㅈ"]
shortweeklist = ["월", "화", "수", "목", "금", "토", "일"]
longweeklist = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

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
    strnowyear = str(objtoday.year)
    strnowmon = str(objtoday.month)
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

    # 날짜형식이 유효할시
    # 날짜,요일 설정
    else:
        temprtn = tofulldate(tempcmd[0])

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
    if istime(tempcmd[1] == False):
        dummy = 0
    # 시간이 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
        return 0

    ##보스설정블록
    # 보스가 유효할시
    # 보스 설정
    if isValidbss(tempcmd[2] == False):
        dummy = 0
    # 보스가 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
        return 0

    ##참가자설정블록
    # 참가자가 "모두" 유효할시
    # 참가자 설정
    if False in list(isValidattendee(tempcmd[i]) for i in range(3, len(tempcmd))):
        for i in range(3, len(tempcmd)):
            dummy = 0
    # 참가자가 "하나라도" 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
        return 0


def deleteschedule(pram):
    return 0


def selectschedule(pram):
    # str(datetime.now().year)
    schedules = Bschedule.objects.all()
    return 0


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
            tmon = ttemp[0]
            tdate = ttemp[1].splite("일")[0]
        else:
            rtn = "err"

    # 구분자가 '-'일경우 ex)m-d일
    # 파라미터 분리
    # 월,일부분이 없을 경우 에러 설정
    elif "-" in dparam:
        ttemp = dparam.splite("-")
        if len(ttemp) > 1:
            tmon = ttemp[0]
            tdate = ttemp[1]
        else:
            rtn = "err"
    # 구분자가 '/'일경우 ex)m/d일
    # 월,일부분이 없을 경우 에러 설정
    elif "/" in dparam:
        ttemp = dparam.splite("/")
        if len(ttemp) > 1:
            tmon = ttemp[0]
            tdate = ttemp[1]
        else:
            rtn = "err"
    # mmdd형식일시
    elif len(dparam) == 4:
        tmon = dparam[:2]
        tdate = dparam[2:]
    # md형식일시
    elif len(dparam) == 2:
        tmon = dparam[0]
        tdate = dparam[1]
    # mmd or mdd 형식일시
    # 10월1~9 vs 1월01~09일
    # 11월1~9 vs 1월11~19일
    # 12월1~9 vs 1월21~29일
    # 의 이중의미를 가지나,
    # 운용상 일주일내의 일정등록을 가정으로 하고
    # 이중날짜중 가장차이 적게차이나는것이 20일 내외이므로 
    # 두가지모두 날짜로 변환해 오늘날짜에 더 가까운것을 선택
    elif len(dparam) == 3:
        bdate1=isdate(strtyear,dparam[:2],dparam[2:])
        bdate2=

    # 대응 포맷이 아닐시
    else:
        rtn = "err"

    # 설정된 에러가 없을시
    if rtn == "":
        # 이번달이 12월이고 입력받은 달이 1월일경우
        # 년도 +1
        if strtnowmon == "12" and (tmon == "1" or tmon == "01"):
            tyear = str(int(strtyear) + 1)
        try:
            rtn = datetime.strptime(
                tyear + "/" + tmon + "/" + tdate, "%Y/%m/%d"
            ).strftime("%Y/%m/%d")
        except:
            rtn = "err"

    return rtn


# 날짜 인지 체크
# 인수 연,월,일
# 반환 True or False
def isdate(year , mon ,date):
    rtn=""
    try:
        datetime.strptime(year + "/" + mon + "/" + date, "%Y/%m/%d")
        rtn=True
    except:
        rtn = False
    
    return rtn



# 시간체크를 한다
# 인수 시간부
# 반환 시간이 유효할시 True를 반환
# 대응포맷 hh:mm hhmm (24시간제)
def istime(time):
    rtn = False
    return rtn


# 보스이름 길이체크
# 인수 보스이름
# 반환 길이가 최대길이 보다 작거나 같으면 True
def isValidbss(bs):
    return True


# 닉네임 길이체크
# 인수 닉네임
# 반환 길이가 최대길이 보다 작거나 같으면 True
def isValidattendee(at):
    return True


# 인수1:오늘날짜 오브젝트
# 인수2:찾는 요일
# 반환값: 지정한요일이 돌아오는 가장 빠른날짜(당일포함)
def findnextweekday(objnowdate, strseekweekday):
    wdidx = shortweeklist.find(strseekweekday)
    # 지정요일이 오늘 요일과 같을때
    if objnowdate.weekday == wdidx:
        return objnowdate.strftime("%Y-%m-%d")
    # 요일이 오는 가장빠른 날짜 구하기
    else:
        intdt = ((objnowdate.weekday + 7) % 7) - wdidx
        return (objnowdate + deltatime(days=intdt)).strftime("%Y-%m-%d")
