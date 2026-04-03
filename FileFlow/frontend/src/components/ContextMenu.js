import React from 'react';
import { useFiles } from '../context/FileContext';
import './ContextMenu.css';

function ContextMenu({ x, y, selectedFiles, onClose }) {
  const { deleteFiles, renameFile, fetchFiles } = useFiles();

  if (!selectedFiles || selectedFiles.length === 0) {
    return null;
  }

  const handleOpen = () => {
    const file = selectedFiles[0];
    if (file.is_folder) {
      fetchFiles(file.id);
    } else {
      window.open(`/view_file/${file.id}`, '_blank');
    }
    onClose();
  };

  const handleDownload = () => {
    selectedFiles.forEach(file => {
      if (!file.is_folder) {
        window.open(`/download_file/${file.id}`, '_blank');
      }
    });
    onClose();
  };

  const handleDelete = async () => {
    if (window.confirm(`Delete ${selectedFiles.length} item(s)?`)) {
      await deleteFiles(selectedFiles.map(f => f.id));
    }
    onClose();
  };

  const handleRename = () => {
    const file = selectedFiles[0];
    const newName = prompt('Enter new name:', file.filename);
    if (newName && newName !== file.filename) {
      renameFile(file.id, newName);
    }
    onClose();
  };

  const handleCopy = () => {
    // Copy functionality - store file IDs for paste
    localStorage.setItem('clipboard', JSON.stringify({
      files: selectedFiles.map(f => f.id),
      operation: 'copy'
    }));
    onClose();
  };

  const handleCut = () => {
    // Cut functionality - store file IDs for paste
    localStorage.setItem('clipboard', JSON.stringify({
      files: selectedFiles.map(f => f.id),
      operation: 'cut'
    }));
    onClose();
  };

  // Close menu when clicking outside
  const handleOverlayClick = (e) => {
    if (e.target.className === 'context-menu-overlay') {
      onClose();
    }
  };

  return (
    <div className="context-menu-overlay" onClick={handleOverlayClick}>
      <div className="context-menu" style={{ top: y, left: x }}>
        <ul>
          <li onClick={handleOpen}>
            <i className="fas fa-folder-open"></i> Open
          </li>
          {selectedFiles.length === 1 && !selectedFiles[0].is_folder && (
            <li onClick={handleDownload}>
              <i className="fas fa-download"></i> Download
            </li>
          )}
          <li className="separator"></li>
          <li onClick={handleCopy}>
            <i className="fas fa-copy"></i> Copy
          </li>
          <li onClick={handleCut}>
            <i className="fas fa-cut"></i> Cut
          </li>
          <li className="separator"></li>
          {selectedFiles.length === 1 && (
            <li onClick={handleRename}>
              <i className="fas fa-pen"></i> Rename
            </li>
          )}
          <li onClick={handleDelete} className="danger">
            <i className="fas fa-trash"></i> Delete
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ContextMenu;