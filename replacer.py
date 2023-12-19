def replacer(port):
    file = open("index.js")
    content = file.readlines()
    file.close()

    line = content[22]
    if "createMainWindow" not in line:
        line = line.replace("","createMainWindow")
    content[22] = line
    print(content[22])

    line = content[12]
    content[12] = f"win.loadURL('http://localhost:{port}/mainpage.html');\n"

    file = open("index.js", "w")
    file.write("".join(content))
    file.close()