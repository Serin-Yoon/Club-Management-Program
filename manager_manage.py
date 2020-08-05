import codecs
import task_manage as t


class Managers:
    def __init__(self, _id, name, is_speciality):
        self._id = _id
        self.name = name
        self.is_speciality = is_speciality
        self.task = None

    def __str__(self):
        return self.name


manager_list = []


def print_managers(manager):
    print(
        f"학번 : {manager._id}, 이름 : {manager.name}, 간부 여부 : {manager.is_speciality}")


def add_by_file():
    filename = "list-managers.csv"
    csv = codecs.open(filename, "r", "euc_kr").read()

    data = []
    rows = csv.split("\r\n")
    for row in rows:
        if row == "":
            continue
        cells = row.split(",")
        data.append(cells)

    data = data[1:]

    print("다음 운영진들을 추가합니다.")
    for m in data:
        manager_list.append(Managers(m[0], m[1], m[2]))
        print_managers(manager_list[-1])


def add_by_input():
    while 1:
        _id = input("새 운영진의 학번을 입력하세요. >> ")
        name = input("새 운영진의 이름을 입력하세요. >> ")
        is_speciality = 1 if (input("새 운영진은 간부인가요? (y/n) >> ") == 'y') else 0
        manager_list.append(Managers(_id, name, is_speciality))
        print_managers(manager_list[-1])
        # csv 파일에도 더해서 수정하는 코드가 있으면 좋을듯!
        _continue = input("계속 추가하시겠습니까? (y/n)")
        if (_continue == 'y'):
            continue
        else:
            print("메인 화면으로 돌아갑니다.")
            break


def find_mem(mem):
    for i in range(len(manager_list)):
        if mem == manager_list[i].name:
            return manager_list[i]
    return None
