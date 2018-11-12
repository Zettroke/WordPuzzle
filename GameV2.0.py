from tkinter import Button, Tk, Frame, StringVar, Label, Menu, Toplevel, SUNKEN, Scale, HORIZONTAL
import WordGen2
from random import randint
from os.path import join
import sys
import os
base_dir = '.'
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS

if not os.path.exists("config.cnf"):
    open("config.cnf", "w").write("8 0 0 0 0 0 0 0 0 0 0")



def unbindall():
    for i in letters:
        for j in i:
            j.unbind("<Button-1>")


def bindall():
    for i in letters:
        for j in i:
            if not j.lock and j not in word.l:
                j.bind("<Button-1>", press1)


def binding(widget):
    temp = []
    try:
        temp.append(letters[widget.posx][widget.posy+1])
    except Exception:
        pass
    try:
        temp.append(letters[widget.posx+1][widget.posy])
    except Exception:
        pass
    try:
        temp.append(letters[widget.posx][widget.posy-1])
    except Exception:
        pass
    try:
        temp.append(letters[widget.posx-1][widget.posy])
    except Exception:
        pass
    for i in temp:
        if not i.lock and i not in word.l:
            i.bind("<Button-1>", press1)


def press1(event):
    data.timergo = True
    if not data.bonuslevel:
        unbindall()
        event.widget.bind("<Button-1>", press2)
        event.widget.configure(bg=color.take())
        word.put(event.widget)
        check()
        binding(event.widget)
    else:
        unbindall()
        bindall()
        event.widget.bind("<Button-1>", press2)
        event.widget.configure(bg=color.take())
        word.put(event.widget)
        check()


def press2(event):
    if not data.bonuslevel:
        unbindall()
        event.widget.bind("<Button-1>", press1)
        event.widget.configure(bg='white')
        word.rem()
        check()
        if len(word.l) != 0:
            word.take().bind("<Button-1>", press2)
            binding(word.take())
        else:
            bindall()
    else:
        event.widget.bind("<Button-1>", press1)
        event.widget.configure(bg='white')
        word.rem()
        check()
        if len(word.l) != 0:
            word.take().bind("<Button-1>", press2)


def check():
    def winn():
        temp = data.letternum
        for i in data.bonuswords:
            temp += len(i)
        for i in data.words:
            temp -= len(i)
        win(temp, True)
    temp = ''
    temp2 = ''
    for i in word.l:
        temp += i.char
        temp2 += i.char + '-'
    v.set(temp2)
    try:
        if len(data.words) != 0:
            ind = data.words.index(temp)
            labels[ind].configure(bg=color.take())
            for i in word.l:
                i.lock = True
            labels2.append(labels[ind])
            labels.remove(labels[ind])
            data.words.remove(data.words[ind])
            v.set(temp)
            color.next()
            word.clear()
            unbindall()
            bindall()

        if len(data.words) == 0 and not data.bonuslevel:
            hg = 15+data.step*len(data.wordsclone)
            label = Label(root, text="Bonus words:", font='Arial 22')
            label.place(x=WordGen2.getborder(data.wordsclone, data.hard)*50+25, y=hg)
            hg += 10
            labels.clear()
            for i in data.bonuswords:
                hg += data.step
                label = Label(root, text=i, font='Arial ' + str(data.size))
                label.place(x=WordGen2.getborder(data.wordsclone, data.hard)*50+30, y=hg)
                labels.append(label)
            data.bonuslevel = True
            data.words.extend(data.bonuswords)
            Button(root, text='Конец', font='Arial 14', command=winn).place(x=WordGen2.getborder(data.wordsclone, data.hard)*50+135, y=WordGen2.getborder(data.wordsclone, data.hard)*50-25)
        if len(data.words) == 0 and data.bonuslevel:
            win(WordGen2.getborder(data.wordsclone, data.hard)**2)
    except Exception:
            pass


class Stack:
    l = []
    counter = 0

    def __init__(self, ls=None):
        if ls:
            self.l = ls

    def take(self):
        try:
            return self.l[len(self.l)-(1+self.counter)]
        except Exception:
            return '#999999'

    def shake(self):
        for i in range(len(self.l)):
            i1 = randint(0, len(self.l)-1)
            i2 = randint(0, len(self.l)-1)
            self.l[i1], self.l[i2] = self.l[i2], self.l[i1]
        self.counter = 0

    def next(self):
        self.counter += 1

    def put(self, x):
        self.l.append(x)

    def rem(self):
        self.l.remove(self.l[len(self.l)-1])

    def clear(self):
        self.l.clear()


class GameData:
    words = []
    wordsclone = []
    letternum = 0
    bonuswords = []
    step = 30
    size = 14
    bonuslevel = False
    time = 0
    timergo = True
    wordnums = 8
    hard = 2

    def nextwords(self):
        self.letternum = 0
        self.wordsclone.clear()
        words = open(join(base_dir, 'datasorted.dat'), 'r', encoding="utf-8").read().split()
        self.words.clear()
        if self.wordnums >= 15:
            self.step = 23
            self.size = 12
        else:
            self.step = 30
            self.size = 14
        for i in range(self.wordnums):
            tempw = words[randint(0, len(words)-1)]
            if tempw not in self.words:
                self.words.append(tempw)
                self.wordsclone.append(tempw)
                self.letternum += len(tempw)
            else:
                i -= 1

    def timer(self):
        if self.timergo:
            self.time += 1
            vtime.set(self.time)
            root.after(1000, self.timer)
        else:
            vtime.set(self.time)
            root.after(1000, self.timer)

    def refresh(self):
        self.wordnums = int(open('config.cnf', 'r').read().split()[0])


class But(Button):
    lock = False
    posx = 0
    posy = 0
    char = ''


def start(event=0):
    for i in letters:
        for j in i:
            j.destroy()
    for i in labels2:
        i.destroy()
    labels.clear()
    labels2.clear()
    word.clear()
    letters.clear()
    color.shake()
    data.bonuslevel = False

# -------------------------------------------------------------------------------------------------------------------------

    data.refresh()
    data.nextwords()
    words = WordGen2.start(data.words, data.hard)
    data.bonuswords = words[1]
    lett = words[0]
    bord = WordGen2.getborder(data.words, data.hard)
    root.minsize(int(bord*50+210), int(bord*50+65))
    frame = Frame(root, width=int(WordGen2.getborder(data.words, data.hard)*50+210), height=int(WordGen2.getborder(data.words, data.hard)*50+650))
    frame.place(x=0, y=0)
    labels2.append(frame)
    Frame(root, width=bord*50+20, height=bord*50+20, bg='grey').place(x=2,y=2)
    framelett = Frame(root, width=bord*50+16, height=bord*50+16, bg='white')
    framelett.place(x=4, y=4)
    hg = 15

    for i in range(bord):
        temp = []
        for j in range(bord):
            temp.append(0)
        letters.append(temp)
    for b in lett:
        but = But(framelett, text=b.char, width=3, height=1, bg="white", font="Arial 16")
        but.bind("<Button-1>", press1)
        but.place(x=b.x+10, y=b.y+10)
        but.posx, but.posy, but.char = b.x//50, b.y//50, b.char
        letters[b.x//50][b.y//50] = but
    for i in data.words:
        lab = Label(frame, text=i, font='Arial ' + str(data.size), name=i)
        lab.place(x=bord*50+30, y=hg)
        labels.append(lab)
        hg += data.step
    Label(frame, textvariable=v, font='Arial 18').place(x=5, y=bord*50*1.05)
    Label(frame, textvariable=vtime, font='Arial 18').place(x=bord*50+150, y=bord*50+25)
    data.time = 0
    data.timergo = True
    vtime.set(0)


def win(points, notfull=False):
    print(points)
    points = int(points*3) + int(points*1.5) - data.time
    wind = Toplevel(root, relief=SUNKEN)
    wind.minsize(width=350, height=400)
    Label(wind, text='  Вы победили! \n Ваши очки: ' + str(points), font='Arial 18').place(x=70, y=20)
    data.timergo = False
    records('set', points)
    ls = records('get')
    hg = 100
    for i in ls:
        Label(wind, text=str(i), font='Arial 14').place(x=150, y=hg)
        hg += 25


def settings():
    data.timergo = False
    dat = open('config.cnf', 'r').read().split()
    words = dat[0]
    recordes = dat[1:]
    t = StringVar()

    def prnt(event):
        t.set('Слова: ' + str(event))

    def save():
        temp = ''
        for i in recordes:
            temp += ' ' + i
        open('config.cnf', 'w').write(str(w.get()) + temp)
        wind.destroy()
        start()

    def reset():
        open('config.cnf', 'w').write(str(words) + ' 0 0 0 0 0 0 0 0 0 0')
        recordes.clear()
        recordes.extend(' 0 0 0 0 0 0 0 0 0 0'.split())

    def close():
        wind.destroy()
        data.timergo = True

    wind = Toplevel(root, relief=SUNKEN)
    wind.minsize(width=350, height=350)
    Label(wind, textvariable=t, font='Arial 18').place(x=125, y=20)
    w = Scale(wind, from_=1, to=20, orient=HORIZONTAL, width=20, length=200, showvalue=False, command=prnt)
    w.set(int(words))
    w.place(x=75, y=75)
    Button(wind, text='Сохранить', command=save, font='Arial 14', width=8).place(x=60, y=250)
    Button(wind, text='Закрыть', command=close, font='Arial 14', width=6).place(x=220, y=250)
    Label(wind, text='Сбросить рекорды:', font='Arial 18').place(x=80, y=120)
    Button(wind, text='СБРОС', font='Arial 14', command=reset).place(x=140, y=160)


def records(mode='window', points=0):
    dat = open('config.cnf', 'r').read().split()
    words = dat[0]
    recr = dat[1:]
    def close():
        wind.destroy()
        data.timergo = True

    if mode == 'window':
        data.timergo = False
        wind = Toplevel(root, relief=SUNKEN)
        wind.minsize(width=250, height=385)
        Label(wind, text='Рекорды:', font='Arial 18').place(x=75, y=10)
        hg = 40
        for i in recr:
            Label(wind, text=str(i), font='Arial 14').place(x=115, y=hg)
            hg += 30
        Button(wind, text='Закрыть', font='Arial 14', command=close).place(x=75, y=hg)
    elif mode == 'get':
        return recr
    elif mode == 'set':
        for i in range(len(recr)):
            recr[i] = int(recr[i])
        recr.append(points)
        recr.sort()
        recr.reverse()
        recr.remove(recr[-1])
        temp = ''
        for i in recr:
            temp += ' ' + str(i)
        open('config.cnf', 'w').write(words + temp)


def rules():
    txt = '''
Во время основного уровня вы должны находить
слова из правого столбца на поле из букв.
Слова идут "змейкой" и могут изгибатся как
угодно. После нахождения всех слов основного
уровня вам будут даны дополнительные слова,
которые нужно найти в оставшихся буквах,
буквы могут идти в произвольном порядке.
Также пройдя основной уровень вы можете
досрочно завершить игру, нажав кнопку "Конец"'''
    wind = Toplevel(root, relief=SUNKEN)
    wind.minsize(width=450, height=400)
    Label(wind, text='Правила:', font='Arial 18').place(x=160, y=20)
    Label(wind, text=txt, font='Arial 14').place(x=0, y=60)

labels = []
labels2 = []
letters = []
data = GameData()
word = Stack()
color = Stack(['#D1BC8A', '#F7BA0B', '#F3E03B', '#DB6A50', '#B42041', '#8A5A83', '#9A5161', '#992572' '#1F4764', '#21888F', '#2874B2',
               '#2E5978', '#28713E', '#0E4243', '#66825B', '#D2E094', '#6F474C', '#BAABE1', '#475256', '#483D8B', '#6A5ACD',
               '#BDB76B', '#FF69B4', '#00E2B5', '#999900', '#666633', '#DA97A5', '#F05A5A', '#FF4915', '#1242D1', '#5EF55E'])
root = Tk()
v = StringVar()
vtime = StringVar()
start()
data.timer()
m = Menu(root)
root.config(menu=m)
root.title('WordPuzzle by Olleggerr')
root.iconbitmap(join(base_dir, 'icon.ico'))
fm = Menu(m)
hm = Menu(m)
m.add_cascade(label="Игра", menu=fm)
fm.add_command(label="Новая игра", command=start)
fm.add_command(label="Рекорды", command=records)
fm.add_command(label="Настройки", command=settings)
fm.add_command(label="Выход", command=root.destroy)
m.add_cascade(label='Помощь', menu=hm)
hm.add_command(label='Правила', command=rules)
root.mainloop()


# for i in range(len(letters)):
#   for j in range(len(letters)):
#       print(letters[j][i].posy, end=' ')
#  print()
