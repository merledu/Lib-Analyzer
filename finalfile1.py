from os import times
from pydoc import doc
import re
from pathlib import *
import string
import time
import csv
import numpy as np
import statistics
import termcolor
import getpass
time_of_cellname_extract=int()
time_of_max_trans_extract=int()
time_of_fiteration=int()
time_of_fiteration1=int()
time_of_pinname_extract=int()
time_of_direction_extract=int()
time_of_function_extract=int()
time_of_area_extract=int()
time_of_leakage_power_extract=int()
time_of_extract_max_cap=int()
time_of_extract_max_delay_fall=int()
time_of_extract_max_delay_rise=int()

class Cell_info_extract():
    def __init__(self,path:string):
        self.path=path
        self.dic=dict()
        self.total_cell_info={}
        if 'sky' in self.path:
            print('This is SKY')
            self.open1=open('cell_info(sky).csv','w').close()
            self.open1=open('cell_info(sky).csv','a')
            self.write1=csv.writer(self.open1)
        
        else:
            print('This is another lib file')
            self.open1=open('cell_info(anotherlib).csv','w').close()
            self.open1=open('cell_info(anotherlib).csv','a')
            self.write1=csv.writer(self.open1)

        # Extract cell info in list:
        cell_name,cell_span=self.extract_cell_name(self.path)

        # Extract Usefull info from each cell's info:
        self.filter(cell_name,cell_span,self.path)

        # Make a summary file:
        #self.make_summary()
    
    def extract_cell_name(self,path):
        global time_of_cellname_extract
        start=time.time()
        file  = open(path,'r')
        content = file.read()
        cellname=[]
        cellspan=[]
        #for cell names
        ab= re.finditer('(cell\s*\()"(.*?)"(\))',content)
        for i in ab:
            if i[2]=='':
                continue
            cellname.append(i[2])
            cellspan.append(i.span())
        end=time.time()
        time_of_cellname_extract+=end-start
        return cellname,cellspan

    def filter(self,cellname:list,cellspan:list,path:str):
        global time_of_fiteration1
       
        self.write1.writerow(['Cell Name','Pin name','Direction','Max Transition','Area','Function',\
            'Leakage Power','Max_Cap','Input Transition Fall','Input Transition Rise',\
                'Output Capacitance Fall','Output Capacitance Rise','Delay Fall','Delay Rise'\
                    ,'Delay Value Fall','Delay Value Rise','Max Pin Delay Fall','Max Pin Delay Rise'])
        f1=open(path,'r')
        r1=f1.read()
        for i,j in zip(cellname,cellspan):
            if cellspan.index(j)==len(cellspan)-1:
                start1=time.time()
                self.total_cell_info[i]=r1[j[0]:]
                end1=time.time()
                time_of_fiteration1+=end1-start1
            else:
                start1=time.time()
                self.total_cell_info[i]=r1[j[0]:cellspan[cellspan.index(j)+1][1]]
                end1=time.time()
                time_of_fiteration1+=end1-start1

            pins,direction,max_trans,max_cap,max_in1_list_fall,max_in1_list_rise\
                ,max_in2_list_fall,max_in2_list_rise,max_delay_list_fall,max_delay_list_rise,max_delay_val_fall\
                    ,max_delay_val_rise,max_pin_fall,max_pin_rise=self.extract_pin_name(i,self.total_cell_info[i])
            
            if direction is None:
                termcolor.cprint(f'{i} is fail to extract the information','red')
                continue

            else:
                termcolor.cprint(f'{i} is pass to extract the information','green')
                area=self.extract_area_of_cell(self.total_cell_info[i])
                fun=self.extract_function_of_cell(self.total_cell_info[i])
                leakage=self.extract_leakage_power(self.total_cell_info[i])
                self.dic[i]={}
                self.dic[i]['pin_name']=pins
                self.dic[i]['direction']=direction
                self.dic[i]['max_transition']=max_trans
                self.dic[i]['max_capacitance']=max_cap
                self.dic[i]['area']=area
                self.dic[i]['function']=fun
                self.dic[i]['leakage']=leakage
                self.dic[i]['Input Transition Fall']=max_in1_list_fall
                self.dic[i]['Input Transition Rise']=max_in1_list_rise
                self.dic[i]['Output Capacitance Fall']=max_in2_list_fall
                self.dic[i]['Output Capacitance Rise']=max_in2_list_rise
                self.dic[i]['Delay Fall']=max_delay_list_fall
                self.dic[i]['Delay Rise']=max_delay_list_rise
                self.dic[i]['Max Delay Value Fall']=max_delay_val_fall
                self.dic[i]['Max Delay Value Rise']=max_delay_val_rise
                self.dic[i]['Max Pin Delay Fall']=max_pin_fall
                self.dic[i]['Max Pin Delay Rise']=max_pin_rise
                self.write1.writerow([i,pins,direction,max_trans,area,fun,leakage,max_cap,\
                    max_in1_list_fall,max_in1_list_rise,max_in2_list_fall,max_in2_list_rise,\
                        max_delay_list_fall,max_delay_list_rise,max_delay_val_fall,max_delay_val_rise,\
                            max_pin_fall,max_pin_rise])
        f1.close()
        self.open1.close()

    def extract_direction_of_pins(self,cell_info):
        start1=time.time()
        global time_of_direction_extract
        dir = re.findall('(\s*direction\s*:\s*)"?(.[^;"]*)',cell_info)

        if dir:
            end1=time.time()
            time_of_direction_extract+=end1-start1
            return str(dir[0][1]).rstrip(' ')
        else:
            end1=time.time()
            time_of_direction_extract+=end1-start1
            return 'Not Available'

    def extract_pin_name(self,cell_name,cell_info):
        start=time.time()
        global time_of_pinname_extract
        pin_name=[]
        direction=[]
        max_trans=[]
        max_cap=[]
        max_in1_list_fall=list()
        max_in2_list_fall=list()
        max_delay_list_fall=list()
        max_delay_val_fall=float()
        max_pin_fall=str()
        max_in1_list_rise=list()
        max_in2_list_fall=list()
        max_in2_list_rise=list()
        max_delay_list_rise=list()
        max_delay_val_rise=float()
        max_pin_rise=str()
        pins=re.finditer('(\spin\s*\()"?(.[^"|^)]*)',cell_info)

        if pins:
            end=time.time()
            time_of_pinname_extract+=end-start
            pins=list(pins)
            for i in pins:
                if pins.index(i) == len(pins)-1:
                    max= self.extract_max_transition_of_pins(cell_info[i.span()[0]:])
                    direct=self.extract_direction_of_pins(cell_info[i.span()[0]:])
                    cap=self.extract_max_capacitance(cell_info[i.span()[0]:])

                    if 'output' in direction and direct=='output':
                        return None,None,None,None,None,None,None,None,None,None,None,None,None,None

                    if 'output' not in direction and direct!='output':
                        direction.append(direct)
                        max_cap.append(cap)
                        pin_name.append(i[2])
                        max_trans.append(max)

                    elif direct=='output':
                        direction.insert(len(direction),direct)
                        max_cap.insert(len(max_cap),cap)
                        pin_name.insert(len(pin_name),i[2])
                        max_trans.insert(len(max_trans),max)
                        max_in1_list_fall,max_in2_list_fall,max_delay_list_fall,max_delay_val_fall,max_pin_fall=\
                        self.cell_fall_matrix_extract(cell_info[i.span()[0]:])
                        max_in1_list_rise,max_in2_list_rise,max_delay_list_rise,max_delay_val_rise,max_pin_rise=\
                        self.cell_rise_matrix_extract(cell_info[i.span()[0]:])
                        #self.output_info[cell_name]=cell_info[i.span()[0]:]
                    else:
                        direction.insert(len(direction)-1,direct)
                        max_cap.insert(len(max_cap)-1,cap)
                        pin_name.insert(len(pin_name)-1,i[2])
                        max_trans.insert(len(max_trans)-1,max)

                else:
                    max=self.extract_max_transition_of_pins(cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]])
                    direct=self.extract_direction_of_pins(cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]])
                    cap=self.extract_max_capacitance(cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]])

                    if 'output' in direction and direct=='output':
                        return  None,None,None,None,None,None,None,None,None,None,None,None,None,None

                    if 'output' not in direction and direct!='output':
                        direction.append(direct)
                        max_cap.append(cap)
                        pin_name.append(i[2])
                        max_trans.append(max)

                    elif direct=='output':
                        direction.insert(len(direction),direct)
                        max_cap.insert(len(max_cap),cap)
                        pin_name.insert(len(pin_name),i[2])
                        max_trans.insert(len(max_trans),max)
                        max_in1_list_fall,max_in2_list_fall,max_delay_list_fall,max_delay_val_fall,max_pin_fall=\
                        self.cell_fall_matrix_extract(cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]])

                        max_in1_list_rise,max_in2_list_rise,max_delay_list_rise,max_delay_val_rise,max_pin_rise=\
                        self.cell_rise_matrix_extract(cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]])
                        
                        #self.output_info[cell_name]=cell_info[i.span()[0]:pins[pins.index(i)+1].span()[1]]
                    else:
                        direction.insert(len(direction)-1,direct)
                        max_cap.insert(len(max_cap)-1,cap)
                        pin_name.insert(len(pin_name)-1,i[2])
                        max_trans.insert(len(max_trans)-1,max)
                        
        #print(pin_name,direction,max_cap,max_trans)
        if direction.count('input')>=1 and direction.count('output')==1:
            return pin_name,direction,max_trans,max_cap,max_in1_list_fall,max_in1_list_rise,\
                max_in2_list_fall,max_in2_list_rise,max_delay_list_fall,max_delay_list_rise,\
                    max_delay_val_fall,max_delay_val_rise,max_pin_fall,max_pin_rise
        else:
            return None,None,None,None,None,None,None,None,None,None,None,None,None,None

    def extract_max_transition_of_pins(self,cell_info):
        start1=time.time()
        global time_of_max_trans_extract
        trans=re.findall("(\s*max_transition\s*:)(.[^;]*)",cell_info)

        if trans:
            end1=time.time()
            time_of_max_trans_extract+=end1-start1
            return eval(trans[0][1])
        else:
            end1=time.time()
            time_of_max_trans_extract+=end1-start1
            return 'Not Available'

    def extract_area_of_cell(self,cell_info):
        start1=time.time()
        global time_of_area_extract
        area=re.search("(\s*area\s*:)(.[^;]*)",cell_info)
        if area :
            end1=time.time()
            time_of_area_extract+=end1-start1
            return float(area[2])
        else:
            end1=time.time()
            time_of_area_extract+=end1-start1
            return 'Not Available'

    def extract_function_of_cell(self,cell_info):
        start1=time.time()
        global time_of_function_extract
        func1=re.search('(\s*function\s*:)\s*"?(.[^;"]*)',cell_info)

        if func1:
            end1=time.time()
            time_of_function_extract+=end1-start1
            return str(func1[2].replace(' ',''))
        else:
            end1=time.time()
            time_of_function_extract+=end1-start1
            return 'Not Available'


    def extract_leakage_power(self,cell_info):
        start1=time.time()
        global time_of_leakage_power_extract
        leakage=re.search('(\s*cell_leakage_power :)\s*?(.[^;]*)',cell_info)
        if leakage:
            if leakage[2]!=None:
                end1=time.time()
                time_of_leakage_power_extract+=end1-start1
                return float(leakage[2])

            else:
                end1=time.time()
                time_of_leakage_power_extract+=end1-start1
                return 'Not Available'
    
    def extract_max_capacitance(self,cell_info):
        start1=time.time()
        global time_of_extract_max_cap
        max_cap=re.search('(\scapacitance\s*:)\s*(.[^;]*)',cell_info)
        if max_cap:
            if max_cap[2]!=None:
                end1=time.time()
                time_of_extract_max_cap+=end1-start1
                return float(max_cap[2])
            
        else:
            end1=time.time()
            time_of_extract_max_cap+=end1-start1
            return 'Not Available'
    
    def cell_fall_matrix_extract(self,cell_info):
        start1=time.time()
        global time_of_extract_max_delay_fall
        timesec=re.finditer('\s*timing.*\(\).*',cell_info)
        if timesec:
            max_pin=str(' ')
            max_in1_list=None
            max_in2_list=None
            max_delay_val=float(0)
            max_delay_list=[0]
            timesec=list(timesec)
            for i in timesec:
                if timesec.index(i)==len(timesec)-1:
                    relpin=re.search('(\srelated_pin.*:)\s*"?(.[^;"]*)',cell_info[i.span()[0]:])
                    in1=re.search('(\s*cell_fall.*)\n(\s*index_1\()"?(.[^");]*)',cell_info[i.span()[0]:])
                    in2=re.search('(\s*cell_fall.*)(\n.*){2}(\s*index_2\()"?(.[^");]*)',\
                        cell_info[i.span()[0]:])
                    val1=re.search('(\s*cell_fall.*)(\n.*){2}(\s*values\("?)(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)'\
                        ,cell_info[i.span()[0]:])

                    if in1 and in2 and val1:
                        delay_mat=eval('['+val1[4].replace('"','').replace('\\','')+val1[5].replace('"','').replace('\\','').replace(' ','')\
                            +val1[6].replace('"','').replace('\\','').replace(' ','')\
                                +val1[7].replace('"','').replace('\\','').replace(' ','')\
                                +val1[8].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[9].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[10].replace('"','').replace(')','').replace(';','').replace(' ','')+']')
                        delay_mat=np.array(delay_mat)
                        delay_mat= np.reshape(delay_mat,(7,7))

                       
                        if in1[3]!=None and in2[4]!=None and val1:
                            medvalin1=statistics.median(eval('['+in1[3]+']'))
                            medvalin2=statistics.median(eval('['+in2[4]+']'))
                            medinin1=eval('['+in1[3]+']').index(medvalin1)
                            medinin2=eval('['+in2[4]+']').index(medvalin2)
                            if delay_mat[medinin1][medinin2] > max_delay_val:
                                max_delay_val=delay_mat[medinin1][medinin2]
                                max_delay_list=delay_mat[medinin1].tolist()
                                max_pin=max_pin.replace(max_pin[:],relpin[2])
                                max_in1_list=eval('['+in1[3]+']')
                                max_in2_list=eval('['+in2[4]+']')
                else:
                    relpin=re.search('(\srelated_pin.*:)\s*"?(.[^;"]*)',cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    in1=re.search('(\s*cell_fall.*)\n(\s*index_1\()"?(.[^");]*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    in2=re.search('(\s*cell_fall.*)(\n.*){2}(\s*index_2\()"?(.[^");]*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    val1=re.search('(\s*cell_fall.*)(\n.*){2}(\s*values\("?)(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])

                    if in1 and in2 and val1:
                        delay_mat=eval('['+val1[4].replace('"','').replace('\\','')+val1[5].replace('"','').replace('\\','').replace(' ','')\
                            +val1[6].replace('"','').replace('\\','').replace(' ','')\
                                +val1[7].replace('"','').replace('\\','').replace(' ','')\
                                +val1[8].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[9].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[10].replace('"','').replace(')','').replace(';','').replace(' ','')+']')
                        delay_mat=np.array(delay_mat)
                        #print(relpin[2],delay_mat)
                        delay_mat = np.reshape(delay_mat,(7,7))

                        if in1[3]!=None and in2[4]!=None and val1:
                            medvalin1=statistics.median(eval('['+in1[3]+']'))
                            medvalin2=statistics.median(eval('['+in2[4]+']'))
                            medinin1=eval('['+in1[3]+']').index(medvalin1)
                            medinin2=eval('['+in2[4]+']').index(medvalin2)
                            if delay_mat[medinin1][medinin2] > max_delay_val:
                                max_delay_val=delay_mat[medinin1][medinin2]
                                max_delay_list=delay_mat[medinin1].tolist()
                                max_pin=max_pin.replace(max_pin[:],relpin[2])
                                max_in1_list=eval('['+in1[3]+']')
                                max_in2_list=eval('['+in2[4]+']')
            end1=time.time()
            time_of_extract_max_delay_fall+=end1-start1
            return max_in1_list,max_in2_list,max_delay_list,max_delay_val,max_pin
    
    
    def cell_rise_matrix_extract(self,cell_info):
        start1=time.time()
        global time_of_extract_max_delay_rise
        timesec=re.finditer('\s*timing.*\(\).*',cell_info)
        if timesec:
            max_pin=str(' ')
            max_in1_list=None
            max_in2_list=None
            max_delay_val=float(0)
            max_delay_list=[0]
            timesec=list(timesec)
            for i in timesec:
                if timesec.index(i)==len(timesec)-1:
                    relpin=re.search('(\srelated_pin.*:)\s*"?(.[^;"]*)',cell_info[i.span()[0]:])
                    in1=re.search('(\s*cell_rise.*)\n(\s*index_1\()"?(.[^");]*)',cell_info[i.span()[0]:])
                    in2=re.search('(\s*cell_rise.*)(\n.*){2}(\s*index_2\()"?(.[^");]*)',\
                        cell_info[i.span()[0]:])
                    val1=re.search('(\s*cell_rise.*)(\n.*){2}(\s*values\("?)(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)'\
                        ,cell_info[i.span()[0]:])
                  
                    if in1 and in2 and val1:
                        delay_mat=eval('['+val1[4].replace('"','').replace('\\','')+val1[5].replace('"','').replace('\\','').replace(' ','')\
                            +val1[6].replace('"','').replace('\\','').replace(' ','')\
                                +val1[7].replace('"','').replace('\\','').replace(' ','')\
                                +val1[8].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[9].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[10].replace('"','').replace(')','').replace(';','').replace(' ','')+']')
                        delay_mat=np.array(delay_mat)
                        delay_mat= np.reshape(delay_mat,(7,7))


                        if in1[3]!=None and in2[4]!=None and val1:
                            medvalin1=statistics.median(eval('['+in1[3]+']'))
                            medvalin2=statistics.median(eval('['+in2[4]+']'))
                            medinin1=eval('['+in1[3]+']').index(medvalin1)
                            medinin2=eval('['+in2[4]+']').index(medvalin2)
                            if delay_mat[medinin1][medinin2] > max_delay_val:
                                max_delay_val=delay_mat[medinin1][medinin2]
                                max_delay_list=delay_mat[medinin1].tolist()
                                max_pin=max_pin.replace(max_pin[:],relpin[2])
                                max_in1_list=eval('['+in1[3]+']')
                                max_in2_list=eval('['+in2[4]+']')
                else:
                    relpin=re.search('(\srelated_pin.*:)\s*"?(.[^;"]*)',cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    in1=re.search('(\s*cell_rise.*)\n(\s*index_1\()"?(.[^");]*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    in2=re.search('(\s*cell_rise.*)(\n.*){2}(\s*index_2\()"?(.[^");]*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])
                    val1=re.search('(\s*cell_rise.*)(\n.*){2}(\s*values\("?)(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)'\
                        ,cell_info[i.span()[0]:timesec[timesec.index(i)+1].span()[1]])

                    if in1 and in2 and val1:
                        delay_mat=eval('['+val1[4].replace('"','').replace('\\','')+val1[5].replace('"','').replace('\\','').replace(' ','')\
                            +val1[6].replace('"','').replace('\\','').replace(' ','')\
                                +val1[7].replace('"','').replace('\\','').replace(' ','')\
                                +val1[8].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[9].replace('"','').replace('\\','').replace(' ','')\
                                    +val1[10].replace('"','').replace(')','').replace(';','').replace(' ','')+']')
                        #print(relpin[2],delay_mat)
                        delay_mat=np.array(delay_mat)
                        delay_mat = np.reshape(delay_mat,(7,7))
                        
                
                        if in1[3]!=None and in2[4]!=None and val1:
                            medvalin1=statistics.median(eval('['+in1[3]+']'))
                            medvalin2=statistics.median(eval('['+in2[4]+']'))
                            medinin1=eval('['+in1[3]+']').index(medvalin1)
                            medinin2=eval('['+in2[4]+']').index(medvalin2)
                            if delay_mat[medinin1][medinin2] > max_delay_val:
                                max_delay_val=delay_mat[medinin1][medinin2]
                                max_delay_list=delay_mat[medinin1].tolist()
                                max_pin=max_pin.replace(max_pin[:],relpin[2])
                                max_in1_list=eval('['+in1[3]+']')
                                max_in2_list=eval('['+in2[4]+']')
            end1=time.time()
            time_of_extract_max_delay_rise+=end1-start1
            return max_in1_list,max_in2_list,max_delay_list,max_delay_val,max_pin  
    
    def make_summary(self):
        counter=0
        distinct_name_of_cell={}
        
        if 'sky' in self.path:
            function=open(f'/home/{getpass.getuser()}/Desktop/summary_csv(sky).csv','w').close()
            function=open(f'/home/{getpass.getuser()}/Desktop/summary_csv(sky).csv','a')
            write1=csv.writer(function)
            write1.writerow(['Distinct Cell Name','Total Cells','Cell list','Function List',\
                'Area List','No of Input List'])
        else:
            termcolor.cprint("WARNING!!! This file related to another technology so, please test the Lib Analyzer Software Again","orange")
            termcolor.cprint("Maybe there is no summary data generated regarding this anonymos technology","orange")
            function=open('function_based_summary(others)','w').close()
            function=open('function_based_summary(others)','a')
        for i in self.dic.keys():
            sky=re.search('(.*__)(.*)(_.*)',i)
            if sky:
                name=re.sub('\d','',sky[2])

            if name not in distinct_name_of_cell:
                counter+=1
                distinct_name_of_cell[name]={}
                distinct_name_of_cell[name]['no._of_cells']=int(1)
                distinct_name_of_cell[name]['name_of_cell']=[]
                distinct_name_of_cell[name]['function']=[]
                distinct_name_of_cell[name]['Area']=[]
                distinct_name_of_cell[name]['number_of_inputs']=[]
                distinct_name_of_cell[name]['name_of_cell'].append(i)
                distinct_name_of_cell[name]['function'].append(self.dic[i]['function'])
                distinct_name_of_cell[name]['Area'].append(self.dic[i]['area'])
                distinct_name_of_cell[name]['number_of_inputs'].append(self.dic[i]['direction'].count('input'))
            else:
                distinct_name_of_cell[name]['no._of_cells']+=1
                distinct_name_of_cell[name]['name_of_cell'].append(i)
                distinct_name_of_cell[name]['Area'].append(self.dic[i]['area'])
                distinct_name_of_cell[name]['function'].append(self.dic[i]['function'])
                distinct_name_of_cell[name]['number_of_inputs'].append(self.dic[i]['direction'].count('input'))
        
        for i in distinct_name_of_cell.keys():
            write1.writerow([i,len(distinct_name_of_cell[i]['name_of_cell'])\
                ,distinct_name_of_cell[i]['name_of_cell']\
                ,distinct_name_of_cell[i]['function'],distinct_name_of_cell[i]['Area']\
                    ,distinct_name_of_cell[i]['number_of_inputs']])
        
        
       
                

#Cell=Cell_info_extract('/home/mmohsin/eelgui/skylibfiles/sky130_fd_sc_hd__tt_025C_1v80.lib')


#Cell.cell_rise_matrix_extract(Cell.output_info['sky130_fd_sc_hd__xor3_1'])


#Cell.cell_fall_matrix_extract(Cell.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_max_capacitance(Cell.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_pin_name(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_max_transition_of_pins(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_direction_of_pins(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])

#
#Cell.extract_area_of_cell(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_function_of_cell(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])


#Cell.extract_leakage_power(self.total_cell_info['sky130_fd_sc_hd__xor3_1'])