import React from 'react';
import './PreviewPanel.css';

function PreviewPanel({ selectedFile, onClose }) {
  if (!selectedFile) {
    return null;
  }

  return (
    <div className="preview-panel">
      <button onClick={onClose}>Close</button>
      <h3>{selectedFile.name}</h3>
      <p>Size: {selectedFile.size}</p>
      <p>Date: {selectedFile.date}</p>
    </div>
  );
}

export default PreviewPanel;