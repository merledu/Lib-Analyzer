def changeIndex(whichOne):
    file = open("index.js", "r")
    contents = file.readlines()
    file.close()

    if whichOne == "box":
        contents[11] = "win.loadURL('http://localhost:8008/box.html');\n"
    elif whichOne == "mainpage":
        contents[11] = "win.loadURL('http://localhost:8009/mainpage.html');\n"


    filW = open("index.js", "w")
    filW.write("".join(contents))
    filW.close()

