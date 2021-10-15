import re, copy, datetime, read_excel
time_schedule = {'08:00 - 09:30':1,'09:40 - 11:10':2,'11:30 - 13:00':3,'13:10 - 14:40':4,'15:00 - 16:30':5,'16:40 - 18:10':6,'18:20 - 19:50':7}
time_schedule1 = {value:key for key, value in time_schedule.items()}
weekday_list = {"Понедельник":1,"Вторник":2,"Среда":3,"Четверг":4,"Пятница":5,"Суббота":6,"Воскресенье":7}
weekday_list1 = {value:key for key, value in weekday_list.items()}


def read_weekday(weekday):
    if weekday_list1.get(datetime.datetime.today().isoweekday()) == weekday:
        liva_weekday = " сегодня"
    elif weekday_list1.get(datetime.datetime.today().isoweekday()+1) == weekday:
        liva_weekday = " завтра"
    else:
        liva_weekday = " " + weekday
    return liva_weekday


def merge(Mschedule, Msubstitutions, Mtime, schedule):
    print('---------------------------------------------------')
    
    print('СЛИЯНИЕ Время:',Mtime, 'Расписание', Mschedule, 'Замены', Msubstitutions, 'День недели', schedule, 'Сегодня', weekday_list1.get(datetime.datetime.today().isoweekday()), 'liva_weekday', read_weekday(schedule))
    to_day_or_not_today = read_weekday(schedule)
    w = []
    time = []
    patter = r'[0-9][0-9]\:[0-9][0-9]\s\-\s[0-9][0-9]\:[0-9][0-9]'
    for item in Msubstitutions:
        #print(item[:1])
        for item2 in Mschedule:
            if item2[:1] == item[:1]:
                Mschedule[Mschedule.index(item2)] = item2[:1] + '. Empty'
                time.append(item2[:1] + (f'. ({(re.search(patter, item2)).group(0) })' if type(re.search(patter, item2)) != type(None) else ""))

    print('Расписание:', Mschedule)
    print('Замены:', Msubstitutions)

    print('Время:', time)
    if len(Msubstitutions) != 0:
        x = sorted([
            x for x in Mschedule+Msubstitutions
            if x[0].isdigit() and not 'Empty' in x[3:]
            ], key=lambda x: int(x[0]))
        for x in x: w.append(x)
    else:
        print("Замен нет")
        w.clear()
        w = Mschedule.copy()

    print(w)


    result_time = copy.deepcopy(w) #создаем копию списка расписания
    print('Первая пара, номер',result_time[0][0])
    print('Вторая пара, номер',result_time[1][0])
    for i in range(0,5):
        if result_time[i][3:] != 'Н/Б':
            time_one = str(result_time[i][0])[0]
            break
    #time_one = str(result_time[0][0])[0]
    time_one = str(time_schedule1.get(int("".join(time_one.split()))))[:5]
    #узнаем время
    for item in result_time:
        if result_time[result_time.index(item)][3:6] != 'Н/Б':
            print(result_time[result_time.index(item)])
            result_time[result_time.index(item)] = '('+time_schedule1.get(int(item[:1]))+')'
        else:
            result_time[result_time.index(item)] = ''
        
    print(result_time)
        #= [item[1] for item in result_time]
    print('В колледж в', time_one)


    for item in time:
        #print(item[:1])
        for item2 in w:
            if item2[:1] == item[:1]:
                w[w.index(item2)] = "&#128260;" + item2[:1] + f'. {item2[3:]} ' + item[3:]
    """
    if Mtime != 'Пусто':
        print(Mtime)
        w = [''.join(Mtime)] + ['\n'] + w
    else:
        patter = r'[0-9][0-9]\:[0-9][0-9]'
        Mtime = (re.search(patter, w[0])).group(0)
        if type(Mtime) != type(None) and Mtime != 'Пусто':
            w = ['В колледж '] + [''.join(Mtime)] + ['\n'] + w
    """

    print('СЛИЯНИЕ:', w)

    if w == []:
        return 'Слияние не удалось'


    if len(w) == len(result_time):
        w = [val for pair in zip(w, result_time) for val in pair]
    else:
        return 'Размер расписания не соответсутет размеру времени'
    print('СЛИЯНИЕ:', w)
    w = [f'\n{j}' for j in w]
    w = [f'\n\n&#128341;{to_day_or_not_today.title()} в ' + time_one] + w + ["\n"]
    w = ['Расписание на' + to_day_or_not_today] + w
    return w

