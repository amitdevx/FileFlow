import React, { useState, useEffect } from 'react';
import './App.css';
import Toolbar from './components/Toolbar';
import Breadcrumb from './components/Breadcrumb';
import FileList from './components/FileList';
import StatusBar from './components/StatusBar';
import SearchPanel from './components/SearchPanel';
import PreviewPanel from './components/PreviewPanel';
import ContextMenu from './components/ContextMenu';
import LoginPrompt from './components/LoginPrompt';
import { ThemeProvider } from './context/ThemeContext';
import { FileProvider, useFiles } from './context/FileContext';

function AppContent() {
  const [viewMode, setViewMode] = useState('list');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [showPreview, setShowPreview] = useState(true);
  const [contextMenu, setContextMenu] = useState(null);
  const [showRenameDialog, setShowRenameDialog] = useState(false);
  const [renameFile, setRenameFile] = useState(null);
  const [newFileName, setNewFileName] = useState('');
  
  const { files, deleteFiles, renameFile: doRename, isAuthenticated } = useFiles();
  
  const handleRename = (file) => {
    setRenameFile(file);
    setNewFileName(file.filename);
    setShowRenameDialog(true);
  };
  
  const handleRenameSubmit = async () => {
    if (newFileName.trim() && newFileName !== renameFile.filename) {
      await doRename(renameFile.id, newFileName.trim());
    }
    setShowRenameDialog(false);
    setRenameFile(null);
    setNewFileName('');
    setSelectedFiles([]);
  };
  
  const handleDelete = async (filesToDelete) => {
    if (filesToDelete && filesToDelete.length > 0) {
      const message = filesToDelete.length === 1 
        ? `Delete "${filesToDelete[0].filename}"?`
        : `Delete ${filesToDelete.length} items?`;
      
      if (window.confirm(message)) {
        await deleteFiles(filesToDelete.map(f => f.id));
        setSelectedFiles([]);
      }
    }
  };
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't trigger shortcuts when typing in input fields
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }
      
      // Ctrl/Cmd + A: Select all
      if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
        e.preventDefault();
        setSelectedFiles(files || []);
      }
      // Delete: Delete selected files
      if (e.key === 'Delete' && selectedFiles.length > 0) {
        e.preventDefault();
        handleDelete(selectedFiles);
      }
      // F2: Rename
      if (e.key === 'F2' && selectedFiles.length === 1) {
        e.preventDefault();
        handleRename(selectedFiles[0]);
      }
      // Escape: Clear selection
      if (e.key === 'Escape') {
        setSelectedFiles([]);
        setContextMenu(null);
        setShowRenameDialog(false);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFiles, files]);
  
  return (
    <div className="App">
      <header className="App-header">
        <h1><i className="fas fa-cloud"></i> FileFlow</h1>
      </header>
      
      <Toolbar 
        viewMode={viewMode}
        setViewMode={setViewMode}
        selectedFiles={selectedFiles}
        onRename={handleRename}
        onDelete={handleDelete}
      />
      
      <SearchPanel />
      
      <main className="App-main">
        <div className="file-browser">
          <Breadcrumb />
          <FileList 
            viewMode={viewMode}
            selectedFiles={selectedFiles}
            setSelectedFiles={setSelectedFiles}
            onContextMenu={setContextMenu}
          />
        </div>
        
        {showPreview && selectedFiles.length === 1 && (
          <PreviewPanel 
            selectedFile={selectedFiles[0]}
            onClose={() => setShowPreview(false)}
          />
        )}
      </main>
      
      <StatusBar 
        selectedCount={selectedFiles.length}
        totalFiles={files?.length || 0}
      />
      
      {contextMenu && (
        <ContextMenu 
          x={contextMenu.x}
          y={contextMenu.y}
          selectedFiles={selectedFiles}
          onClose={() => {
            setContextMenu(null);
            setSelectedFiles([]);
          }}
        />
      )}
      
      {/* Rename Dialog */}
      {showRenameDialog && (
        <div className="dialog-overlay">
          <div className="dialog">
            <h3>Rename</h3>
            <input
              type="text"
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleRenameSubmit();
                if (e.key === 'Escape') setShowRenameDialog(false);
              }}
              autoFocus
              onFocus={(e) => {
                // Select filename without extension
                const lastDot = newFileName.lastIndexOf('.');
                if (lastDot > 0) {
                  e.target.setSelectionRange(0, lastDot);
                } else {
                  e.target.select();
                }
              }}
            />
            <div className="dialog-buttons">
              <button onClick={() => setShowRenameDialog(false)}>Cancel</button>
              <button onClick={handleRenameSubmit} className="primary">Rename</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <FileProvider>
        <AppContent />
      </FileProvider>
    </ThemeProvider>
  );
}

export default App;
