import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
import re
from datetime import datetime

import db

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument("--disable-dev-shm-usage")

## 특정 태그(로그인 성공 시 생성) 나올때까지 기다리기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def newLoginSession(email, ID):
    '''
    새로운 세션 생성
    - email: DB에 저장된 이메일 입력(이메일 전송용)
    '''
    
    driver = webdriver.Chrome('./chromedriver', options=options)
    # 창 최대화(최종 구현 시 창 제거 커맨드 입력해야함.)
    # driver.maximize_window()

    driver.get('https://discord.com/login')

    # QR코드가 생성되어 표시될 때 까지 기다림
    # QR_Code_Base64 = driver.find_element_by_class_name('qrCode-2R7t9S').find_element_by_tag_name('img').get_attribute('src')
    QR_Code_Base64 = WebDriverWait(driver, timeout=60).until( EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[3]/div/div/div/div[1]/div[1]/img')) )
    QR_Code_Base64 = QR_Code_Base64.get_attribute('src')
#     print(QR_Code_Base64)
    
    # 메소드 실행
    QR_Code_Send_Email(email, QR_Code_Base64)
    result = loginCheck(driver)
    
    if result == 'ok':
        keyword = db.getKeyword(ID)
        crawling(driver, ID, keyword)
    
    # 단, 주의해야 할 점은 창이 보이지 않는다고 동작이 멈춘게 아니기 때문에, 원하는 작업이 끝났으면 quit() 함수로 반드시 종료해주어야 합니다. 그러지 않으면 backgroud에서 chrome이 계속 리소스를 잡아먹고 있게 됩니다.
    driver.quit()

######################################## 이메일 전송 ##########################################
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formatdate
from email.mime.base import MIMEBase
import secretAccount as secret

def QR_Code_Send_Email(mailAddr, QR_Code_Base64):
    '''
    디스코드 로그인 QR코드를 메일로 전송하기 위한 코드
    - mailAddr: 수신자의 메일주소
    - QR_Code_Base64: QR코드를 Base64로 변환하여 입력
    '''
    
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # TLS 보안 시작
    s.starttls()

    # 로그인 인증
    s.login(secret.emailID, secret.emailPW) # 비번 포함됨!!!!!! 유출 주의

    # 보낼 메시지 설정
    msg = MIMEMultipart()
    msg['From'] = '디스코드 알리미' # 표시될 이름
    msg['To'] = mailAddr
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s='디스코드 알리미 로그인 QR코드', charset='utf-8')
    # body = MIMEText('첨부된 파일 확인해 주세요.', _charset='utf-8')
    body = MIMEText('디스코드 알리미 로그인 QR코드입니다. <br />' + 
                    '아래의 QR코드를 디스코드 앱 내의 좌측 상단 三 메뉴 -> 우측 하단 디스코드 아이콘 -> <br />' + 
                    '[사용자 설정] 항목의 [QR 코드 스캔] 기능으로 스캔해주세요! <br />' + 
                    '<b>해당 QR코드는 약 1분간 유효합니다.</b><br /><br /><br /><img src=' + QR_Code_Base64 + ' />', 'html')
    msg.attach(body)

    ## 첨부파일 전송: base64 형태로 바로 입력받을 수 있도록 수정함. ## 이거 사용 없이 가능
    part = MIMEBase('application', "octet-stream")
    part.add_header('Content-Transfer-Encoding', 'base64')
    part.add_header('Content-Disposition', 'attachment; filename="QR CODE.png"')
    part.set_payload(QR_Code_Base64.split(sep='data:image/png;base64,')[1]) # 첨부될 base64 기반 문자열 입력
    msg.attach(part)
    
    ## 디버깅용 로그
#     print(part)
#     type(part)

    # msg['Subject'] = '제목 : 메일 보내기 테스트'
    # msg = MIMEText('내용 : 본문내용 테스트', _charset='utf-8')

    # 메일 보내기
    s.sendmail(secret.emailID, mailAddr, msg.as_string())
    # s.send_message(msg) # 이걸로 하면 한글 이름이 제대로 표시되지 않음!

    # 세션 종료
    s.quit()
    
    print('QR코드 메일 전송 완료!')

def errLogEmail(mailAddr, err):
    '''
    오류 시 이메일로 알려주기 위한 코드
    - mailAddr: 수신자의 메일주소
    - err: 오류 내용
    '''
    
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # TLS 보안 시작
    s.starttls()

    # 로그인 인증
    s.login(secret.emailID, secret.emailPW) # 비번 포함됨!!!!!! 유출 주의

    # 보낼 메시지 설정
    msg = MIMEMultipart()
    msg['From'] = '디스코드 알리미' # 표시될 이름
    msg['To'] = mailAddr
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s='알리미 오류 발생!', charset='utf-8')
    # body = MIMEText('첨부된 파일 확인해 주세요.', _charset='utf-8')
    body = MIMEText('다음과 같은 오류가 발생했습니다. </br></br>[Error LOG]</br>' + str(err), 'html')
    msg.attach(body)


    # 메일 보내기
    s.sendmail(secret.emailID, mailAddr, msg.as_string())
    # s.send_message(msg) # 이걸로 하면 한글 이름이 제대로 표시되지 않음!

    # 세션 종료
    s.quit()
    
    print('[LOG] 오류발생 - 메일 전송 완료!')

##################################### 로그인 성공 여부 판단 #######################################

def loginCheck(driver):
    try:
        nickname = WebDriverWait(driver, timeout=60).until( EC.presence_of_element_located((By.CLASS_NAME, 'title-338goq')) )
        print('로그인 성공!')
        print('닉네임: ' + nickname.text)
        return 'ok'
    except Exception as e:
        print('[LOG] 로그인하지 않아서 세션 종료!')
        errLogEmail("tiger8084@naver.com", '60초간 로그인하지 않음. 크롤링 코드 종료합니다.')
        errLogEmail("positionace@naver.com", '60초간 로그인하지 않음. 크롤링 코드 종료합니다.')
        db.update_crawling_state(ID, 'False') # DB에 크롤링 작동 상태 False로 저장.
        return 'off'
        

# 닉네임 DB에 기록
# 앱에 ???님 로그인 하신 것을 환영합니다. 띄워주면 좋을듯?

######################################### 크롤링 코드 입력 ########################################
import datetime

def crawling(driver, ID, keyword):
    
    # 아만URL = "https://discord.com/channels/660684739056762891/724168359171719199" #키워드 선택이랑 서버선택도 해야함 서버선택에서 해당서버 url 들 서버=url
    print("1구간")
    count=0
    while(True):
        print("2구간")
        try:
            print("3구간")
            if db.getState(ID) == 'False':
                print('[LOG] state: False! 크롤링 종료합니다.')
                db.sendMessage(ID, 'state: False! 알림을 종료합니다.', '[알림 상태 변경]')
                errLogEmail("tiger8084@naver.com", 'state: False! 크롤링 종료합니다.')
                errLogEmail("positionace@naver.com", 'state: False! 크롤링 종료합니다.')
                break
            else:
                print(str(datetime.datetime.now().replace(microsecond=0)))
                print('URL: ' + db.getServerURL(ID)) # 구분자
                driver.get(db.getServerURL(ID))
                # driver.get(아만URL)
                print("4구간")
                while(True):
                    element = driver.find_elements_by_class_name("contents-2MsGLg")
                    if element:
                        check=checking(element)
                        break
                    else:
                        time.sleep(5)
                        print("긁어오기 실패 재탐색")
                    # element = WebDriverWait(driver, timeout=60).until( EC.presence_of_elements_located((By.CLASS_NAME, 'contents-2MsGLg')) )
                     
                    # print(type(element))
                    # print('check1:' + str(check))
                print("5구간")
                while(True):
                    print("6구간")
                    print(check)
                    context = re.sub(r'\[[^)]*\]', '',element[check].text)
                    print('[LOG] 1')
                    
                    # print('check2: ' + str(check))
                    check=check+1
                    if keyword in context:
                        print("[LOG] push 전송!")
                        db.sendMessage(ID, '키워드: ' + str(keyword) + '알림', '[키워드 알림]')
                        count=1
                    else:
                        print("[LOG] no")
                    if check == 50:
                        print("7구간")
                        break
                if count == 1:
                    print("count=1")
                    time.sleep(3300)
                else:
                    print("count=0")
                    time.sleep(180)
        except Exception as e:
            print('[LOG] 오류 발생.. 크롤링 종료합니다.')
            print(e)
            db.update_crawling_state(ID, 'False') # DB에 크롤링 작동 상태 False로 저장.
            db.sendMessage(ID, '서버 오류로 알림을 종료합니다.', '[오류 발생!]')
            errLogEmail("tiger8084@naver.com", e)
            errLogEmail("positionace@naver.com", e)
            break
        

    
    ## 파싱부분
    # 아만URL = "https://discord.com/channels/660684739056762891/724168359171719199" #키워드 선택이랑
    # driver.get(아만URL) # 아만
    # driver.get('https://discord.com/channels/762164926436343888/762524681621209098') # genshin
    # # # driver.get('https://discord.com/channels/932250790071009342/932250790071009346') # test
    

    # time.sleep(7)

    # chat_list = driver.find_elements_by_class_name('messageContent-2t3eCI')

    # for i in chat_list:
    #     print(i.text)

# def crawling(driver, keyword):
#     time.sleep(4)
#     아만URL = "https://discord.com/channels/660684739056762891/724168359171719199" #키워드 선택이랑 서버선택도 해야함 서버선택에서 해당서버 url 들 
#     driver.get(아만URL)

#     time.sleep(4)
#     element = driver.find_elements_by_class_name("contents-2MsGLg")

#     check=checking(element)
#     while(True):
#         context = re.sub(r'\[[^)]*\]', '',element[check].text)
#         print(context)
#         check=check+1
#         if keyword in context:
#             print("push")
#         else:
#             print("no")
#         if check == 50:
#             break

def checking(element):
    i=0
    check=0
    print('checking: ' + str(type(element)))
    for _ in element:
        context = element[i].text
        print('[LOG]2')
        if "떠돌이 상인은" in context:
            check=i
            i=i+1
        else:
            i=i+1
            check=check
    return check