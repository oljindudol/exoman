from django.shortcuts import render
from .models import Bschedule
from datetime import datetime
from datetime import deltatime

# Create your views here.


mslist = []
cmdlist = ["일정", "ㅇㅈ", "일정등록", "ㅇㅈㄷㄹ", "일정삭제", "ㅇㅈㅅㅈ"]
longweeklist = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
shortweeklist = ["월", "화", "수", "목", "금", "토", "일"]

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
    strnowyear = objtoday.year
    strnowmon = objtoday.month
    # 날짜 필드 설정용 'yyyy-mm-dd'
    strfulldate = ""
    # 요일 필드 설정용 ex)'월'
    strday = ""
    # 시간 필드 설정용 hh:mm (24시간제)
    strtime = ""
    # 보스 필드 설정용 ex)하루윌
    strbss = ""
    # 보스 참가자1~6 설정용
    strone = ""
    strtwo = ""
    strthree = ""
    strfour = ""
    strfive = ""
    strsix = ""

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
    elif isdate(tempcmd[0] == True):
        dummy = 0

    # 날짜가 유효하지 않을 시
    # 에러메세지 설정하고 함수끝
    else:
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


# 갯수체크를 한다.
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


# 날짜인지체크 한다
# 인수 날짜부
# 반환 날짜가 유효할시 True
# 가능포맷1 MM/DD or M/D
# 가능포맷2 MM-DD or M-D
# 가능포맷3 MM월DD일 or M월D일
# 불가능포맷 MMDD
def isdate(date):

    # 체크1. 길이판별
    # return False

    # 체크2. MM-DD 혹은 MM/DD형식인지 판별
    # return False

    # 전처리. -혹은 / 기점으로 두개로 쪼갠다.
    # 전처리. 좌0패딩
    # 전처리. year에 올해년도를 대입하고 month,date에 인수를 대입한다.
    # 전처리. 당월이12월이고 1월을 입력받았을시, year+1한다.

    # 체크3. 날짜 유효성 체크
    # return False

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
