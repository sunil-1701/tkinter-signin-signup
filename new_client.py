from tkinter import *
import socket
import hashlib
import pickle

from tkinter import messagebox
import re


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

clientsocket, address= s.accept()

#---------------------------------------------------------------------
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(regex, email)):
        pass
 
    else:
        messagebox.showinfo('error','Invalid E-mail')
        window.destroy()
        signUp_Window()
        


def signup():
    username=user.get()
    email=email_.get()
    
    password=passw.get()
    confirm_password=confirm_passw.get()
    check_email(email)
    
    if password==confirm_password:
        clientsocket.send(bytes('0','utf-8'))
        send_signup_data(username,email,password)
        
    else:
        messagebox.showinfo('error','Password does not match')
        
        
def on_enter_user(e):
    user.delete(0,'end')
def on_leave_user(e):
    if user.get()=='':
        user.insert(0,'Username')
        
def on_enter_email(e):
    email_.delete(0,'end')
def on_leave_email(e):
    if email_.get()=='':
        email_.insert(0,'E-mail')

def on_enter_passw(e):
    passw.delete(0,'end')
def on_leave_passw(e):
    if passw.get()=='':
        passw.insert(0,'Password')
        
def on_enter_confirm_passw(e):
    confirm_passw.delete(0,'end')
def on_leave_confirm_passw(e):
    if confirm_passw.get()=='':
        confirm_passw.insert(0,'Confirm Password')
        
def send_signup_data(user,email,passw):
    store(user,email,passw)
    sends(pickle.dumps(user_dict))
    
    mg=clientsocket.recv(16).decode('utf-8')
    if mg=='0':
        messagebox.showinfo("error","Username or E-mail already exists... Try using different credentials")
        user_dict.clear()
        window.destroy()
        signUp_Window()
        
    elif mg=='1':
        messagebox.showinfo('successful','Sign up successful')
        window.destroy()
        signIn_window()
         
user_dict={}
def hashing(text):
    h=hashlib.new("SHA256")
    h.update(text.encode())
    hashed=h.hexdigest()
    return hashed

def store(user,email,passw):
    user_dict["Username"]=user
    user_dict["E-mail"]=hashing(email)
    user_dict["Password"]=hashing(passw)
    
def sends(data): 
    
    while True:
        clientsocket.send(bytes(data))
        break

#------------------------------------------------------------------
def signUp_Window():
    
    global window
    window=Tk()
    window.title("Sign Up")
    window.geometry("925x500+300+200")
    window.configure(bg='#fff')
    window.resizable(False,False)

    frame=Frame(window,width=350,height=430,bg='#fff')
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign Up',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=25)

    global user
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter_user)
    user.bind("<FocusOut>", on_leave_user)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    
    global email_
    email_=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    email_.place(x=30,y=150)
    email_.insert(0,'E-mail')
    email_.bind("<FocusIn>",on_enter_email)
    email_.bind("<FocusOut>", on_leave_email)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
    
    global passw
    passw=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    
    passw.place(x=30,y=220)
    passw.insert(0,'Password')
    passw.bind("<FocusIn>",on_enter_passw)
    passw.bind("<FocusOut>", on_leave_passw)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
    
    global confirm_passw
    confirm_passw=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    confirm_passw.place(x=30,y=290)
    confirm_passw.insert(0,'Confirm Password')
    confirm_passw.bind("<FocusIn>",on_enter_confirm_passw)
    confirm_passw.bind("<FocusOut>", on_leave_confirm_passw)
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

    Button(frame,width=39,padx=7,text='Sign Up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=350)
    label=Label(frame,text='I already have an account!',fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=80,y=410)
    
    signin=Button(frame,width=6,text='Sign in',border=0,command=signIn_window,bg='white',cursor='hand2',fg='#57a1f8')
    signin.place(x=230,y=410)
    
    #landing_page()
    window.mainloop()

def signin():
    username=user.get()
    email=email_.get()
    password=passw.get()
    clientsocket.send(bytes('1','utf-8'))
    send_signin_data(username,email,password)
     
def send_signin_data(user,email,passw):
    store(user,email,passw)
    sends(pickle.dumps(user_dict))
    
    mg=clientsocket.recv(16).decode('utf-8')
    if mg=='0':
        messagebox.showinfo("Success","Login Successful")
        window1.destroy()
    elif mg=='1':
        messagebox.showinfo("Unsuccessful","Unsuccessful login attempt")
        window1.destroy()
        signIn_window()
        
     
def signIn_window():
    
    global window1
    window1=Tk()
    window1.title("Sign in")
    window1.geometry("925x500+300+200")
    window1.configure(bg='#fff')
    window1.resizable(False,False)

    frame=Frame(window1,width=350,height=430,bg='#fff')
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=25)

    global user
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter_user)
    user.bind("<FocusOut>",on_leave_user)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

    global email_
    email_=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    email_.place(x=30,y=150)
    email_.insert(0,'E-mail')
    email_.bind("<FocusIn>",on_enter_email)
    email_.bind("<FocusOut>",on_leave_email)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

    global passw
    passw=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    passw.place(x=30,y=220)
    passw.insert(0,'Password')
    passw.bind("<FocusIn>",on_enter_passw)
    passw.bind("<FocusOut>",on_leave_passw)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

    Button(frame,width=39,padx=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=280)
    label1=Label(frame,text='Don\'t have an account?',fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label1.place(x=90,y=340)

    signup=Button(frame,width=6,text='Sign up',border=0,command=signUp_Window,bg='white',cursor='hand2',fg='#57a1f8')
    signup.place(x=230,y=340)
    
    window.destroy()
    window1.mainloop()
    
signUp_Window()
