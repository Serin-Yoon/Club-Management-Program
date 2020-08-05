import codecs

import manager_manage as m


class Node:
    def __init__(self, value):  # 생성자
        self.data = value  # data
        self.llink = '\0'  # llink
        self.rlink = '\0'  # rlink


class Deque:
    def __init__(self):  # 생성자
        head = Node("trash")  # 헤드포인터 역할을 해줄 노드 생성
        self.head = head  # self.head: 덱의 head 포인터. 첫번째 노드를 가리킴.
        self.tail = head  # self.tail: 덱의 가장 마지막 노드
        self.size = 0  # 덱의 크기(노드의 개수)를 나타내는 변수

    def is_empty(self):
        if self.head.rlink == '\0':
            return True
        else:
            return False

    def enqueue_front(self, data):
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
        new_node = Node(data)  # 새로운 노드 생성
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
        else:
            tmp = self.tail.data  # 마지막 원소의 값 저장
            self.tail = self.tail.llink  # 마지막에서 두번째 원소를 마지막 원소로 저장
            self.tail.rlink = '\0'  # 새로운 마지막 원소의 우링크 NULL로 다시 바꾸기
            self.size = self.size - 1  # size 변수 관리
            return tmp

    def print_deque(self):  # 덱 출력
        current = self.head.rlink
        if self.is_empty() == True:
            print("empty deque")
        else:
            for i in range(self.size):  # 차례대로 덱의 노드 값 출력
                print(f"{current.data}")
                current = current.rlink

    def print_deque2(self):  # 덱 출력
        trav_str = ''
        current = self.head.rlink
        if self.is_empty() == True:
            return "일이 없습니다."
        print("[중요도] 업무명")
        for i in range(self.size):
            trav_str += f"[{current.data.n_important}] {current.data.toDo} \n"
            current = current.rlink
        return trav_str


class Tasks:
    def __init__(self, toDo, n_important):
        self.toDo = toDo
        self.n_important = int(n_important)

    def __str__(self):
        return f"[{self.n_important}] {self.toDo} "


works_deque = Deque()


def sort_deq(work):
    save_data = []
    while 1:
        if work.n_important <= works_deque.head.rlink.data.n_important:
            works_deque.enqueue_front(work)
            break
        elif work.n_important >= works_deque.tail.data.n_important:
            works_deque.enqueue_rear(work)
            break
        else:
            save_data.append(works_deque.dequeue_front())

    save_data.reverse()
    for i in save_data:
        works_deque.enqueue_front(i)


def add_by_file():
    filename = "list-tasks.csv"
    csv = codecs.open(filename, "r", "euc_kr").read()

    data = []
    rows = csv.split("\r\n")
    for row in rows:
        if row == "":
            continue
        cells = row.split(",")
        data.append(cells)

    data = data[1:]

    for t in data:
        if(works_deque.is_empty()):
            works_deque.enqueue_front(Tasks(t[0], t[1]))

        else:
            sort_deq(Tasks(t[0], t[1]))


def add_by_input(work_name, work_level):
    if(works_deque.is_empty()):
        works_deque.enqueue_front(Tasks(work_name, work_level))
    else:
        sort_deq(Tasks(work_name, work_level))


def give_tasks():
    for i in range(len(m.manager_list)):
        man = m.manager_list[i]
        if man.task is not None:
            continue
        works_deque.print_deque()
        if(works_deque.is_empty()):
            print('일이 없다')
            break
        if(int(man.is_speciality)):
            print("운영진")
            tmp = works_deque.dequeue_rear()
            man.task = tmp
        else:
            print("안 운영진")
            tmp = works_deque.dequeue_front()
            man.task = tmp
        print(f"{man}에게 {man.task}를 부여합니다.")


def show_tasks():

    for i in range(len(m.manager_list)):
        man = m.manager_list[i]
        if man.task == None:
            print(f"{man}은(는) 쉬는 중..")

        else:
            print(f"{man}은(는) {man.task}하는 중..")


def fin_task():
    print("누구의 업무가 완료되었습니까?")
    show_tasks()
    while True:
        man = input(">> ")
        man = m.find_mem(man)
        if man == None:
            print("다시 입력해 주세요")
        else:
            if man.task == None:
                print(f"{man}은(는) 쉬는 중이었습니다")
            man.task = None
            print(f"{man}에게 일을 더 맡기시겠습니까?")
            cont = input(">> ")
            if cont == 'y' or cont == 'Y':
                if(works_deque.is_empty()):
                    print('일이 없다')
                    break
                if(int(man.is_speciality)):
                    tmp = works_deque.dequeue_rear()
                    man.task = tmp
                else:
                    tmp = works_deque.dequeue_front()
                    man.task = tmp
                print(f"{man}에게 {man.task}를 부여합니다.")
                break
            else:
                print("종료합니다.")
                break


def fin_task_tk(man):
    print(f"{man}에게 일을 더 맡기시겠습니까?")
    cont = 'y'

    if cont == 'y' or cont == 'Y':
        if(works_deque.is_empty()):
            print('일이 없다')
        else:
            if(int(man.is_speciality)):
                tmp = works_deque.dequeue_rear()
                man.task = tmp
            else:
                tmp = works_deque.dequeue_front()
                man.task = tmp
            print(f"{man}에게 {man.task}를 부여합니다.")
    else:
        print("종료합니다.")
