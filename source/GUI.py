from tkinter import *
import time
import platform
if platform.system() == "Windows":
    print("Operating System: Linux")
    from RaspPi import config
    from RaspPi import wheels
    from RaspPi import avoidObstacle
elif platform.system() == "Linux":
    print("Operating System: Linux")
    import config
    import wheels
    import avoidObstacle
else:
    print("Invalid operating system.")

widgets = dict()
label_no = 0
scale_no = 0
sync_lock = False
flag = False
widgets['flag'] = flag
# 同步锁, 一次只触发一种模式
# 未实现同步锁

def createWindow(parent=None, mydict = {'title': 'myApp'}):
    if parent == None:
        window = Tk()
    else:
        window = Toplevel(parent)
    if 'title' in mydict.keys():
        window.title(mydict['title'])
    window.geometry('500x400')
    widgets['window_'+mydict['title']] = window
    return window

def createButton(window, text):
    b = Button(window,
                  text=text,
                  width=15,
                  height=2
                  )
    widgets['button_'+text] = b
    return b


def createLabel(window, strVar):
    if type(strVar) == StringVar:
        l = Label(window,
                     textvariable=strVar,  # 标签的文字
                     bg='white',  # 背景颜色
                     font=('Arial', 12),  # 字体和字体大小
                     )
    else:
        l = Label(window,
                  text=strVar,  # 标签的文字
                  bg='white',  # 背景颜色
                  font=('Arial', 12),  # 字体和字体大小
                  )
    widgets['label_' + str(label_no)] = l
    return l


def createScale(window, start, end, res, speed):
    s = Scale(window,
              from_=start,  # 设置最大值
              to=end,  # 设置最小值
              resolution=res,  # 设置步距值
              variable=speed,# 设置绑定变量
              orient=HORIZONTAL  # 设置水平方向
              )
    widgets["scale_"+str(scale_no)] = s
    return s


def turnLeft(event):
    widgets['status'].set("Turn left.")
    wheels.Left(widgets['speed'].get())


def turnRight(event):
    widgets['status'].set("Turn right.")
    wheels.Right(widgets['speed'].get())


def goForward(event):
    widgets['status'].set("Go forward.")
    wheels.Forward(widgets['speed'].get())


def goBackward(event):
    widgets['status'].set("Go backward.")
    wheels.Backward(widgets['speed'].get())


def RturnLeft(event):
    widgets['status'].set("Turn left stopped.")
    wheels.LeftRelease()


def RturnRight(event):
    widgets['status'].set("Turn right stopped.")
    wheels.RightRelease()


def RgoForward(event):
    widgets['status'].set("Forward stopped.")
    wheels.ForwardRelease()


def RgoBackward(event):
    widgets['status'].set("Backward stopped.")
    wheels.BackwardRelease()


def choicesRelease(event):
    """键盘松弛触发事件"""
    if event.char == 'a':
        RturnLeft("<ButtonRelease-1>")
    elif event.char == 'd':
        RturnRight("<ButtonRelease-1>")
    elif event.char == 'w':
        RgoForward("<ButtonRelease-1>")
    elif event.char == 's':
        RgoBackward("<ButtonRelease-1>")
    else:
        pass


def choices(event):
    """键盘按键触发事件"""
    if event.char == 'a':
        turnLeft("<Button-1>")
    elif event.char == 'd':
        turnRight("<Button-1>")
    elif event.char == 'w':
        goForward("<Button-1>")
    elif event.char == 's':
        goBackward("<Button-1>")
    else:
        pass



def handlerAdaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def createMainGUI():
    config.setup()
    # print(config.PWMs[0])
    window = createWindow(None, {'title': 'Main'})
    l = createLabel(window, "Hello Rasperberry Car")
    l.grid(row=1, columnspan=3, sticky=N+S+E+W)
    remote = createButton(window, 'Remote Control')
    remote.grid(row=2, column=2, sticky=N+S+E+W)
    remote.bind("<Button-1>", handlerAdaptor(createRemoteGUI, parent=window))
    track = createButton(window, 'Obstacle Avoidance')
    track.grid(row=3, column=2, sticky=N+S+E+W)
    track.bind("<Button-1>", handlerAdaptor(createTrackGUI, parent=window))
    window.mainloop()
    config.cleanup()


def createRemoteGUI(event, parent=None):
    window = createWindow(parent, {'title': 'Remote Control'})
    window.bind_all("<KeyRelease>", choicesRelease)
    window.bind_all("<Key>", choices)
    # create label to display information
    status = StringVar()
    status.set("Remote Control Mode")
    widgets['status'] = status
    label_0 = createLabel(window, status)
    label_0.grid(row=1, columnspan=3, sticky=N+S+E+W)
    # create buttons
    l = createButton(window, 'left')
    l.bind('<Button-1>', turnLeft)
    l.bind('<ButtonRelease-1>', RturnLeft)
    l.grid(row=3, column=0, sticky=N+S+E+W)
    r = createButton(window, 'right')
    r.bind('<Button-1>', turnRight)
    r.bind('<ButtonRelease-1>', RturnRight)
    r.grid(row=3, column=2, sticky=N+S+E+W)
    f = createButton(window, 'forward')
    f.bind('<Button-1>', goForward)
    f.bind('<ButtonRelease-1>', RgoForward)
    f.grid(row=2, column=1, sticky=N+S+E+W)
    b = createButton(window, 'backward')
    b.bind('<Button-1>', goBackward)
    b.bind('<ButtonRelease-1>', RgoBackward)
    b.grid(row=5, column=1, sticky=N+S+E+W)
    # create speed scale bar
    speed = StringVar()
    widgets['speed'] = speed
    s = createScale(window, 5, 15, 0.1, speed)
    s.config(label="speed")
    s.grid(row=6, columnspan=3, sticky=N+S+E+W)
    # loop
    window.mainloop()


def startAvoid(event):
    widgets['status'].set("Avoidance...")
    duration = widgets['time_input'].get().strip()
    print("duration time:", duration)
    avoidObstacle.start(5, float(duration))
    widgets['status'].set("Stopped.")
    avoidObstacle.stop()


def createTrackGUI(event, parent=None):
    window = createWindow(parent, {'title': 'Obstacle Avoidance'})
    status = StringVar()
    status.set("Avoidance Mode")
    widgets['status'] = status
    l = createLabel(window, status)
    l.grid(row=1, columnspan=3, sticky=N+S+E+W)
    time_show = createLabel(window, "Duration time(secs):")
    time_show.grid(row=3, column=1, sticky=N+S+E+W)
    # time_input = StringVar()
    # time_input.set("20")
    # widgets['time_input'] = time_input
    time_entry = Entry(window, bg="white", fg="red", text="20")
    time_entry.grid(row=3, column=2, columnspan=2, sticky=N+S+E+W)
    widgets['time_input'] = time_entry
    start = createButton(window, "Start")
    start.bind("<Button-1>", handlerAdaptor(startAvoid))
    start.grid(row=2, column=2, sticky=N+S+E+W)
    window.mainloop()


if __name__ == '__main__':
    try:
        createMainGUI()
    except:
        print("Interrupted.")
    finally:
        config.cleanup()
