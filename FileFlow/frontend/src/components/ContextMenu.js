import React from 'react';
import './ContextMenu.css';

function ContextMenu({ x, y, selectedFiles, onClose }) {
  if (!selectedFiles || selectedFiles.length === 0) {
    return null;
  }

  return (
    <div className="context-menu" style={{ top: y, left: x }}>
      <ul>
        <li>Open</li>
        <li>Download</li>
        <li>Delete</li>
        <li>Rename</li>
      </ul>
    </div>
  );
}

export default ContextMenu;