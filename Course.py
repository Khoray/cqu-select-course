from random import randint, random
import requests as rq
import win32api
import win32con
import time
import os
from mycqu.auth import login, NeedCaptcha
from mycqu.mycqu import access_mycqu, get_oauth_token
from requests import Session
from multiprocessing import Process
import json

class Course:
    def __init__(self):
        self.courseCode = ""
        self.instructorNames = ""
        self.classNbr = ""
        self.stuCapacity = -1
        self.selectedNum = -1
        self.classId = ""
        self.courseName = ""
        self.courseCategory = ""
        self.selectionArea = ""
        self.programType = ""
        self.courseNature = ""
        self.studyNature = "初修"
        self.selectionSource = "主修"
        self.courseId = ""
        self.courseFull = None
        
    def loadByCourse(courseCode, classNbr, session):
        c = Course()
        c.courseCode = courseCode
        c.classNbr = classNbr
        time.sleep(1)
        c.getCourseInfo(session)
        time.sleep(1)
        c.getClassInfo(session)
        return c

    def loadByStr(s):
        c = Course()
        i = s.split('\t')
        c.courseName, c.courseCode, c.courseId, c.courseCategory, c.selectionArea, c.programType, c.courseNature, c.studyNature, c.classId, c.selectionSource = i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]
        return c

    def __str__(self):
        return str({"courseName" : self.courseName, "instructorNames" : self.instructorNames, "courseCode" : self.courseCode, "classNbr" : self.classNbr})

    def getCourseInfo(self, session):
        url = "https://my.cqu.edu.cn/api/enrollment/enrollment/course-list?selectionSource=%s" % self.selectionSource
        resp = session.get(url)
        if(resp.text.find("success") == -1):
            print("获取失败，重新尝试中...", resp.text)
            self.getCourseInfo()
            return

        d = json.loads(resp.text)
        
        for i in d['data']:
            for cou in i['courseVOList']:
                if(cou['codeR'] == self.courseCode):
                    self.courseName = cou['name']
                    self.courseCategory = cou['courseCategory']
                    self.selectionArea = cou['selectionArea']
                    self.programType = cou['programType']
                    self.courseNature = cou['courseNature']
                    self.courseId = cou['id']
                    return

    def getClassInfo(self, session):
        url = "https://my.cqu.edu.cn/api/enrollment/enrollment/courseDetails/%s?selectionSource=%s" % (
            self.courseId, self.selectionSource)
        resp = session.get(url)
        if(resp.text.find("selectCourseListVOs") == -1):
            print("获取失败，重新尝试中...", resp.text)
            self.getClassInfo()
            return

        d = json.loads(resp.text)
        volist = d['selectCourseListVOs'][0]['selectCourseVOList']

        for j in volist:
            if(j['classNbr'] == self.classNbr):
                self.classId = j['classId']
                self.selectedNum = j['selectedNum']
                self.stuCapacity = j['stuCapacity']
                self.instructorNames = j['instructorNames']
                if(resp.text.find("已选满") != -1):
                    self.courseFull = True
                else:
                    self.courseFull = False

    def select(self, session):
        data = ('{"courses":[{"courseName":"%s","courseCode":"%s","courseId":"%s","courseCategory":"%s","selectionArea":"%s","programType":"%s","courseNature":"%s","studyNature":"%s","classes":[{"classIds":["%s"],"fakeClassTypeList":[]}],"selectedFakeClass":false}],"selectionSource":"%s","reservation":false}' % (
            self.courseName, self.courseCode, self.courseId, self.courseCategory, self.selectionArea, self.programType, self.courseNature, self.studyNature, self.classId, self.selectionSource)).encode('utf-8').decode('latin1')
        hh = {"Content-Type": "application/json",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"}
        resp = session.post(
            "https://my.cqu.edu.cn/api/enrollment/enrollment/student/select", data=data, headers=hh)
        print(resp.text)
        return resp.text


# 登录CQU，获取Authoration
def get_session(session):
    try:
        login(session, "你的认证号", "你的密码")  # 需要登陆
        # login(session, "", "")  # 需要登陆
    except NeedCaptcha as e:  # 需要输入验证码的情况
        with open("captcha.jpg", "wb") as file:
            file.write(e.image)
        print("输入 captcha.jpg 处的验证码并回车: ", end="")
        e.after_captcha(input())

    access_mycqu(session)