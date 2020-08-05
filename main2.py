## 외부 모듈 import하기 ##
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
## 사용자 정의 모듈 import하기 ##
import manager_manage as m
import task_manage as t
from functools import partial


def man_add_by_input_form(w1):

    l1 = Label(w1, text="학번", font=('Malgun Gothic', 12))
    _id = Entry(w1, width=10)
    l2 = Label(w1, text="이름", font=('Malgun Gothic', 12))
    name = Entry(w1, width=10)
    l3 = Label(w1, text="운영진인가요? (y/n)", font=('Malgun Gothic', 12))
    is_speciality = Entry(w1, width=10)
    submit_btn = Button(w1, width=10, text="추가하기", fg='white', bg='black',
                        command=lambda: m.add_by_input(_id, name, is_speciality))
    l1.place(x=200, y=120)
    _id.place(x=260, y=120)
    l2.place(x=360, y=120)
    name.place(x=420, y=120)
    l3.place(x=520, y=120)
    is_speciality.place(x=680, y=120)
    submit_btn.place(x=800, y=120)

def onclick1():
    w1 = Tk()
    w1.title("Manger Input")
    w1.geometry("1000x200+100+168")
    w1.resizable(False, False)
    add_man_btn_y = Button(w1, text="파일로 입력하기", fg='white', bg='gray', height = 2,
                           command=lambda: m.add_by_file())
    add_man_btn_n = Button(w1, text="직접 입력하기", fg='white', bg='gray', height = 2,
                           command=lambda: man_add_by_input_form(w1))
    add_man_btn_y.place(x=400, y=50)
    add_man_btn_n.place(x=550, y=50)


def task_add_by_input_form(w2):

    l1 = Label(w2, text="이름", font=('Malgun Gothic', 12))
    work_name = Entry(w2, width=10)
    l2 = Label(w2, text="중요도", font=('Malgun Gothic', 12))
    work_level = Entry(w2, width=10)
    submit_btn = Button(w2, width=10, text="추가하기", fg='white', bg='black',
                        command=lambda: [t.add_by_input(work_name.get(), work_level.get()), onclick3()])
    l1.place(x=100, y=120)
    work_name.place(x=160, y=120)
    l2.place(x=260, y=120)
    work_level.place(x=320, y=120)
    submit_btn.place(x=440, y=120)


def onclick2():
    w2 = Tk()
    w2.title("Task Input")
    w2.geometry("600x200+100+168")
    add_task_btn_y = Button(w2, text="파일로 입력하기", fg='white', bg='gray', height = 2,
                            command=lambda: [t.add_by_file(), onclick3()])
    add_task_btn_n = Button(w2, text="직접 입력하기", fg='white', bg='gray', height = 2,
                            command=lambda: [task_add_by_input_form(w2), onclick3()])
    add_task_btn_y.place(x=180, y=50)
    add_task_btn_n.place(x=330, y=50)


w3 = Tk()
w3.title("Tasks List")
w3.geometry("300x400+100+300")


def _clear(wwww):
    list_ = wwww.slaves()
    print(list_)
    if len(list_) == 0:
        list_ = wwww.grid_slaves()
    for l in list_:
        l.destroy()


def onclick3():
    _clear(w3)
    ts = t.Deque.print_deque2(t.works_deque)
    lb = Label(w3, text=ts, font=('Malgun Gothic', 12), pady=10)
    lb.pack()
    reset_btn = Button(w3, text="새로고침", fg='white', bg='black', width=20, font=('Malgun Gothic', 10), command=lambda: onclick3())
    reset_btn.place(x=80, y=350)


def onclick4():
    t.give_tasks()
    onclick3()
    onclick5()


doing_task = Tk()
doing_task.title("Task on Process")
doing_task.geometry("700x400+400+300")


def onclick5():
    _clear(doing_task)
    print("cleared")
    col = 10
    num = 0
    buttons = []
    varietys = []
    click = []

    for i in range(len(m.manager_list)):
        man = m.manager_list[i]
        col += 1
        if man.task == None:
            l10 = Label(doing_task, text=f"                    ▶ {man}는 쉬는 중..", font=(
                'Malgun Gothic', 12), padx=10, pady=10)
            l10.grid(row=col, column=0)
            buttons.append(None)
        else:
            l10 = Label(doing_task, text=f"                    ▶ {man}는 {man.task}하는 중..", font=(
                'Malgun Gothic', 12), padx=10, pady=10)
            l10.grid(row=col, column=0)
            buttons.append(Button(doing_task, width=10, text=" 임무 완료!", fg='white', bg='gray',
                                  command=partial(work_finish, num, buttons, click)))
            buttons[num].grid(row=col, column=1)
        num += 1
    for i in buttons:
        click.append(0)

    button = Button(doing_task, text="Submit", fg='white', bg='black', width=20, font=('Malgun Gothic', 10),
                    overrelief="solid", command=lambda: [show(click), onclick5()])
    button.place(x=260 ,y=350)


def work_finish(num, buttons, click):
    print(num)
    print(buttons)
    click[num] = 1
    print(click)
    buttons[num].grid_forget()
    m.manager_list[num].task = None


def show(click):

    number = 0
    number2 = 0
    name = []
    more = []
    button = []
    manage_list = []
    w7 = Tk()
    w7.title("Give more tasks")
    w7.geometry("470x400+900+300")
    for i in click:
        if i == 1:
            manage_list.append(m.manager_list[number])
            name.append(Label(w7, text=m.manager_list[number], padx=20, pady=10, font=(
                'Malgun Gothic', 12)))
            name[number2].grid(row=number2, column=0)
            #Btn=(Button(w7, width=10, text="추가하기",command=partial(t.fin_task_tk,m.manager_list[number2])))
            more.append(Button(w7, width=10, text="추가하기", fg='white', bg='gray', command=partial(
                after_show, number2, more, number, w7)))
            more[number2].grid(row=number2, column=1)
            number2 += 1
        number += 1
    print("click")
    print(click)

    if not 1 in click:
        l10 = Label(w7, text="업무를 추가할 사람이 없습니다!", font=('Malgun Gothic', 12))
        l10.grid(row=0, column=0)

    print(more)
    onclick5()


def after_show(number2, more, number, w7):
    more[number2].grid_forget()
    if t.works_deque.is_empty():
        l10 = Label(w7, text=f"{m.manager_list[number]}에게 부여할 일이 없습니다!", font=(
            'Malgun Gothic', 12))
        l10.grid(row=number2, column=2)
    else:
        if m.manager_list[number].is_speciality:
            task = t.works_deque.dequeue_rear()
        else:
            task = t.works_deque.dequeue_front()
        m.manager_list[number].task = task
        l10 = Label(
            w7, text=f"{m.manager_list[number]}에게 {task}를 부여합니다.", font=('Malgun Gothic', 12))
        l10.grid(row=number2, column=2)
    onclick5()
    onclick3()


def all_fin_task_tk(more, manage_list):
    number2 = 0
    print("hello>")
    print(more)
    for i in manage_list:
        t.fin_task_tk(i, more[number2])
        number2 += 1


window = Tk()


def main():

    window.title("User Management")
    window.geometry("1000x100+100+170")
    window.resizable(False, False)

    fontstyle = tkFont.Font(window, family="Courier", size=20, weight="bold")
    title = Label(window, text="업무 분담 모듈", font=fontstyle)
    title.place(x=410, y=10)

    btn1 = Button(window, text="운영진 추가하기", command=onclick1,
                  fg='white', bg='black', width=20, font=('Malgun Gothic', 11))
    btn1.place(x=5, y=50)
    #btn1.grid(row=0, column=0, padx = 5, pady = 5)
    btn2 = Button(window, text="업무 추가하기", command=onclick2,
                  fg='white', bg='black', width=20, font=('Malgun Gothic', 11))
    btn2.place(x=205, y=50)
    #btn2.grid(row=0, column=1, padx = 5, pady = 5)
    btn3 = Button(window, text="남은 업무 보기", command=onclick3,
                  fg='white', bg='black', width=20, font=('Malgun Gothic', 11))
    btn3.place(x=405, y=50)
    #btn3.grid(row=0, column=2, padx = 5, pady = 5)
    btn4 = Button(window, text="업무 분배하기", command=onclick4,
                  fg='white', bg='black', width=20, font=('Malgun Gothic', 11))
    btn4.place(x=605, y=50)
    #btn4.grid(row=0, column=3, padx = 5, pady = 5)
    btn5 = Button(window, text="업무 진행 상황 보기", command=onclick5,
                  fg='white', bg='black', width=20, font=('Malgun Gothic', 11))
    btn5.place(x=805, y=50)
    #btn5.grid(row=0, column=4, padx = 5, pady = 10)

    window.mainloop()


main()
doing_task = None
