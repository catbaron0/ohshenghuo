import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import re
import http.cookiejar
import json
from urllib import request,parse
import threading
class register_win(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Download my life v.beta 0.1")
        self.label_id = tk.LabelFrame(self,text="Your email:")
        self.ipt_id = tk.Text(self.label_id,height=1)
        self.label_pwd = tk.LabelFrame(self,text="Your email:")
        self.ipt_pwd = tk.Text(self.label_pwd,height=1)
        self.opt = tk.Text(self)
        self.btn = tk.Button(self, command = self.do_down, text = u"下载我的生活")

        self.label_id.pack()
        self.ipt_id.pack()
        self.label_pwd.pack()
        self.ipt_pwd.pack()
        self.btn.pack()
        self.opt.pack()
 
        INFO = u"一个下载【oh生活】日记记录的第三方工具。\n需要你提供邮箱密码，不过放心是发给ohshenghuo的不是发给我的。\n因为是第三方要一篇一篇读所以可能有点慢。\n我没在oh生活上写过多少日记所以不知道日记太多会有啥问题。\n"
        self.output(INFO)

    def do_down(self):
        self.mail = self.ipt_id.get("0.0", tk.END)
        self.pwd = self.ipt_pwd.get("0.0", tk.END)
        self.clr()
        try:
            trd = threading.Thread(target = self.down_my_life)
            trd.start()
        except:
            print("Unable to start thread!")
        #self.register(users)

    def down_my_life(self):
        url = "https://ohshenghuo.com/api/login/"
        latest_url = "https://ohshenghuo.com/api/diary/latest/"
        pre_url = "https://ohshenghuo.com/api/diary/prev/"

        email = self.mail.strip()
        passwd = self.pwd.strip()
        data = parse.urlencode([
            ('email', email),
            ('password', passwd),
        ]).encode('utf-8')

        cj = http.cookiejar.CookieJar()
        opener = request.build_opener(request.HTTPCookieProcessor(cj))

        with opener.open(url,data) as f:
            self.output('Status: ' + str(f.status) +" " + str(f.reason) + "\n")
            login_res = f.read().decode('utf-8')
            login_res = json.loads(login_res)
            print(login_res)
        error = login_res['error']
        if error != 0:
            self.output("Sorry, login failed...\n")
            return
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        opener.addheaders = [('auth','token '+login_res['token'])]

        with open("DIARY.txt", "wt", encoding='utf-8') as f:
            self.output("Saving to files...\n\n")
            url = latest_url
            while True:
                with opener.open(url) as d:
                    data = d.read().decode('utf-8')
                    dd = json.loads(data)
                    err = dd["error"]
                    if err != 0:
                        break
                    diary = dd["diary"]
                    ctnt = "content:"+diary["content"]+"\n"
                    date = "date:"+diary["createddate"]+"\n"
                    weekday = "weekday:"+diary["weekday"]+"\n"
                    did = diary["id"]
                    self.output("saving diary on "+date+"\n")
                    f.write(date+weekday+ctnt+"====\n\n")
                url = pre_url+str(did)
        self.output("完成！\n")
        self.output("Saved to DIARY.txt\n")

    def output(self, outputs):
        text = self.opt
        text.insert(tk.INSERT, outputs)
        
    def clr(self):
        self.opt.delete(0.0, tk.END)

win = register_win()
win.mainloop()