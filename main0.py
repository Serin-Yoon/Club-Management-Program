## 외부 모듈 import하기 ##
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import codecs
import csv

## 사용자 정의 모듈 import하기 (1. 지원자 관리 모듈 2. 업무 관리 모듈) ##
#import main1 as m1 
#import main2 as m2 
from functools import partial

# 지원자 관리 모듈
def move1():
    import main1 as m1

def move2() :
    import main2 as m2

# 메인 페이지

main0 = Tk()
main0.title("동아리 관리 프로그램")
main0.geometry("1000x500+300+150")
main0.resizable(False, False)

fontstyle1 = tkFont.Font(main0, family="Courier", size=30, weight="bold")
title = Label(main0, text=" 댁은 덱을 이용하셔야 합니다 ", font=fontstyle1, fg="white", bg="black")
title.place(x=230, y=20)

fontstyle2 = tkFont.Font(main0, family="Courier", size=12, weight="bold")
title2 = Label(main0, text="― 덱(Deque)을 활용한 동아리 관리 프로그램", font=fontstyle2)
title2.place(x=344, y=77)

wall1 = PhotoImage(file = "applicant.png")
wall1_label = Label(main0, image = wall1)
wall1_label.place(x=250, y=120)
wall2 = PhotoImage(file = "task.png")
wall2_label = Label(main0, image = wall2)
wall2_label.place(x=550, y=135)

fontstyle3 = tkFont.Font(main0, family="Malgun Gothic", size=17, weight="bold")

first = tk.Button(main0, text='1. 지원자 관리', font=fontstyle3, bg="gray80", command=move1)
first.place(x=290, y=370)
second = tk.Button(main0, text='2. 업무 관리', font=fontstyle3, bg="gray80", command=move2)
second.place(x=570, y=370)


fontstyle4 = tkFont.Font(main0, family="Malgun Gothic", size=10, weight="bold", slant="italic")
madeby = Label(
    main0, text=" Made By. 성균관대학교 컴퓨터교육과 | 김서진, 심규현, 양동석, 윤세린, 장미", font=fontstyle4)
madeby.place(x=270, y=460)

main0.mainloop()