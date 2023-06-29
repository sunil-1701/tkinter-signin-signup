
import socket
import mysql.connector as cnct
import pickle
mydb= cnct.connect(host='localhost',user='root',passwd='Pass#1',database='lunatic')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(),1234))
def signup():
    
        full_msg=b''
        full_msg=s.recv(1024)
        userData_dict=pickle.loads(full_msg)
        
        mycursor = mydb.cursor(buffered=(True))
        check_data=("select userName from userdata where exists(SELECT * FROM userdata where userName= %(Username)s or Email=%(E-mail)s)")
        mycursor.execute(check_data,userData_dict)
        data=mycursor.fetchone()
        if data is None:
                
            add_data=("Insert into userData" "(userName,Email,PassWd)" "values(%(Username)s,%(E-mail)s,%(Password)s)")
            mycursor.execute(add_data, userData_dict)
            mydb.commit()
            s.send(bytes('1','utf-8'))
            userData_dict.clear()
            
        else:
            
            s.send(bytes('0','utf-8'))
        

def signin():
    
        full_msg=b''
        full_msg=s.recv(1024)
        
        userData_dict=pickle.loads(full_msg)
        
        mycursor = mydb.cursor(buffered=(True))
        check_data=("select userName from userdata where exists(SELECT * FROM userdata where userName= %(Username)s and Email=%(E-mail)s and PassWd=%(Password)s)")
        mycursor.execute(check_data,userData_dict)
        data=mycursor.fetchone()
        if data is None:
            s.send(bytes('1','utf-8'))
        else:
            
            s.send(bytes('0','utf-8'))
            


while True:
    mg=s.recv(16).decode('utf-8')
    if mg=="0":
        signup()
    else:
        signin()
        break
