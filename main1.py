# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import codecs
import csv


class Node:
    def __init__(self, value):  # 생성자
        self.data = value  # data
        self.llink = '\0'  # llink
        self.rlink = '\0'  # rlink


class Deque:
    def __init__(self):  # 생성자
        head = Node("trash")  # 헤드포인터 역할을 해줄 노드 생성
        self.head = head  # self.head: 덱의 head 포인터. 첫번째 노드를 가리킴.
        self.tail = '\0'  # self.tail: 덱의 가장 마지막 노드
        self.size = 0  # 덱의 크기(노드의 개수)를 나타내는 변수

    def is_empty(self):
        if self.head.rlink == '\0':
            return True
        else:
            return False

    def enqueue_front(self, data):
        data.over_perfect()  # 만점 초과시
        new_node = Node(data)  # 새로운 노드 생성
        new_node.rlink = self.head.rlink  # 기존의 첫번재 노드를 우링크로 연결
        if(self.is_empty() == False):
            self.head.rlink.llink = new_node  # 기존의 첫번째 노드의 좌링크를 newnode로 연결
        new_node.llink = self.head
        if(new_node.rlink == '\0'):
            self.tail = new_node
        self.head.rlink = new_node  # 첫번째 노드를 새로운 노드로 변경
        self.size = self.size + 1  # count해주기

    def enqueue_rear(self, data):
        data.over_perfect()  # 만점 초과시
        new_node = Node(data)  # 새로운 노드 생성
        if self.tail == '\0':
            if self.head.rlink == '\0':
                new_node.llink = self.head
                new_node.rlink = self.head.rlink
                self.head.rlink = new_node
        else:
            new_node.llink = self.tail  # 기존의 마지막 노드를 좌링크로 연결
            new_node.rlink = self.tail.rlink
            self.tail.rlink = new_node  # 현재 위치 바로 다음을 새로운 노드로 설정
        self.tail = new_node  # 새로운 노드를 마지막 노드로 변경
        self.size = self.size + 1  # count해주기

    def dequeue_front(self):
        if self.is_empty() == True:
            print("ERROR: deque is empty")
            return 0
        elif self.size == 1:
            tmp = self.head.rlink.data
            self.head.rlink = '\0'
            self.tail = '\0'
            self.size = self.size - 1
            return tmp
        else:
            tmp = self.head.rlink.data  # 첫번째 원소의 값 저장
            self.head.rlink = self.head.rlink.rlink  # 두 번째 원소를 첫번째 원소로 변경
            self.head.rlink.llink = self.head  # 새로운 첫번째 원소의 좌링크를 헤드포인터로 변경
            self.size = self.size - 1  # size 변수 관리
            return tmp

    def dequeue_rear(self):
        if self.is_empty() == True:
            print("ERROR: deque is empty")
            return 0
        elif self.size == 1:
            tmp = self.tail.data
            self.tail = '\0'
            self.size = self.size - 1
            self.head.rlink = '\0'
        else:
            tmp = self.tail.data  # 마지막 원소의 값 저장
            self.tail = self.tail.llink  # 마지막에서 두번째 원소를 마지막 원소로 저장
            if self.tail != '\0':
                self.tail.rlink = '\0'  # 새로운 마지막 원소의 우링크 NULL로 다시 바꾸기
            self.size = self.size - 1  # size 변수 관리
        return tmp

    def print_deque(self):  # 덱 출력
        applist = []
        current = self.head.rlink
        if self.is_empty() == True:
            applist.append("empty deque")
        else:
            for i in range(self.size):  # 차례대로 덱의 노드 값 출력
                applist.append(current.data.print_applicant(
                    is_blind))  # is_blind = True/False
                current = current.rlink
        return applist


class Criteria:
    ratesum = 0

    def __init__(self, criteria_name):  # 기준 비중 % / 기준 만점 / 최소 조건 여부
        self.name = criteria_name
        self.rate = 0
        self.perfect = 100.0
       # self.is_min_condition = False
        self.min_condition = 0.0


class Applicant:
    def __init__(self, _id, name, major, selfpr, criteria):
        self._id = _id
        self.name = name
        self.major = major
        self.selfpr = selfpr
        self.criteria_score = criteria  # 기준별 점수 리스트
        self.score = -1  # 총점
        self.pr_score = 0  # 정성평가 점수

    def __str__(self):
        return self.name

    def over_perfect(self):  # 만점(ex. 학점 4.5) 넘으면 0점으로 처리
        for i, my_score in enumerate(self.criteria_score):
            if(float(my_score) > customized_criteriaList[i].perfect):
                self.criteria_score[i] = "0.0"

    def print_applicant(self, is_blind):
        app = ""
        if not(is_blind):
            app += f"-{self.name}: {self.major}, {self._id}"
        for i, my_score in enumerate(self.criteria_score):
            app += f" {customized_criteriaList[i].name}: {my_score}"
        if self.score >= 0:
            app += " 총점 :%.2f" % self.score
        else:
            app += " 총점: 미평가"
        app += f"/ {self.selfpr}"
        return app

    def is_qualified(self):  # 최소조건만족 여부?
        for i, my_score in enumerate(self.criteria_score):
            c = customized_criteriaList[i]
            if(float(my_score) < c.min_condition):
                return False
        return True

    def evaluate(self, score):
        self.pr_score = float(score.get())
        self.score = 0.0
        for i, my_score in enumerate(self.criteria_score):
            c = customized_criteriaList[i]
            self.score += c.rate/c.ratesum * (float(my_score) / c.perfect)
        self.score = 70 * self.score + 0.3 * self.pr_score
        # 여기서 정렬
        tempdq = Deque()
        if passApplicants.head.rlink != '\0':
            frt = passApplicants.head.rlink.data.score - self.score
            end = self.score - passApplicants.tail.data.score
        else:
            frt = 1
            end = 0
        if frt > end:  # 가장 앞과의 차이가 더 큼 -> 뒤에서 빼서 자리 찾기
            while(passApplicants.tail != '\0' and self.score > passApplicants.tail.data.score):  # 뒤에서 빼서 자리 찾아 넣기
                tempdq.enqueue_front(passApplicants.dequeue_rear())
            passApplicants.enqueue_rear(self)
            while not(tempdq.is_empty()):
                passApplicants.enqueue_rear(tempdq.dequeue_front())

        else:  # 가장 뒤와의 차이가 더 크거나 앞과 뒤의 차이가 같음 -> 앞에서 빼서 자리 넣기.
            while(passApplicants.head.rlink and self.score < passApplicants.head.rlink.data.score):  # 앞에서 빼서 자리 찾아 넣기
                tempdq.enqueue_rear(passApplicants.dequeue_front())
            passApplicants.enqueue_front(self)
            while not(tempdq.is_empty()):
                passApplicants.enqueue_front(tempdq.dequeue_rear())

        # 선발인원 초과시 탈락시키기
        if passApplicants.size > selectNum:
            failApplicants.enqueue_front(passApplicants.dequeue_rear())

        # 덱 업데이트
        updateApplicantsDeque()
        updateFailApplicants()
        updatePassApplicants()

# 창 닫기


def quitProgram():
    root.destroy()

# CSV 업로드 / 선발 인원 & 블라인드 페이지


def uploadCSV():

    def UploadAction():
        global data, writer, newfile, customized_criteriaList, criteriaN
        newfile = open("new-list-applicants.csv", "w",
                       encoding="euc-kr", newline='')  # 새파일
        writer = csv.writer(newfile)
        filename = filedialog.askopenfilename()
        filement = Label(upload, text="OK!")
        filement.place(x=372, y=30)
        try:
            csvfile = open(filename, "r", encoding='utf-8', newline='')  # 읽을파일
        except:
            csvfile = open(filename, "r", encoding='euc-kr',
                           newline='')  # 읽을파일
        my_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_csv:
            print(row)  # 디버깅용
            writer.writerow(row)  # 새파일에 복사해두고
            data.append(row)  # 쓸 리스트에다도 넣음
        csvfile.close()
        customized_criteriaList = [Criteria(name)
                                   for name in data[0][4:]]  # 기준리스트 값넣기
        criteriaN = len(customized_criteriaList)
        data = data[1:]
        # 난 사실 터미널창에 filename(파일명) 출력하는 것보단 tkinter에서 출력을 하고싶은데.. 어렵네
        # -> 완료!

    def getData():
        global selectNum, is_blind
        selectNum = int(combobox1.get())
        if combobox2.current() == 0:  # Yes
            is_blind = True
        showCriteria()  # 기준정보 입력창 띄움

    def quit():
        upload.destroy()
        updateApplicantsDeque()
        updateFailApplicants()
        updatePassApplicants()
    global cnt
    cnt = 0  # 몇번째 기준인지

    upload = Tk()
    upload.title("명단 업로드 / 선발 인원 & 블라인드")
    upload.geometry("500x430+1000+200")

    uploadment = Label(upload, text="지원자 파일을 업로드하세요",
                       font=('Malgun Gothic', 12))
    uploadment.place(x=105, y=30)
    uploadbtn = tk.Button(upload, text='업로드',
                          command=UploadAction, fg='white', bg='gray')
    uploadbtn.place(x=320, y=30)

    # CSV 파일 업로드 후
    limitnum = Label(upload, text="선발 인원", font=('Malgun Gothic', 12))
    limitnum.place(x=100, y=90)
    combobox1 = ttk.Combobox(upload, textvariable=str, width=10)
    combobox1['value'] = [str(i) for i in range(1, 21)]
    combobox1.current(0)
    combobox1.place(x=280, y=90)

    blind = Label(upload, text="블라인드 선발", font=('Malgun Gothic', 12))
    blind.place(x=100, y=120)
    combobox2 = ttk.Combobox(upload, textvariable=str, width=10)
    combobox2['value'] = ('Yes', 'No')
    combobox2.current(0)
    combobox2.place(x=280, y=120)

    updatebtn = Button(upload, text="반영하기", fg='white',
                       bg='gray', width=50, command=getData)
    updatebtn.place(x=70, y=170)

    # CSV 파일 업로드 후 (파일과 관련한 설정 - 만점 / 최소점수 / 평가 반영 비율)
    # 여기는 이제 파일을 성공적으로 불러들이면 알고리즘 반영에서 수정해야 할 거 같아 변수명도 일단 별로지만 이렇게 할게 (ment 등등...)
    def getPerfect(score):
        global customized_criteriaList
        customized_criteriaList[cnt].perfect = float(score.get())

    def getMinCondition(minscore):
        global customized_criteriaList
        customized_criteriaList[cnt].min_condition = float(minscore.get())

    def getRate(combobox):
        global Criteria, customized_criteriaList, cnt, applicantsDeque, failApplicants
        cc = customized_criteriaList[cnt]
        cc.rate = int(combobox.get())
        Criteria.ratesum += cc.rate
        cnt += 1
        print(
            f"{cc.name}: {cc.perfect}점 만점, 최소점수{cc.min_condition}점, 반영비율 {cc.rate}/{Criteria.ratesum}")
        if(cnt == criteriaN):  # 파일에 있던 지원자들 덱에 삽입
            for c in data:
                app = Applicant(c[0], c[1], c[2], c[3], c[4:])
                # app.over_perfect() ->enqueue에서 할거같음
                if app.is_qualified() == True:
                    applicantsDeque.enqueue_rear(app)
                else:
                    failApplicants.enqueue_rear(app)
            updateApplicantsDeque()
            updateFailApplicants()
            quit()
        else:
            showCriteria()

    def showCriteria():
        global cnt
        cc = customized_criteriaList[cnt]
        ment = Label(upload, text=f"({cc.name}) 만점을 입력하세요", font=(
            'Malgun Gothic', 12))
        ment.place(x=20, y=250)
        score = Entry(upload)
        score.place(x=350, y=250, width=50)
        btn = Button(upload, text="입력", command=lambda: getPerfect(score))
        btn.place(x=410, y=250, height=20)

        ment = Label(upload, text=f"({cc.name}) 최소점수를 입력하세요", font=(
            'Malgun Gothic', 12))
        ment.place(x=20, y=280)
        minscore = Entry(upload)
        minscore.place(x=350, y=280, width=50)
        btn = Button(upload, text="입력",
                     command=lambda: getMinCondition(minscore))
        btn.place(x=410, y=280, height=20)

        ment = Label(upload, text=f"({cc.name}) 평가 반영 비율", font=(
            'Malgun Gothic', 12))
        ment.place(x=20, y=310)
        combobox = ttk.Combobox(upload, textvariable=str, width=10)
        combobox['value'] = [str(i*10) for i in range(11)]
        combobox.current(0)
        combobox.place(x=350, y=310)

        # 비율받기 -> 기준 변경/창 닫기
        closebtn = Button(upload, text="완료", command=lambda: getRate(combobox),
                          fg='white', bg='gray')  # 비율받고 다시 다음기준으로 바꿈
        closebtn.place(x=230, y=370)

    # 기준별 정보들 입력받기

    upload.mainloop()

# 지원자 추가 페이지


def appendPerson():
    global applicantsDeque, failApplicants

    def add():
        inp = new.get()
        a = inp[inp.index('(')+1:inp.index(')')].split(',')
        applicant = Applicant(a[0], a[1], a[2], a[3], a[4:])
        writer.writerow(a)
        if applicant.is_qualified() == True:
            applicantsDeque.enqueue_rear(applicant)
        elif applicant.is_qualified() == False:
            print("지원자가 최소조건을 만족하지 못했습니다.")
            write2 = Label(
                addPerson, text="지원자가 최소조건을 만족하지 못했습니다.", font=fontstyle)
            write2.place(x=130, y=20)
            failApplicants.enqueue_rear(applicant)
        updateApplicantsDeque()
        updateFailApplicants()

    def quit():
        addPerson.destroy()

    addPerson = Tk()
    addPerson.title("지원자 추가")
    addPerson.geometry("500x230+1000+300")
    addPerson.resizable(False, False)

    fontstyle = tkFont.Font(
        addPerson, family="Malgun Gothic", size=12, weight="bold")
    text = "[양식] +(학번,이름,학과,자기소개"
    for c in customized_criteriaList:
        text += f",{c.name}"
    text += ")"
    write = Label(
        addPerson, text=text, font=fontstyle)
    write.place(x=100, y=20)

    new = Entry(addPerson)
    new.place(x=35, y=100, width=380, height=60)
    btn = Button(addPerson, text="입력", command=add, fg='white', bg='gray')
    btn.place(x=435, y=100, height=60)

    closebtn2 = Button(addPerson, text="완료", command=quit,
                       fg='white', bg='gray')
    closebtn2.place(x=230, y=180)

    addPerson.mainloop()

# 지원자 평가 페이지


def evaluatePerson():
    global applicant,flag
    flag = 0
    def evaluateapp(score):
        global applicant,flag
        if(flag == 0):
            applicant.evaluate(score)
        flag = 1

    def quit():
        evaluate.destroy()

    applicant = applicantsDeque.dequeue_front()
    evaluate = Tk()
    evaluate.title("지원자 평가")
    evaluate.geometry("500x370+1000+250")
    evaluate.resizable(False, False)

    fontStyle = tkFont.Font(
        evaluate, family="Malgun Gothic", size=12, weight="bold")

    person = Label(evaluate, text="지원자 정보는 아래와 같습니다", font=fontStyle)
    person.place(x=130, y=20)

    fontStyle = tkFont.Font(evaluate, family="Malgun Gothic", size=12)

    if applicantsDeque.is_empty():
        blah1 = Label(
            evaluate, text="최소조건을 만족한 지원자 중 \n평가되지 않은 지원자가 없습니다.", font=fontStyle)
        blah1.place(x=120, y=100)
    else:
        blah2 = Label(evaluate, text=applicant.print_applicant(
            is_blind), font=fontStyle, wrap=370)
        blah2.place(x=70, y=100)

    ment = Label(evaluate, text="정성 평가 점수 (만점 100)", font=fontStyle)
    ment.place(x=80, y=240)
    score = Entry(evaluate)
    score.place(x=300, y=240, width=50)
    btn = Button(evaluate, text="입력", command=lambda: evaluateapp(score), fg='white', bg='gray')
    btn.place(x=360, y=240, height=20)

    closebtn3 = tk.Button(evaluate, text="완료",
                          command=quit, fg='white', bg='gray')
    closebtn3.place(x=230, y=320)

    evaluate.mainloop()


# 덱, 전역변수들 초기화
applicantsDeque = Deque()
passApplicants = Deque()
failApplicants = Deque()
data = []
is_blind = False
writer = None
newfile = None
cnt = 0
customized_criteriaList = []

# 메인 페이지
root = Tk()
root.title("지원자 관리 모듈")
root.geometry("1000x500+80+170")
root.resizable(False, False)

fontstyle = tkFont.Font(root, family="Courier", size=20, weight="bold")
label = Label(root, text="지원자 관리 모듈", font=fontstyle)
label.place(x=400, y=20)

fontStyle = tkFont.Font(root, family="Malgun Gothic", size=12)

btn1 = Button(root, text="명단 업로드", font=('Malgun Gothic', 12),
              command=uploadCSV, fg='white', bg='black')
btn1.place(x=210, y=75, width=130, height=30)

btn2 = Button(root, text="지원자 추가", font=('Malgun Gothic', 12),
              command=appendPerson, fg='white', bg='black')
btn2.place(x=360, y=75, width=130, height=30)

btn3 = Button(root, text="지원자 평가", font=('Malgun Gothic', 12),
              command=evaluatePerson, fg='white', bg='black')
btn3.place(x=510, y=75, width=130, height=30)

btn3 = Button(root, text="프로그램 종료", font=('Malgun Gothic', 12),
              command=quitProgram, fg='white', bg='black')
btn3.place(x=660, y=75, width=130, height=30)


# 평가 X 덱 / 탈락자 덱 / 평가 O 덱

fontstyle2 = tkFont.Font(root, family="Malgun Gothic", size=12, weight="bold")

deque1 = Label(root, text="평가 전 지원자 DEQUE", font=fontstyle2)
deque1.place(x=140, y=180)

# 덱 업데이트


def updateApplicantsDeque():
    frame1 = tk.Frame(root)
    scrollbar1 = tk.Scrollbar(frame1)
    scrollbar1.pack(side="right", fill="y")
    listbox = tk.Listbox(frame1, yscrollcommand=scrollbar1.get())
    applist = applicantsDeque.print_deque()
    for i, app in enumerate(applist):
        listbox.insert(i, app)
    listbox.pack(side="left")
    scrollbar1["command"] = listbox.yview
    frame1.place(x=140, y=230)


updateApplicantsDeque()


deque2 = Label(root, text="탈락 지원자 DEQUE", font=fontstyle2)
deque2.place(x=420, y=180)


def updateFailApplicants():
    frame2 = tk.Frame(root)
    scrollbar2 = tk.Scrollbar(frame2)
    scrollbar2.pack(side="right", fill="y")
    listbox = tk.Listbox(frame2, yscrollcommand=scrollbar2.get())
    applist = failApplicants.print_deque()
    for i, app in enumerate(applist):
        listbox.insert(i, app)
    listbox.pack(side="left")
    scrollbar2["command"] = listbox.yview
    frame2.place(x=420, y=230)


updateFailApplicants()


deque3 = Label(root, text="평가 후 지원자 DEQUE", font=fontstyle2)
deque3.place(x=680, y=180)


def updatePassApplicants():
    frame3 = tk.Frame(root)
    scrollbar3 = tk.Scrollbar(frame3)
    scrollbar3.pack(side="right", fill="y")
    listbox = tk.Listbox(frame3, yscrollcommand=scrollbar3.get())
    applist = passApplicants.print_deque()
    for i, app in enumerate(applist):
        listbox.insert(i, app)
    listbox.pack(side="left")
    scrollbar3["command"] = listbox.yview
    frame3.place(x=680, y=230)


updatePassApplicants()

root.mainloop()