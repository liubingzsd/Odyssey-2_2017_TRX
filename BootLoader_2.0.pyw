IP1 = '192'
IP2 = '168'
IP3 = '2'
IP4 = '160'

from Tkinter import*
import tkFileDialog, os, time, socket, binascii

UDP_PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# ----------------------------------
#    User Interface
#------------------------------------
def close():
    sock.close()
    print ('The End')
    root.destroy()
    root.quit()
    
root=Tk()
root.title('Bootloader 2.0')
x = str((root.winfo_screenwidth() - root.winfo_reqwidth()) / 3)
y = str((root.winfo_screenheight() - root.winfo_reqheight()) / 3)
root.geometry('400x300+'+x+'+'+y)
root.maxsize(400, 330)
root.minsize(400, 330)
root.protocol('WM_DELETE_WINDOW', close)
#-------------------------------------------------------------------

# Main message
main_msg = StringVar()
main_msg.set('''        Welcome to Bootloader 2.0 for Odyssey TRX.
Before using this programm ensure that divice runs in bootloader mode
and set current IP address here:

''')
main = Label(root, textvariable=main_msg, width=54, height=5, #bd=2,
             relief=GROOVE, justify=CENTER)
main.place(x=8, y=10)

# Current IP address selection field
ip_addr1 = StringVar()
ip_addr2 = StringVar()
ip_addr3 = StringVar()
ip_addr4 = StringVar()
ip_addr1.set(IP1)
ip_addr2.set(IP2)
ip_addr3.set(IP3)
ip_addr4.set(IP4)
current_ip_entry1 = Entry(root, width=3, textvariable=ip_addr1)
current_ip_entry2 = Entry(root, width=3, textvariable=ip_addr2)
current_ip_entry3 = Entry(root, width=3, textvariable=ip_addr3)
current_ip_entry4 = Entry(root, width=3, textvariable=ip_addr4)
current_ip_entry1.place(x=130, y=62)
current_ip_entry2.place(x=160, y=62)
current_ip_entry3.place(x=190, y=62)
current_ip_entry4.place(x=220, y=62)
    
# Test IP button
def test_error_window(msg, color, btn='N'):
    global test_error
    test_error = Toplevel(root)
    z = root.winfo_geometry()
    x = int(z[-7:-4]) + 30
    y = int(z[-3:])  + 30
    if(color=='green'):
        abg = 'green'
        bg = 'pale green'
    elif(color=='red'):
        abg = 'red'
        bg = 'pink'
    test_error.geometry('400x300+' + str(x) + '+' + str(y))
    test_error.maxsize(400, 100)
    test_error.minsize(400, 100)
    test_error.grab_set()
    test_error.focus_set()
    error_msg = StringVar()
    error_msg.set(msg)
    error = Label(test_error, textvariable=error_msg, width=54, height=3,
             relief=GROOVE, justify=CENTER)
    error.place(x=8, y=10)
    if(btn=='D'):
        btn = DISABLED
    else:
        btn = NORMAL
    close_btn = Button(test_error, text="CLOSE", activebackground=abg,
                bg=bg, bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
                width=53,height=1, state=btn,
                command=test_error.destroy
                )
    close_btn.place(x=10, y=67) 
    
def test_button_clicked():
    ip_1 = ip_addr1.get()
    ip_2 = ip_addr2.get()
    ip_3 = ip_addr3.get()
    ip_4 = ip_addr4.get()
    if(len(ip_1)<=3 and len(ip_2)<=3 and len(ip_3)<=3 and len(ip_4)<=3
       and ip_1.isdigit()==True and ip_2.isdigit()==True
       and ip_3.isdigit()==True and ip_4.isdigit()==True):
        if(int(ip_1)>255 or int(ip_2)>255 or int(ip_3)>255 or int(ip_4)>255):
            test_error_window('''The entry is not correct. Please use only digits in the range
from 0 to 255 and try again.
''', 'red')
            return None
        MESSAGE = bytearray(b'MAC' + chr(0)*29) # Preparing the message
        UDP_IP = ip_1 +'.' +ip_2 + '.' + ip_3 + '.' + ip_4    
        DEVICE_ADDRESS = (UDP_IP, UDP_PORT)
        sock.sendto(MESSAGE, DEVICE_ADDRESS)# Sending request
        sock.settimeout(1)# Waiting for reply
        try:
            reply = sock.recv(32)
        except:
            test_error_window('''Device was not found. Please check the entered
IP address and settings of Ethernet connection on your PC.''', 'red')
            browse_btn['state']=DISABLED
            ch_ip_btn['state']=DISABLED
            quit_btn['activebackground'] = 'red'
            quit_btn['bg'] = 'pink'
        else:# Reply was received
            if(reply[0:3]==b'MAC'):
                MAC1 = binascii.b2a_hex(reply[26])
                MAC2 = binascii.b2a_hex(reply[27])
                MAC3 = binascii.b2a_hex(reply[28])
                MAC4 = binascii.b2a_hex(reply[29])
                MAC5 = binascii.b2a_hex(reply[30])
                MAC6 = binascii.b2a_hex(reply[31])
                test_error_window(('''Device with the specified IP address was found
in the current network environment. MAC: '''+MAC1+' '+MAC2+' '+MAC3+' '+MAC4+' '+MAC5+' '+MAC6), 'green')
                self = open('BootLoader_2.0.pyw', 'r')# writing this IP to file
                self_lines = self.readlines()
                self.close()
                self_lines[0] = 'IP1 = ' + "'" + str(ip_addr1.get() + "'\n")
                self_lines[1] = 'IP2 = ' + "'" + str(ip_addr2.get() + "'\n")
                self_lines[2] = 'IP3 = ' + "'" + str(ip_addr3.get() + "'\n")
                self_lines[3] = 'IP4 = ' + "'" + str(ip_addr4.get() + "'\n")
                self = open('BootLoader_2.0.pyw', 'w')
                self.writelines(self_lines)
                self.close()
                browse_btn['state']=NORMAL
                ch_ip_btn['state']=NORMAL
                quit_btn['activebackground'] = 'green'
                quit_btn['bg'] = 'pale green' 
            else:
                test_error_window('''Device was not found. Please check the entered
IP address and settings of Ethernet connection on your PC.''', 'red')
                browse_btn['state']=DISABLED
                ch_ip_btn['state']=DISABLED
                quit_btn['activebackground'] = 'red'
                quit_btn['bg'] = 'pink'
               
    else: # Entry is not correct
        test_error_window('''The entry is not correct. Please use only digits in range
from 0 to 255 and try again.
''', 'red')

 #   
test_ip_btn = Button(root, text="Test", activebackground='green',
                bg='grey', bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
               # width=6,height=1,
                command=test_button_clicked)
test_ip_btn.place(x=250, y=60 )

#-----------------------------------------------------------------------
# Changing IP
ch_ip_msg = StringVar()
ch_ip_msg.set('''To change the current IP enter new value and click button.

''')
ch_ip = Label(root, textvariable=ch_ip_msg, width=54, height=3, #bd=2,
             relief=GROOVE, justify=CENTER)
ch_ip.place(x=8, y=100)

# New IP address selection field
new_ip_addr1 = StringVar()
new_ip_addr2 = StringVar()
new_ip_addr3 = StringVar()
new_ip_addr4 = StringVar()
new_ip_addr1.set(ip_addr1.get())
new_ip_addr2.set(ip_addr2.get())
new_ip_addr3.set(ip_addr3.get())
new_ip_addr4.set(ip_addr4.get())
new_ip_entry1 = Entry(root, width=3, textvariable=new_ip_addr1)
new_ip_entry2 = Entry(root, width=3, textvariable=new_ip_addr2)
new_ip_entry3 = Entry(root, width=3, textvariable=new_ip_addr3)
new_ip_entry4 = Entry(root, width=3, textvariable=new_ip_addr4)
new_ip_entry1.place(x=130, y=122)
new_ip_entry2.place(x=160, y=122)
new_ip_entry3.place(x=190, y=122)
new_ip_entry4.place(x=220, y=122)



# Change IP button
def write_ip():
    ip_1 = new_ip_addr1.get()
    ip_2 = new_ip_addr2.get()
    ip_3 = new_ip_addr3.get()
    ip_4 = new_ip_addr4.get()
    if(len(ip_1)<=3 and len(ip_2)<=3 and len(ip_3)<=3 and len(ip_4)<=3
       and ip_1.isdigit()==True and ip_2.isdigit()==True
       and ip_3.isdigit()==True and ip_4.isdigit()==True):
        if(int(ip_1)>255 or int(ip_2)>255 or int(ip_3)>255 or int(ip_4)>255):
            test_error_window('''The entry is not correct. Please use only digits in range
from 0 to 255 and try again.
''', 'red')
            return None
        MESSAGE = bytearray(b'WIP' + chr(0)*25) # Preparing the message
        MESSAGE = MESSAGE + chr(int(ip_1)) + chr(int(ip_2)) + chr(int(ip_3)) + chr(int(ip_4))
        UDP_IP = ip_addr1.get() +'.' +ip_addr2.get() + '.' + ip_addr3.get() + '.' + ip_addr4.get()
        DEVICE_ADDRESS = (UDP_IP, UDP_PORT)
        sock.sendto(MESSAGE, DEVICE_ADDRESS)# Sending request
        sock.settimeout(1)# Waiting for reply
        try:
            reply = sock.recv(32)
        except:
            test_error_window('''The IP address was not writen sucsesfully !
Please check a connection and try again''', 'red')
        else:# Reply was received
            if(reply[0:3]==b'WIP'):
                test_error_window('''The new IP address was writed sucsesfully.
Please make changes in Ethernet settings on your PC.
''', 'green')
                ip_addr1.set(ip_1) # writing new IP to current fields
                ip_addr2.set(ip_2)
                ip_addr3.set(ip_3)
                ip_addr4.set(ip_4)
                self = open('BootLoader_2.0.pyw', 'r')# writing new IP to file
                self_lines = self.readlines()
                self.close()
                self_lines[0] = 'IP1 = ' + "'" + str(new_ip_addr1.get() + "'\n")
                self_lines[1] = 'IP2 = ' + "'" + str(new_ip_addr2.get() + "'\n")
                self_lines[2] = 'IP3 = ' + "'" + str(new_ip_addr3.get() + "'\n")
                self_lines[3] = 'IP4 = ' + "'" + str(new_ip_addr4.get() + "'\n")
                self = open('BootLoader_2.0.pyw', 'w')
                self.writelines(self_lines)
                self.close() 
    else:
        # Error New IP entry window
        test_error_window('''The entry is not correct. Please use only digits in range
from 0 to 255 and try again.
''', 'red')
 
ch_ip_btn = Button(root, text="Write IP", activebackground='green',
                bg='grey', bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
               # width=6,height=1,
                command=write_ip, state=DISABLED)
ch_ip_btn.place(x=250, y=120 )

#-----------------------------------------------------------------------
# Write FW
wr_fw_msg = StringVar()
wr_fw_msg.set('''For writing FirmWare select needed slot, choose correct
file and click button.





''')
wr_fw = Label(root, textvariable=wr_fw_msg, width=54, height=8, #bd=2,
             relief=GROOVE, justify=CENTER)
wr_fw.place(x=8, y=160)

# Radiobuttons (select slot)
rb_state = StringVar()
rb_state.set('Slot 1')
rbutton0 = Radiobutton(root, text='Slot 0', 
                       fg='red', variable=rb_state, value='Slot 0')
rbutton0.place(x=80, y=200)
rbutton1 = Radiobutton(root, text='Slot 1', variable=rb_state, value='Slot 1')
rbutton1.place(x=140, y=200)
rbutton2 = Radiobutton(root, text='Slot 2', variable=rb_state, value='Slot 2')
rbutton2.place(x=200, y=200)
rbutton3 = Radiobutton(root, text='Slot 3', variable=rb_state, value='Slot 3')
rbutton3.place(x=260, y=200)

# Select file field
filename = StringVar()
filename.set(os.path.abspath(os.curdir))
file_enter = Entry(root, textvariable=filename, width=61)
file_enter.place(x=13, y=230)

# Browse file button
def browse_clicked():
    path = tkFileDialog.askopenfilename(#initialdir = "/",
                title = "Select file",filetypes = [("rbf files","*.rbf")])
    if(path == ''):
        filename.set(os.path.abspath(os.curdir))
    else:
        filename.set(path)
    if(path[-4:]=='.rbf'):
        write_btn['state']=NORMAL
    else:
        write_btn['state']=DISABLED
            
browse_btn = Button(root, text="Browse", activebackground='green',
                bg='grey', bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
                width=20,height=1,
                command=browse_clicked, state=DISABLED)
browse_btn.place(x=25, y=255)

# Write file button
def write_clicked():
    f = filename.get()
    f = f.split('/')
    f = f[-1]
    slot = rb_state.get()
    if(rb_state.get()=='Slot 0' and f[0:10]!='Bootloader'):
       test_error_window('''Incorrect file for Slot 0
Please select correct Bootloader file and try again.''', 'red', 'N')
       return
    elif(rb_state.get()!='Slot 0' and f[0:10]=='BootLoader'):
       test_error_window('''Incorrect file for Slot 1-3
Please select correct FirmWare file and try again.''', 'red', 'N')
       return
    f = open(filename.get(), 'rb')# open RBF file
    rbf = f.read() + chr(255)*256
    f.close()
    pages = len(rbf) // 256
    if(pages>(32*256)):
        test_error_window('''This file has too big size for writing to Slot.
Please select other file and try again.''', 'red', 'N')
        return
    test_error_window('Erasing '+slot+' ...'+'\nPlease wait.', 'green', 'D')
    root.update()
    MESSAGE = bytearray(b'ERS' + chr(0)*28 + chr(int(slot[-1])))# Preparing the message
    UDP_IP = ip_addr1.get() +'.' +ip_addr2.get() + '.' + ip_addr3.get() + '.' + ip_addr4.get()
    DEVICE_ADDRESS = (UDP_IP, UDP_PORT)
    sock.sendto(MESSAGE, DEVICE_ADDRESS)# Sending request
    sock.settimeout(10)# Waiting for reply
    reply = None
    while(reply==None):
        try:
            reply = sock.recv(32)
        except:
            test_error.destroy()
            test_error_window('''The erasing Slot was not done sucsesfully !
Please check a connection and try again''', 'red', 'N')
            return None
        else:# Reply was received
            if(reply[0:3]!=b'ERS'):
                reply = None  
    test_error.destroy()
    test_error_window('Writing FirmWare to '+slot+' ...'+'\nPlease wait.', 'green', 'D')
    root.update()
    for i in range(pages):
        MESSAGE = bytearray(b'WPD' + chr(0)*29) # Preparing the message
        MESSAGE += rbf[i*256 : i*256+256]
        sock.sendto(MESSAGE, DEVICE_ADDRESS)# Sending request
        sock.settimeout(2)# Waiting for reply
        reply = None
        while(reply==None):
            try:
                reply = sock.recv(32+256)
            except:
                test_error.destroy()
                test_error_window('''The writing FirmWare was not done sucsesfully !
Please check a connection and try again''', 'red', 'N')
                return None
            else:
                if(reply[0:3]!=b'WPD'):
                    reply = None
                    
        if(MESSAGE != reply):
            test_error.destroy()
            test_error_window('''The writing FirmWare was not done sucsesfully !
Please check a connection and try again''', 'red', 'N')
            return None
          
    test_error.destroy()
    test_error_window('The writing FirmWare was done sucsesfully.', 'green', 'N')            
            
write_btn = Button(root, text="Write FW", activebackground='green',
                bg='grey', bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
                width=20,height=1,
                command=write_clicked, state=DISABLED)
write_btn.place(x=220, y=255)

#------------------------------------------------------------------------

# Quit button    
quit_btn = Button(root, text="QUIT", activebackground='red',
                bg='pink', bd=1,
                justify=CENTER,
                relief=RIDGE, overrelief=SUNKEN,
                width=53,height=1,
                command=close
                )
quit_btn.place(x=10, y=295)
#------------------------------------------------------------------------
    

root.mainloop()



