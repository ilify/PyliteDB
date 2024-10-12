const { app, BrowserWindow, ipcMain,helmet } = require('electron')
const path = require('path');
const { exec } = require('child_process');


let Window;


const createWindow = () => {
    Window = new BrowserWindow({
        width: 1600,
        height: 900,
        titleBarStyle: 'hidden',
        frame: false,
        resizable: false,
        icon: path.join(__dirname, 'Frontend/Images/Logo.ico'),
        webPreferences: {
            nodeIntegration: true,
            devTools: true,
            contextIsolation: false,
            webSecurity: false,  // Disable web security if you encounter CORS issues
        }
    })
    Window.loadURL("http://127.0.0.1:5000")
    Window.setMenuBarVisibility(false)
    // Window.webContents.openDevTools()

}
app.whenReady().then(() => {
    //get path of the python file
    const scriptPath = path.join(__dirname, 'Server.py');
    exec('python -u ' + scriptPath, (error, stdout, stderr) => {
        if (error) {
            console.error(`Flask start error: ${error}`);
            return;
        }
        console.log(`Flask output: ${stdout}`);
        createWindow();
    });
    createWindow()
})


app.on('window-all-closed', () => {
    app.quit()
    //close all the python processes
    exec('taskkill /F /IM python.exe')
})

ipcMain.on('AppClose', () => {
    Window.close()
})

ipcMain.on('AppMin', () => {
    Window.minimize()
})
ipcMain.on('AppMax', () => {
    if (Window.isMaximized()) {
        Window.unmaximize()
    } else {
        Window.maximize()
    }
})