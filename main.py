# -*- coding: utf-8 -*-

import telegram
import time
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

TELEGRAM_TOKEN = '부여받은_토큰'   # 처음 받은 HTTP API
CHAT_ID = '채팅방_ID'   # 채팅방 ID: 확인 방법은 문서 참조

SEMESTER = '2023020'    # 2023년도 1학기이면: 2023010과 같이 표현됨
SAINT_ID = '20xxxxxx'   # 학번
SAINT_PW = 'xxxx'       # SAINT 비밀번호

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

previous_data = {}

def get_saint_cookies(id, pw):
    login_url = "https://msaint.sogang.ac.kr/loginproc.aspx"
    header = {
        "User-Agent": "Mozilla/5.0 (iPod; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 \
            (KHTML, like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1"
    }
    LOGIN_INFO = {
        'destURL': '/',
        'userid': id,
        'passwd': pw,
    }
    try:
        session = requests.session()
        response = session.post(login_url, headers=header, data=LOGIN_INFO, verify=False)
        cookies = response.cookies
        if len(cookies) == 0:
            return None
        session.close()
        return cookies
    except:
        print("Failed to login")
        return None

def get_grade_info_by_semester(cookies, semester):
    semester_dict = {}
    semester_url = 'https://msaint.sogang.ac.kr/grade/g5.aspx?isposted=1&semesteridx={}'.format(semester)
    try:
        response = requests.get(semester_url, cookies=cookies, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            courses = soup.select('tr')[1:]
            for course in courses:
                if '학년도 / 학기' in course.text:
                    break
                course_dict = {}
                tds = course.find_all('td')
                course_number = tds[0].text.strip() if len(tds) > 0 else ''
                course_name = tds[1].text.strip() if len(tds) > 1 else ''
                course_credits = tds[2].text.strip() if len(tds) > 2 else ''
                midterm_grade = tds[3].text.strip() if len(tds) > 3 else ''
                final_grade = tds[4].text.strip() if len(tds) > 4 else ''
                course_dict['course_number'] = course_number
                course_dict['course_name'] = course_name
                course_dict['course_credits'] = course_credits
                course_dict['midterm_grade'] = midterm_grade
                course_dict['final_grade'] = final_grade
                semester_dict[course_number] = course_dict
            return semester_dict
        else:
            print('Request failed with status code {}'.format(response.status_code))
            return None
    except requests.exceptions.RequestException as e:
        print('Connection refused by the server: {}'.format(e))
        return None

def check_for_grade_changes(current_data):
    global previous_data
    changes = []
    for course_number, course_info in current_data.items():
        if course_number in previous_data:
            previous_info = previous_data[course_number]
            if course_info['midterm_grade'] != previous_info['midterm_grade']:
                changes.append('{}의 중간 성적 올라옴: {}'.format(course_info['course_name'], course_info['midterm_grade']))
            if course_info['final_grade'] != previous_info['final_grade']:
                changes.append('{}의 최종 성적 올라옴: {}'.format(course_info['course_name'], course_info['final_grade']))
    previous_data = current_data
    return changes

def main():
    cookies = get_saint_cookies(SAINT_ID, SAINT_PW)
    if cookies is None:
        print("Error: Failed to login")
    else:
        print("성적알림봇을 시작합니다. 5분마다 변경사항을 확인합니다.\n확인 중인 학기: " + SEMESTER)
        send_telegram_message("성적알림봇을 시작합니다. 5분마다 변경사항을 확인합니다.\n확인 중인 학기: " + SEMESTER)
        current_data = get_grade_info_by_semester(cookies, SEMESTER)
        msg = "현재 확인 대상 과목과 점수는 다음과 같습니다:\n"
        for course_number, course_info in current_data.items():
            msg += '[' + course_info['course_name'] + ']\n' + " 중간 '" + course_info['midterm_grade'] + "' / 기말 '" + \
                   course_info['final_grade'] + "'\n\n"
        print(msg)
        send_telegram_message(msg)
        while True:
            current_data = get_grade_info_by_semester(cookies, SEMESTER)
            changes = check_for_grade_changes(current_data)
            if changes:
                for change in changes:
                    send_telegram_message(change)
            time.sleep(300)

if __name__ == '__main__':
    main()
