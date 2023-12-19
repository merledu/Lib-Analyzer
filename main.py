from weakref import ref
import finalfile1

import eel
import tkinter, tkinter.filedialog as tkFileDialog
import os
from eel import init,start
from icecream import ic
import time
from changeIndex import changeIndex
from util import get_port
from replacer import replacer
from port_manip import throw_port_json

if __name__ == '__main__':
    os.system('source external/bin/activate')
    init("web")

    
    global refFile
    refFile=""
    global targetFile
    targetFile =""

    @eel.expose
    def ask_reffile():
        
        root = tkinter.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        filepath = tkFileDialog.askopenfilename()

        

        z=filepath
        global refFile
        refFile = filepath
        print("working")
        eel.changeRefFile(filepath)
        
        
    @eel.expose
    def ask_targetfile():
        print("hello")
        root = tkinter.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        filepath = tkFileDialog.askopenfilename()

        global targetFile
        targetFile = filepath
        eel.changeTargetFile(filepath)


    @eel.expose
    def gen_details_go():
        import json
        dictionary_ref=finalfile1.Cell_info_extract(refFile)
        dictionary_ref.make_summary()
        if targetFile != "":
            dictionary_tar=finalfile1.Cell_info_extract(targetFile)
            dictionary_tar.make_summary()
            file_t = open("extract_results_tar.json", "w+")
            json.dump(dictionary_tar.dic, file_t)
            file_t.close()
        else:
            file = open("extract_results_tar.json", "w+")
            file.write("")
            file.close()

        file_r = open("extract_results_ref.json", "w+")
        json.dump(dictionary_ref.dic, file_r)
        file_r.close()

        fileStr = ""
        fileStr += refFile.split("/")[-1] + "\n"
        if targetFile != "":
            fileStr += targetFile.split("/")[-1]
        else:
            fileStr += " "
        

        file_file = open("files.txt", "w+")
        file_file.write(fileStr)
        file_file.close()

        time.sleep(5)
        ic("KHATAMMMMMMM")

        eel.finishLoading()
        os.system("./startbox.sh")
        


    #start("mainpage.html")
    changeIndex("mainpage")
    port2 = get_port()
    # replacer(port)
    throw_port_json(port2)
    start('web/mainpage.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron', '.'], port=port2)

