from Course import *
from multiprocessing import Process
from random import randint


def qiang(courseList):
    session = Session()
    get_session(session)
    for currentCourse in courseList:
        while(True):
            status = currentCourse.select(session)
            if(status.find('超容量') != -1):
                print(currentCourse.courseName, "已满，尝试选取该组下一个...")
                break
            elif(status.find('success') != -1 or status.find('重复选课') != -1):
                print(currentCourse.courseName, "已选择！！")
                return
            else:
                print(currentCourse.courseName, "选择失败，正在尝试重新选择...")
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    sel = open("tobeselect.txt", "r")

    toSel = [[]]
    for line in sel.readlines():
        tmp = line.replace('\n', '')
        if(len(tmp)):
            toSel[-1].append(Course.loadByStr(tmp))
        else:
            toSel.append([])
    print("获取课程内容成功")
    for i in range(len(toSel)):
        print(f"第{i + 1}组：")
        for j in toSel[i]:
            print(j)

    for i in toSel:
        p = Process(target = qiang, args = (i, ))
        p.start()
