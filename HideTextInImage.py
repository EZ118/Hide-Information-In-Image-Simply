import tkinter.filedialog
from tkinter import *
from tkinter.messagebox import *
from PIL import Image

#以下为自定义部分
SpotSpace = 5
#以上为自定义部分


def FileOpen():
    r = tkinter.filedialog.askopenfilename(title='打开图片文件', filetypes=[('Image File', '*.*')])
    if len(r) == 0:
        print("未选择文件")
    else:
        global fp
        fp = r
        showinfo('成功', '文件已打开')

def clear_console():
    console.delete('1.0','end')

def str2hex(by):
    cb = ()
    for i in by:
        cb += (ord(i), )
    cb_len = len(cb)
    if cb_len % 3 != 0:
        for i in range(0, cb_len % 3 + 1):
            cb += (32, )
    return cb

def hex2str(s):
    a = ""
    for i in range(0, 3):
        try:
            a += chr(s[i])
        except:
            print("error")
    return a

def getChinese(d):
    d = d.split("[}")
    s = ""
    for i in d:
        if "0x" in i:
            i = chr(int(i.replace("0x", "")))
        s += i
    return s

def ChinesetoChar(d):
    cnt = 0
    s = ""
    for i in d:
        if ord(i) >= 256:
            i = "[}0x" + str(ord(i)) + "[}"
        s += i
    return s

def encode_img():
    try:
        img = Image.open(fp)
    except:
        showerror("错误", "请先点击“打开...”按钮选择需要加密或解密的图片")
        return
    
    imgw, imgh = img.size

    ipt = console.get("1.0","end")
    ipt = ChinesetoChar(ipt)
    data = str2hex(ipt)

    cnt = 0
    for i in range(0, imgw, SpotSpace):
        for j in range(0, imgh, SpotSpace):        
            if cnt >= len(ipt):
                img.putpixel((i, j), (32,32,32))
            else:
                img.putpixel((i, j), (data[cnt],data[cnt + 1],data[cnt + 2]))
                cnt += 3
    img.save(fp)

def decode_img():
    try:
        img = Image.open(fp)
    except:
        showerror("错误", "请先点击“打开...”按钮选择需要加密或解密的图片")
        return
    
    img = Image.open(fp)
    imgw, imgh = img.size

    data = ""

    wcnt = hcnt = 0
    for i in range(0, imgw, SpotSpace):
        for j in range(0, imgh, SpotSpace):
            data += hex2str(img.getpixel((i, j)))
    data = data.replace("             ", "")
    data = getChinese(data)
    data += "\\n"
    data = data.split("\\n")
    console.delete('1.0','end')
    for i in data:
        console.insert("end", i + "\n")

win = Tk()
win.title('自制图片隐写工具')
win.geometry('264x344+100+100')

Label1 = Label(win, text='请先打开文件后再操作:', font=('黑体', 12), anchor=W).place(y=13, x=14, width=234, height=20)

Button1 = Button(win, text='打开...', font=('黑体', 11), command = FileOpen).place(y=40, x=20, width=65, height=28)
Button2 = Button(win, text='加密', font=('黑体', 11), command = encode_img).place(y=40, x=99, width=40, height=28)
Button3 = Button(win, text='解密', font=('黑体', 11), command = decode_img).place(y=40, x=153, width=40, height=28)
Button4 = Button(win, text='清空', font=('黑体', 11), command = clear_console).place(y=40, x=207, width=40, height=28)

console = Text(win, font=('黑体', 11))
console.place(y=82, x=15, width=236, height=241)

win.mainloop()
