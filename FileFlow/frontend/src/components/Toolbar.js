import React from 'react';
import './Toolbar.css';

function Toolbar({ viewMode, setViewMode, selectedFiles }) {
  return (
    <div className="toolbar">
      <div className="toolbar-group">
        <button title="Back"><i className="fas fa-arrow-left"></i></button>
        <button title="Forward"><i className="fas fa-arrow-right"></i></button>
      </div>
      
      <div className="toolbar-group">
        <button title="Upload"><i className="fas fa-upload"></i> Upload</button>
        <button title="New Folder"><i className="fas fa-folder-plus"></i> New Folder</button>
      </div>
      
      <div className="toolbar-group">
        <button disabled={!selectedFiles || selectedFiles.length !== 1} title="Rename">
          <i className="fas fa-pen"></i> Rename
        </button>
        <button disabled={!selectedFiles || selectedFiles.length === 0} title="Delete">
          <i className="fas fa-trash"></i> Delete
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
    </div>
  );
}

export default Toolbar;
