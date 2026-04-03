import React, { useRef, useState } from 'react';
import { useFiles } from '../context/FileContext';
import './Toolbar.css';

function Toolbar({ viewMode, setViewMode, selectedFiles, onRename, onDelete }) {
  const { goBack, goForward, uploadFile, createFolder, history, historyIndex } = useFiles();
  const fileInputRef = useRef(null);
  const [showNewFolderDialog, setShowNewFolderDialog] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        await uploadFile(files[i]);
      }
      e.target.value = ''; // Reset input
    }
  };

  const handleNewFolder = () => {
    setShowNewFolderDialog(true);
    setNewFolderName('New Folder');
  };

  const handleCreateFolder = async () => {
    if (newFolderName.trim()) {
      await createFolder(newFolderName.trim());
      setShowNewFolderDialog(false);
      setNewFolderName('');
    }
  };

  const handleCancelFolder = () => {
    setShowNewFolderDialog(false);
    setNewFolderName('');
  };

  return (
    <div className="toolbar">
      <div className="toolbar-group">
        <button 
          title="Back" 
          onClick={goBack}
          disabled={historyIndex <= 0}
        >
          <i className="fas fa-arrow-left"></i>
        </button>
        <button 
          title="Forward" 
          onClick={goForward}
          disabled={historyIndex >= history.length - 1}
        >
          <i className="fas fa-arrow-right"></i>
        </button>
      </div>
      
      <div className="toolbar-group">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          multiple
        />
        <button title="Upload" onClick={handleUploadClick}>
          <i className="fas fa-upload"></i> Upload
        </button>
        <button title="New Folder" onClick={handleNewFolder}>
          <i className="fas fa-folder-plus"></i> New Folder
        </button>
      </div>
      
      <div className="toolbar-group">
        <button 
          disabled={!selectedFiles || selectedFiles.length !== 1} 
          title="Rename"
          onClick={() => onRename && onRename(selectedFiles[0])}
        >
          <i className="fas fa-pen"></i> Rename
        </button>
        <button 
          disabled={!selectedFiles || selectedFiles.length === 0} 
          title="Delete"
          onClick={() => onDelete && onDelete(selectedFiles)}
        >
          <i className="fas fa-trash"></i> Delete
        </button>
        <button 
          disabled={!selectedFiles || selectedFiles.length !== 1 || selectedFiles[0]?.is_folder} 
          title="Download"
          onClick={() => {
            if (selectedFiles && selectedFiles[0]) {
              window.open(`/download_file/${selectedFiles[0].id}`, '_blank');
            }
          }}
        >
          <i className="fas fa-download"></i> Download
        </button>
      </div>
      
      <div className="toolbar-group view-controls">
        <button 
          className={viewMode === 'list' ? 'active' : ''}
          onClick={() => setViewMode('list')}
          title="List View"
        >
          <i className="fas fa-list"></i>
        </button>
        <button 
          className={viewMode === 'grid' ? 'active' : ''}
          onClick={() => setViewMode('grid')}
          title="Grid View"
        >
          <i className="fas fa-th"></i>
        </button>
        <button 
          className={viewMode === 'details' ? 'active' : ''}
          onClick={() => setViewMode('details')}
          title="Details View"
        >
          <i className="fas fa-th-list"></i>
        </button>
      </div>

      {/* New Folder Dialog */}
      {showNewFolderDialog && (
        <div className="dialog-overlay">
          <div className="dialog">
            <h3>Create New Folder</h3>
            <input
              type="text"
              value={newFolderName}
              onChange={(e) => setNewFolderName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleCreateFolder();
                if (e.key === 'Escape') handleCancelFolder();
              }}
              autoFocus
            />
            <div className="dialog-buttons">
              <button onClick={handleCancelFolder}>Cancel</button>
              <button onClick={handleCreateFolder} className="primary">Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Toolbar;
