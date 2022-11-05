import tkinter as tk
import random
import time

def ip_to_binary(addr):
    splitted=addr.split(".")
    for n,data in enumerate(splitted):
        if int(data) <= 255:
            splitted[n]=bin(int(data))[2:].zfill(8)
        else:
            raise ValueError('Incorrect syntax')
    return '.'.join(splitted)

def binary_to_ip(addr):
    splitted=addr.split(".")
    for n,data in enumerate(splitted):
        splitted[n]=str(int((data),2))
    return '.'.join(splitted)

def nadress_finder(i:str,m:str):
    ip    = "".join(ip_to_binary(i).split("."))
    masque= "".join(ip_to_binary(m).split("."))
    adr_reseau_raw=[str(int(bool(int(masque[i]) and int(ip[i])))) for i in range(32)]
    adr_reseau=".".join([''.join(adr_reseau_raw)[:8],''.join(adr_reseau_raw)[8:16],''.join(adr_reseau_raw)[16:24],''.join(adr_reseau_raw)[24:32]])
    return binary_to_ip(adr_reseau)

def broadcast_finder(i:str,m:str):
    ip    = "".join(ip_to_binary(i).split("."))
    masque= "".join(ip_to_binary(m).split("."))
    broadcast_raw=[i for i in ip]
    for i in range(len(masque)):
        if masque[i] == '0':
            broadcast_raw[i]='1'
    broadcast=".".join([''.join(broadcast_raw)[:8],''.join(broadcast_raw)[8:16],''.join(broadcast_raw)[16:24],''.join(broadcast_raw)[24:32]])
    return binary_to_ip(broadcast)


def ip_mask_randomizer():
    masque_possible=[0,128,192,224,240,248,252,254]
    ip=".".join([str(random.randint(0,255)) for i in range(4)])
    masque=[str(255) for i in range(random.randint(1,3))]
    masque.append(str(masque_possible[random.randint(0,len(masque_possible)-1)]))
    while len(masque)!=4:
        masque.append("0")
    masque=".".join(masque)

    return ip,masque


jeu= tk.Tk()
jeu.title("CIDR game")
jeu.geometry("370x170")
#jeu.resizable(False,False)

#Variables
a_check=0
b_check=0
score_val=0
solution_ip= tk.StringVar()
solution_broadcast = tk.StringVar()


#fonctions
def setup(i,m):
    ip_val['text']=i
    masque_val['text']=m
    difficulty()
    #ajouter check difficulté

def difficulty():
    masque_possible=["0","128","192","224","240","248","252","254"]
    masque_facile=["255.0.0.0","255.255.0.0","255.255.255.0"]
    masque_moyen=masque_possible[4:]
    masque_dure=masque_possible[:4]
    if masque_val['text'] in masque_facile:
        difficult["text"]= "easy"
        difficult["bg"]="green"

    elif check_list(masque_val['text'].split("."),masque_moyen):
        difficult["text"]= "med"
        difficult["bg"]="orange"

    elif check_list(masque_val['text'].split("."),masque_dure):
        difficult["text"]= "hard"
        difficult["bg"]="red"



def check_list(l1, l2):
    for i in l1:
        if i in l2:
            return True
        else:
            continue
    return False

def score_difficulty():
    global score_val
    if difficult["text"]=="easy":
        score_val+=100

    elif difficult["text"]== "med":
        score_val+=250

    elif difficult["text"]== "hard":
        score_val+=500

    score['text']=f'Score:{score_val}'




def solution():
    global score_val
    if(check['state']=="normal"):
        check["state"] = "disabled"
        check.grid_forget()
        score_val-=50
        score['text']=f'Score:{score_val}'
        solution_ip.set(nadress_finder(ip_val['text'],masque_val['text']))
        solution_broadcast.set(broadcast_finder(ip_val['text'],masque_val['text']))
    elif (check['state']=="disabled"):
        check["state"]="normal"
        check.grid(row=9,column=1)
        setup(ip_mask_randomizer()[0],ip_mask_randomizer()[1])
        solution_ip.set("")
        solution_broadcast.set("")


def check_solution():
    global score_val
    global a_check
    global b_check
    adresse_val.get()
    broadcast_val.get()
    if adresse_val.get() == nadress_finder(ip_val['text'],masque_val['text']):
        if a_check==0:
            print("score+1 adresse reseau")
            score_difficulty()
            a_check_label['text']='V'
            a_check_label["bg"]='green'
            a_check_label.grid(row=6,column=2)
            a_check=1

    if broadcast_val.get() == broadcast_finder(ip_val['text'],masque_val['text']):
        if b_check==0:
            print("score+1 broadcast")
            score_difficulty()
            b_check_label['text']='V'
            b_check_label["bg"]='green'
            b_check_label.grid(row=7,column=2)
            b_check=1

    if a_check and b_check:
        setup(ip_mask_randomizer()[0],ip_mask_randomizer()[1])
        solution_ip.set("")
        solution_broadcast.set("")


        a_check=0
        b_check=0
        a_check_label['text']='X'
        a_check_label["bg"]='red'
        a_check_label.grid(row=6,column=2)
        b_check_label['text']='X'
        b_check_label["bg"]='red'
        b_check_label.grid(row=7,column=2)


#Widgets
score= tk.Label(jeu,text="Score",font=("Courier", 15))
difficult=tk.Label(jeu,text="diff",font=("Courier", 15),bg="red")

ip=tk.Label(jeu,text="    IP",font=("Courier", 10)).grid(row=3,column=0)
ip_val=tk.Label(jeu,text="xxx.xxx.xxx.xxx",anchor='e',justify='left')
masque=tk.Label(jeu,text="Mask",font=("Courier", 10)).grid(row=4,column=0)
masque_val=tk.Label(jeu,text="xxx.xxx.xxx.xxx",anchor='e',justify='left')
adresse=tk.Label(jeu,text="Network Adress",font=("Courier", 10)).grid(row=6,column=0)
adresse_val=tk.Entry(jeu,textvariable=solution_ip)
broadcast=tk.Label(jeu,text="Broadcast",font=("Courier", 10)).grid(row=7,column=0)
broadcast_val=tk.Entry(jeu,textvariable=solution_broadcast)
check=tk.Button(text="CHECK",font=("Courier", 15),bg="green",command=check_solution)
solution=tk.Button(text="?",font=("Courier", 15),bg="purple",command=solution).grid(row=9,column=2)

a_check_label= tk.Label(jeu,text="X",bg="red",justify='left',anchor='w')
b_check_label= tk.Label(jeu,text="X",bg="red",justify='left',anchor='w')


#Géométrie
score.grid(row=0,column=1)
difficult.grid(row=0,column=2)
ip_val.grid(row=3,column=1)
masque_val.grid(row=4,column=1)
adresse_val.grid(row=6,column=1)
broadcast_val.grid(row=7,column=1)
check.grid(row=9,column=1)
a_check_label.grid(row=6,column=2)
b_check_label.grid(row=7,column=2)


setup(ip_mask_randomizer()[0],ip_mask_randomizer()[1])
jeu.mainloop()
