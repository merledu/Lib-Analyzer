from util import get_port
# from replacer import 
from port_manip import throw_port_json
def changeIndex(whichOne):    
    file = open("index.js", "r")
    contents = file.readlines()
    file.close()
    # port = get_port()
    # throw_port_json(port)

    if whichOne == "box":
        contents[11] = "win.loadURL(`http://localhost:${PORT.port}/box.html`);\n"
    elif whichOne == "mainpage":
        contents[11] = "win.loadURL(`http://localhost:${PORT.port}/mainpage.html`);\n"


    filW = open("index.js", "w")
    filW.write("".join(contents))
    filW.close()

