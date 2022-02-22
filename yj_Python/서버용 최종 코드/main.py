import json
from flask import Flask , request
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from pyfcm import FCMNotification
from threading import Thread

# 사용자 py 스크립트
import secretAccount as secret
import crawling
import db



# 안드로이드 푸시 전송
push_service = FCMNotification(secret.FCM_APIKEY)
def sendMessage(ID, body, title):
    TOKEN = getAppnum(ID)
    
    # 메시지 (data 타입)
    data_message = {
        "body": body,
        "title": title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    result = push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)
 
    # 전송 결과(로그) 출력
    print('[LOG] 푸시 전송 결과')
    print(result)


###### Flask 서버 시작
# 초기화
app = Flask(__name__)

# json 형태로 반환
def statusCodeToJson(code, reason):
    data = {"code":str(code), "reason":reason}
    # response1=json.dumps(data)

    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

# json 형태로 반환1
def statusCodeToJson1(code, reason, state):
    data = {"code":str(code), "reason":reason, "state":str(state)}
    # response1=json.dumps(data)

    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

# POST 방식 => DB에 추가
@app.route("/addUserDB", methods=['POST'])
def add_userDB():
    # 파라미터 값(application/x-www-form-urlencoded 방식)
    # ID = request.form['id']
    # pwd = request.form['pwd']
    # server = request.form['server']
    
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    ID = params['id']
    pwd = params['pwd']
    server = params['server'] # 'server_name'
    
    if db.idCheck(ID) >= 1: # 검색결과가 1건이면(혹시몰라 이상일 경우도 체크함.)
        return statusCodeToJson(300, "존재하는 ID입니다. 다른 아이디로 다시 가입해주세요.")
    else:
        pw_hashed = generate_password_hash(pwd) # 비번 암호화
        db.user_insert(ID, pw_hashed, server) # DB입력
        print('[LOG]')
        print('회원가입 성공!')
        print(f"id = {ID}, server = {server}")
        return statusCodeToJson(200, "회원가입 성공!")

# 로그인 체크
@app.route("/loginCheck", methods=['POST'])
def loginCheck():
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    ID = params['id']
    pwd = params['pwd']
    appnum = params['appnum']
    
    conn = db.dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT pwd FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()
    
    
    if len(rows) == 0: # 일치하는 아이디가 없는 경우
        print('[LOG] 로그인 실패! - 일치하는 아이디가 없음. id = ' + str(ID))
        return statusCodeToJson(300, "로그인 실패! 아이디 및 비밀번호를 확인해주세요.")
    elif check_password_hash(rows[0][0], pwd) == False: # 비밀번호가 틀린 경우
        print('[LOG] 로그인 실패! - 비밀번호가 틀림. id = ' + str(ID))
        return statusCodeToJson(300, "로그인 실패! 아이디 및 비밀번호를 확인해주세요.")
    else:
        print('[LOG] 로그인 성공! - id = ' + str(ID))
        db.lastLoginUpdate(ID)
        db.appnum_insert(ID, appnum) # appnum 업데이트
        return statusCodeToJson(200, "로그인 성공!")

# # 앱 푸시를 위한 appnum 입력 => 로그인 과정에 포함시킴!
# @app.route("/insertAppnum", methods=['POST'])
# def insertAppnum():
#     ## 파라미터 값(json)
#     # print(request.is_json)
#     params = request.get_json()
#     ID = params['id']
#     appnum = params['appnum']
    
#     result = db.appnum_insert(ID, appnum)
    
#     if result == 0: # 기존 값과 동일함 혹은 변경 대상 id가 잘못됨.
#         print('[LOG] 변경할 값과 동일하거나 변경 대상 id가 잘못됨. id = ' + str(ID))
#         return statusCodeToJson(300, "변경 실패! 아이디가 잘못되었거나, 변경할 값이 기존 값과 동일합니다.")
#     elif result == 1: # 변경 성공!
#         print('[LOG] 변경 성공! - id = ' + str(ID))
#         return statusCodeToJson(200, "변경 성공!")
#     else:
#         print('[LOG] 예상치 못한 오류! => /insertAppnum')
#         return statusCodeToJson(400, "예상치 못한 오류!")

# 앱 푸시를 위한 appnum 입력
@app.route("/insertKeyword", methods=['POST'])
def insertKeyword():
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    ID = params['id']
    keyword = params['keyword']
    
    result = db.update_keyword(ID, keyword)
    
    if result == 0: # 기존 값과 동일함 혹은 변경 대상 id가 잘못됨.
        print('[LOG] 변경할 값과 동일하거나 변경 대상 keyword가 잘못됨. id = ' + str(ID))
        return statusCodeToJson(300, "변경 실패! 아이디가 잘못되었거나, 변경할 값이 기존 값과 동일합니다.")
    elif result == 1: # 변경 성공!
        print('[LOG] 변경 성공! - id = ' + str(ID))
        return statusCodeToJson(200, "변경 성공!")
    else:
        print('[LOG] 예상치 못한 오류! => /insertKeyword')
        return statusCodeToJson(400, "예상치 못한 오류!")

# 크롤링 상태 변경
@app.route("/updateCrawllingState", methods=['POST'])
def updateCrawllingState():
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    
    if len(params) == 1: # 파라미터가 1건이면: 조회 기능
        ID = params['id']
        
        rows = db.getState(ID)
        
        if len(rows) == 0: # 일치하는 아이디가 없는 경우
            print('[LOG] state값 조회 오류! - 일치하는 아이디가 없음. id = ' + str(ID))
            return statusCodeToJson(300, "오류! 아이디를 확인해주세요.")
        else:
            print('[LOG] state값 조회 성공! - id = ' + str(ID) + ' / state = ' + str(rows[0][0]))
            return statusCodeToJson1(200, "조회 성공!", rows[0][0]) # state 조회를 위함.
            
    else:               # 파라미터가 2건일때: state 값업데이트 및 크롤링 실행
        ID = params['id']
        state = params['state']
    
        result = db.update_crawling_state(ID, str(state))
        
        if result == 'err': # True 또는 False가 아님. (첫글자 소문자도 여기에 걸러짐.)
            print('[LOG] True 또는 False가 아님. id = ' + str(ID))
            return statusCodeToJson(300, "변경 실패! True 또는 False 값만 입력 가능합니다. (대소문자 구별)")
        elif result == 0: # 기존 값과 동일함 혹은 변경 대상 id가 잘못됨.
            print('[LOG] 변경할 값과 동일하거나 변경 대상 id가 잘못됨. id = ' + str(ID))
            return statusCodeToJson(300, "변경 실패! 아이디가 잘못되었거나, 변경할 값이 기존 값과 동일합니다.")
        elif result == 1: # 변경 성공!
            if state == 'True': # state가 True이면, 크롤링 실행.
                ## 크롤링 코드. 임시로 사용 중단.(테스트) -> 이메일을 아이디로 바꿔야됨!
                th1=Thread(target=crawling.newLoginSession,args=(ID, ID))
                th1.start()
                print('[LOG] 크롤링 코드 실행 성공! - id = ' + str(ID))
                db.sendMessage(ID, 'state: True! 알림 시작', '[알림 상태 변경]')
                return statusCodeToJson(200, "크롤링 코드 실행 성공!")
        
                # 테스트용 코드
                # print('[LOG] 크롤링 코드 실행 성공!(현재는 미실행 - 테스트용) - id = ' + str(ID))
                # return statusCodeToJson(200, "크롤링 코드 실행 성공!(현재는 미실행. - 테스트용)")
            
            elif state == 'False': # state가 False이면, 크롤링 정지
                print('[LOG] 크롤링 상태가 False로 변경됨.  - id = ' + str(ID))
                db.sendMessage(ID, 'state: False! 알림 종료', '[알림 상태 변경]')
                return statusCodeToJson(200, "크롤링 중지로 상태코드 변경됨. (False)")
            
            print('[LOG] 변경 성공! - id = ' + str(ID))
            return statusCodeToJson(200, "변경 성공!")
        else:
            print('[LOG] 예상치 못한 오류! => /updateCrawllingState')
            return statusCodeToJson(400, "예상치 못한 오류!")


# 오류 핸들링
# @app.errorhandler(404)
# def page_not_found(error):
#     return "<h1>404 Error</h1>", 404

# @app.errorhandler(300)
# def error1(error):
#     return "<h1>300 Error</h1>", 300

# @app.errorhandler(400)
# def error2(error):
#     return "<h1>400 Error</h1>", 400



## state 값 조회
# @app.route("/selectState", methods=['POST'])
# def selectState():
#     ## 파라미터 값(json)
#     # print(request.is_json)
#     params = request.get_json()
#     ID = params['id']

#     rows = db.getState(ID)
    
#     if len(rows) == 0: # 일치하는 아이디가 없는 경우
#         print('[LOG] state값 조회 오류! - 일치하는 아이디가 없음. id = ' + str(ID))
#         return statusCodeToJson(300, "오류! 아이디를 확인해주세요.")
#     else:
#         print('[LOG] state값 조회 성공! - id = ' + str(ID) + ' / state = ' + str(rows[0][0]))
#         return statusCodeToJson1(200, "조회 성공!", rows[0][0]) # state 조회를 위함.

@app.route("/crawling", methods=['POST'])
def crawling_test():
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    print(params)
    ID = params['id']
    auth = params['auth']
    if auth == 'abcd':
        email="positionace@naver.com"
        # email="positionace@naver.com"
        # ID = [ID]
        th1=Thread(target=crawling.newLoginSession,args=(email, ID))
        th1.start()
        # crawling.newLoginSession('positionace@naver.com', ID)
        print('[LOG] 크롤링 코드 실행 성공! - id = ' + str(ID))
        return statusCodeToJson(200, "크롤링 코드 실행 성공!")
        
    else:
        print('[LOG] 크롤링 코드 실행 실패!(인증키 오류) - id = ' + str(ID))
        return statusCodeToJson(300, "인증 오류! - 크롤링 코드 실행 실패")

@app.route("/crawling1", methods=['POST'])
def crawling_test1():
    ## 파라미터 값(json)
    # print(request.is_json)
    params = request.get_json()
    print(params)
    ID = params['id']
    auth = params['auth']
    if auth == 'abcd':
        email="yoosj97@naver.com"
        # email="positionace@naver.com"
        # ID = [ID]
        th1=Thread(target=crawling.newLoginSession,args=(email, ID))
        th1.start()
        # crawling.newLoginSession('positionace@naver.com', ID)
        print('[LOG] 크롤링 코드 실행 성공! - id = ' + str(ID))
        return statusCodeToJson(200, "크롤링 코드 실행 성공!")
    else:
        print('[LOG] 크롤링 코드 실행 실패!(인증키 오류) - id = ' + str(ID))
        return statusCodeToJson(300, "인증 오류! - 크롤링 코드 실행 실패")

app.run(host="localhost",port=51123)