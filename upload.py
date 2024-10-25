import os
import re
import requests, json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def upload_file(upload_path, week_number):
    # 查看学生已提交的作业
    driver.find_element(By.XPATH, "//tr[@class='MenuGrid' and td/a/span[@id='Menu1_DataGrid1__ctl11_Label1']]").click()
    driver.find_element(By.ID, "Menu1_Hyperlink3").click()

    # 添加学生并上传文件
    file_list = [pdf_file for pdf_file in os.listdir(upload_path)
                 if pdf_file.endswith('.pdf')]

    for pdf_file in file_list:
        # 进入反馈信息页面
        driver.find_element(By.ID, "Menu1_Hyperlink1").click()
        # g = str(int(int(week_number) / 2 + 1))
        g = str(int(Info["homework_number"]) + 1)
        week_id = f"Menures1_MyList__ctl{g}_rb"
        driver.find_element(By.ID, week_id).click()
        student_name = pdf_file.replace(".pdf", "")
        student_number = student_list[student_name]
        select = Select(driver.find_element(By.ID, 'Menures1_ListBox1'))
        select.select_by_value(student_number)
        driver.find_element(By.ID, "Menures1_ImageButton1").click()
        # 反馈内容
        textarea = driver.find_element(By.ID, 'Menures1_txtDescription')
        textarea.send_keys('详情查看附件')
        # 上传文件
        file_input = driver.find_element(By.ID, 'Menures1_AttachFile')
        path = '.\\homework\\' + week_number
        if pdf_file.startswith(week_number):
            os.rename(os.path.join(path, pdf_file), os.path.join(path, week_number + '-' + pdf_file))
            path = os.path.join(path,  week_number + '-' + pdf_file)
        else:
            path = os.path.join(path, pdf_file)
        pdf_path = os.path.normpath(os.path.join(os.getcwd(), path))
        file_input.send_keys(pdf_path)
        # 提交文件
        print(pdf_path)
        submit_button = driver.find_element(By.ID, 'Menures1_btnUpload')
        # submit_button.click()

    print(file_list)


with open("Info.json", "r", encoding='utf-8') as f:
    Info = json.load(f)
# Set the login URL and the protected page URL
login_url = "http://www.phycai.sjtu.edu.cn/wis/login.aspx"

ex_url = "http://www.phycai.sjtu.edu.cn/"

login_data = {
    "login1:usern": Info["login1:usern"],
    "login1:pass": Info["login1:pass"]
}
work_path = os.path.join(Info["homework_path"], Info["week_number"])
with open(Info["student_list_path"], "r", encoding='utf-8') as file:
    student_couples = file.readlines()
    student_list = {student_couple.replace("\n", "").split("\t")[1]: student_couple.replace("\n", "").split("\t")[0]
                    for student_couple in student_couples
                    }

driver = webdriver.Chrome(Info["Chrome_path"])
driver.get(login_url)

# Log in
for data in login_data.keys():
    search_box = driver.find_element(By.NAME, data)
    search_box.send_keys(login_data[data])

driver.find_element(By.ID, "login1_user_1").click()     # TA
search_box.send_keys(Keys.RETURN)

dec = input("上传前请确认作业已批改完成，并且格式正确，注意修改Info文件。输入 y 上传，输入 n 退出\n")
while True:
    if dec == "y":
        upload_file(work_path, Info["week_number"])
    elif dec == "n":
        break
    else:
        print("请重新输入")
time.sleep(3)
driver.quit()
