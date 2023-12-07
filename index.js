const { app, BrowserWindow } = require('electron');

const createMainWindow = () => {
  const win = new BrowserWindow({show: false,webPreferences: {
    nodeIntegration: true
   } });
   win.maximize();
    
    win.show();
  
    // win.loadFile("index.html")
win.loadURL('http://localhost:8007/mainpage.html');
  }


app.whenReady().then(() => {
    createMainWindow()
});

function openTheMainWindow(){
  createMainWindow()
}


app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
});

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
