const fs = require('fs');
const {app, BrowserWindow, ipcMain, dialog} = require('electron');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const {promisify} = require('util');

const userDataPath = app.getPath('appData'); // Get the AppData path
const myTpoPath = path.join(userDataPath, 'MyTPO'); // Path to the MyTPO folder
const dbPathFile = path.join(myTpoPath, 'Paths.json'); // Path to the DB path file

// Create the MyTPO directory if it doesn't exist
if (!fs.existsSync(myTpoPath)) {
  fs.mkdirSync(myTpoPath, {recursive: true});
}

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1920, height: 1080, webPreferences: {
      preload: path.join(__dirname, 'electron-preload.js'),
      contextIsolation: true,
      enableRemoteModule: false,
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL('http://localhost:9000'); // Your Vue app URL
  mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  ipcMain.handle('set-data', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'], filters: [{name: 'Database Files', extensions: ['db', 'sqlite']}]
    });
    if (result.filePaths.length > 0) {
      const dbPath = result.filePaths[0];
      let json_result = JSON.parse(fs.readFileSync(dbPathFile));
      json_result.dataDB = dbPath;
      fs.writeFileSync(dbPathFile, JSON.stringify(json_result));
      return dbPath.toString();
    }
    return null;
  });
  ipcMain.handle('set-records', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'], filters: [{name: 'Database Files', extensions: ['db', 'sqlite']}]
    });
    if (result.filePaths.length > 0) {
      const dbPath = result.filePaths[0];
      let json_result = JSON.parse(fs.readFileSync(dbPathFile));
      json_result.recordsDB = dbPath;
      fs.writeFileSync(dbPathFile, JSON.stringify(json_result));
      return dbPath.toString();
    }
    return null;
  });
  ipcMain.handle('set-audio', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory'],
    });
    if (result.filePaths.length > 0) {
      const dbPath = result.filePaths[0];
      let json_result = JSON.parse(fs.readFileSync(dbPathFile));
      json_result.audioPath = dbPath;
      fs.writeFileSync(dbPathFile, JSON.stringify(json_result));
      return dbPath.toString();
    }
    return null;
  });

  ipcMain.handle('get-data', () => {
    if (fs.existsSync(dbPathFile)) {
      const data = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8'));
      return data.dataDB;
    }
    return '';
  });
  ipcMain.handle('get-records', () => {
    if (fs.existsSync(dbPathFile)) {
      const data = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8'));
      return data.recordsDB;
    }
    return '';
  });
  ipcMain.handle('get-audio', () => {
    if (fs.existsSync(dbPathFile)) {
      const data = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8'));
      return data.audioPath.toString();
    }
    return '';
  });

  ipcMain.handle('test-db-connection', () => {
    if (!fs.existsSync(dbPathFile)) {
      fs.writeFileSync(dbPathFile, JSON.stringify({dataDB: '', recordsDB: '', audioPath: ''}))
    }

    const data = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8')).dataDB;
    const records = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8')).recordsDB;
    const audio = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8')).audioPath;

    let result = [data !== '', records !== '', audio !== ''];

    const dataDB = new sqlite3.Database(data, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        console.error(err.message);
        result[0] = false
      }
    });

    const recordsDB = new sqlite3.Database(records, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        console.error(err.message);
        result[1] = false
      }
    });

    const audioPath = new sqlite3.Database(audio, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        console.error(err.message);
        result[2] = false
      }
    });

    return result;
  });

  ipcMain.handle('data-sql', async (event, sql, params) => {
    const dbPath = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8')).dataDB.toString();
    const db = new sqlite3.Database(dbPath);
    const all = promisify(db.all.bind(db));
    try {
      return await all(sql, params);
    } catch (error) {
      throw new Error(`Database query failed: ${error.message}`);
    } finally {
      db.close();
    }
  });

  ipcMain.handle('records-sql', async (event, sql, params) => {
    const dbPath = JSON.parse(fs.readFileSync(dbPathFile, 'utf-8')).audioPath.toString();
    const db = new sqlite3.Database(dbPath);
    const all = promisify(db.all.bind(db));
    try {
      return await all(sql, params);
    } catch (error) {
      throw new Error(`Database query failed: ${error.message}`);
    } finally {
      db.close();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
