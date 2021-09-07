import re

def merge(Mschedule, Msubstitutions, Mtime, to_day_or_not_today):
    print('---------------------------------------------------')
    print('СЛИЯНИЕ Время:',Mtime)
    w = []
    time = []
    patter = r'[0-9][0-9]\:[0-9][0-9]\s\-\s[0-9][0-9]\:[0-9][0-9]'
    for item in Msubstitutions:
        #print(item[:1])
        for item2 in Mschedule:
            if item2[:1] == item[:1]:
                Mschedule[Mschedule.index(item2)] = item2[:1] + '. Empty'
                time.append(item2[:1] + f'. ({(re.search(patter, item2)).group(0) if type(re.search(patter, item2)) != type(None) else "Время узнать не удалось"})')

    print('TEST:', Mschedule)
    print('Время:', time)
    x = sorted([
        x for x in Mschedule+Msubstitutions
        if x[0].isdigit() and not 'Empty' in x[3:]
        ], key=lambda x: int(x[0]))
    for x in x: w.append(x)


    for item in time:
        #print(item[:1])
        for item2 in w:
            if item2[:1] == item[:1]:
                w[w.index(item2)] = item2[:1] + f'. {item2[3:]} ' + item[3:]

    if Mtime != 'Пусто':
        print(Mtime)
        w = [''.join(Mtime)] + ['\n'] + w
    else:
        patter = r'[0-9][0-9]\:[0-9][0-9]'
        Mtime = (re.search(patter, w[0])).group(0)
        if type(Mtime) != type(None) and Mtime != 'Пусто':
            w = ['В колледж '] + [''.join(Mtime)] + ['\n'] + w

    print('СЛИЯНИЕ:', w)

    if w == []:
        return 'Слияние не удалось'

    w = [f'\n {j}' for j in w]
    return w