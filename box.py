from glob import glob
import eel
from eel import start, init
from changeIndex import changeIndex
from icecream import ic
from across_gate_analysis import delay_vs_output_cap_graph, delay_vs_input_trans_graph
from util import get_port
# from replacer import replacer
from port_manip import throw_port_json
if __name__ == "__main__":
    init("web")
    
    # global dic
    # dic = {}
    

    @eel.expose
    def keysLeKayAo():
        file = open("extract_results_ref.json")
        import json
        global dic
        global dic_t
        dic = json.loads(file.read())
        file.close()
        file = open("extract_results_tar.json")
        targetContent = file.read()
        if targetContent != "":
            dic_t = json.loads(targetContent)
        else:
            dic_t = {}
        file.close()
        ic(list(dic.keys()))
        eel.setCells(list(dic.keys()))
        eel.setCells2(list(dic_t.keys()))
        funcs = [dic[v]["function"] for v in list(dic.keys())]
        funcs = list(set(funcs))
        eel.setFuncs(funcs)
        funcs2 = [dic_t[v]["function"] for v in list(dic_t.keys())]
        funcs2 = list(set(funcs2))
        eel.setFuncs2(funcs2)
        file_file = open("files.txt")
        fileNames = file_file.read().split("\n")
        eel.changeFileNamess( fileNames[0], fileNames[1] )
        file_file.close()

    @eel.expose
    def bringCellDetailsPaleez(cell):
        eel.takeCellDetailsOK(cell,dic[cell]["function"], dic[cell]["area"], dic[cell]["leakage"], dic[cell]["pin_name"])
    
    @eel.expose
    def bringCellDetailsPaleez2(cell):
        eel.takeCellDetailsOK2(cell,dic_t[cell]["function"], dic_t[cell]["area"], dic_t[cell]["leakage"], dic_t[cell]["pin_name"])

    @eel.expose
    def bringPinDetailsPaleez(celloo):
        cell,pin = celloo.split("-")
        indexOfPin = dic[cell]["pin_name"].index(pin)
        eel.takePinDetailsOK(dic[cell]["max_transition"][indexOfPin], dic[cell]["max_capacitance"][indexOfPin])

    @eel.expose
    def bringPinDetailsPaleez2(celloo):
        cell,pin = celloo.split("-")
        indexOfPin = dic_t[cell]["pin_name"].index(pin)
        eel.takePinDetailsOK2(dic_t[cell]["max_transition"][indexOfPin], dic_t[cell]["max_capacitance"][indexOfPin])


    @eel.expose
    def doFuncThing(func,typee, name_of_file):
        if name_of_file == "ref":
            obj = dic
        elif name_of_file == "tar":
            obj = dic_t
        from across_gate_analysis import Area_vs_Leakage, plot_area_vs_rise_delay, plot_area_vs_fall_delay, plot_leakage_vs_fall_delay, plot_leakage_vs_rise_delay 
        if typee == "avd":
            Area_vs_Leakage(func, obj)
        elif typee == "avrd":
            plot_area_vs_rise_delay(func, obj)
        elif typee == "avfd":
            plot_area_vs_fall_delay(func, obj)
        elif typee == "lvfd":
            plot_leakage_vs_fall_delay(func, obj)
        elif typee == "lvrd":
            plot_leakage_vs_rise_delay(func, obj)


    @eel.expose
    def MakeGraphPlease(graphType, name_of_cell, name_of_file):
        ic(graphType, name_of_cell)
        if name_of_file == "ref":
            obj = dic
        elif name_of_file == "tar":
            obj = dic_t
        cap_fall = obj[name_of_cell]["Output Capacitance Fall"]
        cap_rise = obj[name_of_cell]["Output Capacitance Rise"]
        del_fall = obj[name_of_cell]["Delay Fall"]
        del_rise = obj[name_of_cell]["Delay Rise"]
        tran_fall = obj[name_of_cell]['Input Transition Fall']
        tran_rise = obj[name_of_cell]['Input Transition Rise']
        if graphType == "mtd":
            delay_vs_input_trans_graph(name_of_cell,tran_fall,tran_rise,del_fall,del_rise)
        elif graphType == "mcd":
            delay_vs_output_cap_graph(name_of_cell,cap_fall,cap_rise,del_fall,del_rise)
        
    @eel.expose
    def goToHome():
        eel.finishLoading()
        import os
        os.system("./startmain.sh")


    changeIndex("box")

    port1 = get_port()
    # replacer(port)
    throw_port_json(port1)
    start('box.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron', '.'], port=port1)
