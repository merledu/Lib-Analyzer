import finalfile1
import matplotlib.pyplot as plt
import mplcursors
import re
#func= "(A&!B&!C) | (!A&B&!C) | (!A&!B&C) | (A&B&C)"

# Name = list(finalfile1.Cell.dic.keys())
def Area_vs_Leakage(func, dic):
    Area = []
    Leakage = []
    Function = []
    rise_delay = []
    area_list= []
    leakage_list=[]
    name_list= []
    delay =[]
    fall_delay=[]
    name_list= []
    
    Name = list(dic.keys())
    for i in dic.keys():
        Area.append(dic[i]["area"])
        Leakage.append(dic[i]["leakage"])
        Function.append(dic[i]["function"])
        
    index_pos_list = [ i for i in range(len(Function)) if Function[i] == func ]
    
    
    for i in index_pos_list:
            area_list.append(Area[i])
            leakage_list.append(Leakage[i])
            name_list.append(Name[i])
    x = area_list
    y = leakage_list
    plt.plot(x, y,c="red", marker='o',  linestyle = 'None')
    plt.title('Leakage vs Area', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Leakage(nW)', fontsize=14)
    mplcursors.cursor(hover=True)
    
    for i,j,k in zip(area_list,leakage_list,name_list):

        if "sky" in k:
             plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
        
    plt.show()


def plot_area_vs_rise_delay(func, dic):
    Area = []
    Leakage = []
    Function = []
    rise_delay = []
    area_list= []
    leakage_list=[]
    name_list= []
    delay =[]
    fall_delay=[]
    name_list= []
    Name = list(dic.keys())
    
    for i in dic.keys():
        rise_delay.append(dic[i]["Max Delay Value Rise"])
        Area.append(dic[i]["area"])
        Function.append(dic[i]["function"])
    index_pos_list = [ i for i in range(len(Function)) if Function[i] == func ]
    for i in index_pos_list:
            area_list.append(Area[i])
            delay.append(rise_delay[i])
            name_list.append(Name[i])
    
    x = area_list
    y = delay
    plt.plot(x, y, linestyle='None',c="red", marker='o')
    plt.title('Area vs Rise Delay', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Rise_Delay(ns) ', fontsize=14)
    mplcursors.cursor(hover=True)
    
    for i,j,k in zip(area_list,delay,name_list):
       
        if "sky" in k:
             plt.text(i,j,k.strip("sky130_fd_sc_hd__"))

    plt.show()

def plot_area_vs_fall_delay(func, dic):
    
    Area = []
    Leakage = []
    Function = []
    rise_delay = []
    area_list= []
    leakage_list=[]
    name_list= []
    delay =[]
    fall_delay=[]
        

    Name = list(dic.keys())
    for i in dic.keys():
        fall_delay.append(dic[i]["Max Delay Value Fall"])
        Area.append(dic[i]["area"])
        Function.append(dic[i]["function"])
    index_pos_list = [ i for i in range(len(Function)) if Function[i] == func ]
    for i in index_pos_list:
            area_list.append(Area[i])
            delay.append(fall_delay[i])
            name_list.append(Name[i])
    
    x = area_list
    y = delay
    plt.plot(x, y, linestyle='None',c="red", marker='o')
    plt.title('Area vs Fall Delay', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Fall_Delay(ns) ', fontsize=14)
    mplcursors.cursor(hover=True)
    
    for i,j,k in zip(area_list,delay,name_list):
       
        if "sky" in k:
             plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
        
    plt.show()


def plot_leakage_vs_fall_delay(func, dic):
    Area = []
    Leakage = []
    Function = []
    rise_delay = []
    area_list= []
    leakage_list=[]
    name_list= []
    delay =[]
    fall_delay=[]
    Name = list(dic.keys())
    for i in dic.keys():
        Leakage.append(dic[i]["leakage"])
        Function.append(dic[i]["function"])
        fall_delay.append(dic[i]["Max Delay Value Fall"])

    index_pos_list = [ i for i in range(len(Function)) if Function[i] == func ]
    for i in index_pos_list:
            leakage_list.append(Leakage[i])
            delay.append(fall_delay[i])
            name_list.append(Name[i])
    x = leakage_list
    y = delay
    plt.plot(x, y, linestyle='None',c="red", marker='o')
    plt.title('Leakage vs Fall Delay', fontsize=14)
    plt.xlabel('Leakage(nW)', fontsize=14)
    plt.ylabel('Fall_Delay(ns) ', fontsize=14)
    mplcursors.cursor(hover=True)
    
    for i,j,k in zip(leakage_list,delay,name_list):
       
        if "sky" in k:
             plt.text(i,j,k.strip("sky130_fd_sc_hd__"))

        
    plt.show()
def plot_leakage_vs_rise_delay(func, dic):
    Area = []
    Leakage = []
    Function = []
    rise_delay = []
    area_list= []
    leakage_list=[]
    name_list= []
    delay =[]
    fall_delay=[]
    Name = list(dic.keys())
    for i in dic.keys():
        Leakage.append(dic[i]["leakage"])
        Function.append(dic[i]["function"])
        rise_delay.append(dic[i]["Max Delay Value Rise"])

    index_pos_list = [ i for i in range(len(Function)) if Function[i] == func ]
    for i in index_pos_list:
            leakage_list.append(Leakage[i])
            delay.append(rise_delay[i])
            name_list.append(Name[i])
    x = leakage_list
    y = delay
    plt.plot(x, y, linestyle='None',c="red", marker='o')
    plt.title('Leakage vs Rise Delay', fontsize=14)
    plt.xlabel('Leakage(nW)', fontsize=14)
    plt.ylabel('Rise_Delay(ns) ', fontsize=14)
    mplcursors.cursor(hover=True)
    
    for i,j,k in zip(leakage_list,delay,name_list):
        if "sky" in k:
             plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
        
    plt.show()


def delay_vs_output_cap_graph(name_of_cell,cap_fall,cap_rise,del_fall,del_rise):
        name_list= []
        print("hello")
        f = plt.figure()
        print(plt.title(name_of_cell))
        f.set_figwidth(6)
        f.set_figheight(6)
        print(cap_fall,cap_rise)
        plt.plot(cap_fall,del_fall,color='blue',label='Cell Fall',marker='o',linestyle='dashed',markersize=12)
        plt.plot(cap_rise,del_rise,color='green',label='Cell Rise',marker='o',linestyle='dashed',markersize=12)
        plt.xlabel('Output Capacitance')
        plt.ylabel('Delay')
        mplcursors.cursor(hover=True)
        
        plt.legend(['CELL FALL','CELL RISE'],loc='upper left')
        plt.show()

def delay_vs_input_trans_graph(name_of_cell,tran_fall,tran_rise,del_fall,del_rise):
    
        f = plt.figure()
        plt.title(name_of_cell)
        f.set_figwidth(6)
        f.set_figheight(6)
        plt.plot(tran_fall,del_fall,color='blue',label='Cell Fall',marker='o',linestyle='dashed',markersize=12)
        plt.plot(tran_rise,del_rise,color='green',label='Cell Rise',marker='o',linestyle='dashed',markersize=12)
        plt.xlabel('Input Transition')
        plt.ylabel('Delay')
        mplcursors.cursor(hover=True)
        
        plt.legend(['CELL FALL','CELL RISE'],loc='upper left')
        plt.show()

