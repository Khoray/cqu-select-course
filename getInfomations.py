from Course import *
session = Session()
get_session(session)
print("登录成功")

sel = open("sel.txt", "r")
to = open("tobeselect.txt", 'w')

toSel = [[]]
for line in sel.readlines():
    tmp = line.replace('\n', '').split()
    if(len(tmp)):
        print("正在获取", tmp[0], "的信息...")
        c = Course.loadByCourse(tmp[0], tmp[1], session)
        to.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (c.courseName, c.courseCode, c.courseId, c.courseCategory, c.selectionArea, c.programType, c.courseNature, c.studyNature, c.classId, c.selectionSource) + '\n')
    else:
        to.writelines('\n')