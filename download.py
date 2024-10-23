# encoding = utf-8
import json
import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def repeat_check(a):
    g = []
    repeat = []
    for ele in a:
        if ele not in g:
            g.append(ele)
        else:
            repeat.append(ele)
    return repeat


def get_url(html_data, max_number=26):
    # 使用正则表达式提取学号和URL
    pat = re.compile(r'（(\d{12})）.*?<a href=(/wis/UploadFile/projfile.*?)>', re.DOTALL)
    matches = re.findall(pat, html_data)
    rep = repeat_check([match[0] for match in matches])
    result = {
        match[0]: match[1] for match in matches
    }
    print(result)
    return result, rep


def download_files(students, downLoad_path, week):
    # 查看学生已提交的作业
    driver.find_element(By.XPATH, "//tr[@class='MenuGrid' and td/a/span[@id='Menu1_DataGrid1__ctl11_Label1']]").click()
    driver.find_element(By.ID, "Menu1_Hyperlink3").click()
    no_upload = []
    # Download files
    # choose week number

    visible_name = "第" + week + "周作业"
    week_chose = Select(driver.find_element(By.ID, "_ctl0_listProjName"))
    week_chose.select_by_visible_text(visible_name)

    file_urls, repeat_container = get_url(driver.page_source.replace('\"', ""))
    for student_name in students.keys():
        student_number = students[student_name]
        if student_number in file_urls.keys():
            student_file = ex_url + file_urls[student_number]
            response = requests.get(student_file, stream=True)
            with open(os.path.join(downLoad_path, student_name + ".pdf"), "wb") as f:
                f.write(response.content)
        else:
            no_upload.append(student_name)
    return repeat_container,no_upload


# Load Student List {student_name: student_number}
student_list_file = r'./StudentList/StudentsList.txt'
with open(student_list_file, "r", encoding='utf-8') as file:
    student_couples = file.readlines()
    student_list = {student_couple.replace("\n", "").split("\t")[1]: student_couple.replace("\n", "").split("\t")[0]
                    for student_couple in student_couples
                    }

# Set the login URL and the protected page URL
login_url = "http://www.phycai.sjtu.edu.cn/wis/login.aspx"

ex_url = "http://www.phycai.sjtu.edu.cn/"

# Initial

with open("./Info.json", "r") as file:
    Info = json.load(file)
login_data = {
    "login1:usern": Info["login1:usern"],
    "login1:pass": Info["login1:pass"]
}
week_number = Info["week_number"]
DownLoad_path = os.path.join(Info["homework_path"], week_number)
student_list_path = Info["student_list_path"]
Chrome_path = Info["Chrome_path"]

driver = webdriver.Chrome(Chrome_path)
driver.get(login_url)

# Log in
for data in login_data.keys():
    search_box = driver.find_element(By.NAME, data)
    search_box.send_keys(login_data[data])

driver.find_element(By.ID, "login1_user_1").click()     # TA
search_box.send_keys(Keys.RETURN)

# DownLoad files
repeat_file, no_upload_list = download_files(student_list, DownLoad_path, week_number)

print(no_upload_list)
print(f"there are {len(no_upload_list)} students havn't upload homework.")

time.sleep(2)
driver.quit()
if repeat_file:
    print("Following student(number) upload more than one files, please check.(如果出错就说明重复提交的不是你的学生)")
    for number in student_list.values():
        if number in repeat_file:
            print("ID_number:" + number)

