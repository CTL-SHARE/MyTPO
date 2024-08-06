/**
 * This file is used specifically for security reasons.
 * Here you can access Nodejs stuff and inject functionality into
 * the renderer thread (accessible there through the "window" object)
 *
 * WARNING!
 * If you import anything from node_modules, then make sure that the package is specified
 * in package.json > dependencies and NOT in devDependencies
 *
 * Example (injects window.myAPI.doAThing() into renderer thread):
 *
 *   import { contextBridge } from 'electron'
 *
 *   contextBridge.exposeInMainWorld('myAPI', {
 *     doAThing: () => {}
 *   })
 *
 * WARNING!
 * If accessing Node functionality (like importing @electron/remote) then in your
 * electron-main.js you will need to set the following when you instantiate BrowserWindow:
 *
 * mainWindow = new BrowserWindow({
 *   // ...
 *   webPreferences: {
 *     // ...
 *     sandbox: false // <-- to be able to import @electron/remote in preload script
 *   }
 * }
 */

const {contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld('electron', {
  setData: () => ipcRenderer.invoke('set-data'),
  setRecords: () => ipcRenderer.invoke('set-records'),
  setAudio: () => ipcRenderer.invoke('set-audio'),

  getData: () => ipcRenderer.invoke('get-data'),
  getRecords: () => ipcRenderer.invoke('get-records'),
  getAudio: () => ipcRenderer.invoke('get-audio'),

  testDBConn: () => ipcRenderer.invoke('test-db-connection'),

  dataSQL: (sql, params) => ipcRenderer.invoke('data-sql', sql, params),
  recordsSQL: (sql, params) => ipcRenderer.invoke('records-sql', sql, params)

  // openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
  // getDbPath: () => ipcRenderer.invoke('get-db-path'),
  // executeSql: (sql, params) => ipcRenderer.invoke('execute-sql', sql, params)
});
