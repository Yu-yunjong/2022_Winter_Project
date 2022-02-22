import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import json
from pyfcm import FCMNotification

import secretAccount as secret

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

# DB Setting
def dbConnect():
    conn = pymysql.connect (host=secret.db_host, 
                          user=secret.db_user, password=secret.db_password, db=secret.db_name, charset='utf8')
    return conn

def user_insert(ID, pwd, server):
    conn = dbConnect()
    cur = conn.cursor()
    sql = 'INSERT INTO userinfo(id, pwd, server) VALUES("' + ID + '", "' + pwd + '", "' + server + '");'
    cur.execute(sql)
    conn.commit()
    conn.close()

# 아이디 중복 체크 - 중복된 아이디 개수를 반환함.
def idCheck(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT * FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
#     print(len(rows))
    conn.close()
    return len(rows)

# 안드로이드 푸시 구현을 위한 appnumber 삽입
def appnum_insert(ID, appnum):
    conn = dbConnect()
    curs = conn.cursor()
    sql = "UPDATE userinfo SET appnum = %s WHERE id = %s;"
    result = curs.execute(sql, (appnum, ID))
    conn.commit()
    conn.close()
    return result

# 키워드 설정
def update_keyword(ID, keyword):
    conn = dbConnect()
    curs = conn.cursor()
    sql = "UPDATE userinfo SET keyword = %s WHERE id = %s;"
    result = curs.execute(sql, (keyword, ID))
    conn.commit()
    conn.close()
    return result

# keyword 가져오기
def getKeyword(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT keyword FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()
    
    # id가 존재하지 않는 경우 err 리턴
    if len(rows) == 0:
        return "err"
    else: # 그 외의 경우 Keyword값 리턴
        return rows[0][0]

# 크롤링 상태(state) 확인
def getState(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT state FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()
    
    # id가 존재하지 않는 경우 err 리턴
    if len(rows) == 0:
        return "err"
    else: # 그 외의 경우 state값 리턴
        return rows[0][0]

# 크롤링 상태 설정
def update_crawling_state(ID, state):
    conn = dbConnect()
    curs = conn.cursor()
    sql = "UPDATE userinfo SET state = %s WHERE id = %s;"
    
    # print('state' + str(state) + str(type(state)))
    if ((state == 'False') or (state == 'True')):
        result = curs.execute(sql, (state, ID))
        conn.commit()
        conn.close()
        return result
    else: # True와 False가 아닌 경우.(첫 글자 소문자도 여기에 해당.)
        conn.close()
        return 'err'

# appnum(토큰값) 가져오기
def getAppnum(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT appnum FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()

    # id가 존재하지 않는 경우 err 리턴
    if len(rows) == 0:
        return "err"
    else: # 그 외의 경우 토큰값 리턴
        return rows[0][0]

# 크롤링 state(상태) 조회
def getState(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT state FROM userinfo WHERE id = '" + ID + "';"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()
    return rows

# 최근 로그인 일자 업데이트
def lastLoginUpdate(ID):
    conn = dbConnect()
    curs = conn.cursor()
    sql = "UPDATE userinfo SET lastLoginDate = current_timestamp() WHERE id = %s;"
    result = curs.execute(sql, (ID))
    conn.commit()
    conn.close()
    return result

# 서버 이름 가져오기
def getServerName(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT server FROM userinfo WHERE id = %s;"
    curs.execute(sql, (ID))

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()

    # 서버 이름이 존재하지 않는 경우 err 리턴
    if len(rows) == 0:
        return "err"
    else: # 그 외의 경우 서버 URL 리턴
        return rows[0][0]

# 서버별 디스코드 url 가져오기
def getServerURL(ID):
    conn = dbConnect()
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "SELECT url FROM serverlist WHERE server = %s;"
    curs.execute(sql, (getServerName(ID)))

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()

    # 서버 이름이 존재하지 않는 경우 err 리턴
    if len(rows) == 0:
        return "err"
    else: # 그 외의 경우 서버 URL 리턴
        return rows[0][0]
