import React from 'react';
import './StatusBar.css';

function StatusBar({ selectedCount, totalFiles }) {
  return (
    <div className="status-bar">
      <div className="status-left">
        <span>{totalFiles || 0} items</span>
        {selectedCount > 0 && (
          <span className="selected-info"> | {selectedCount} selected</span>
        )}
      </div>
      <div className="status-right">
        <span>Ctrl+A (Select All) | Ctrl+C (Copy) | Ctrl+X (Cut) | Ctrl+V (Paste) | Del (Delete) | F2 (Rename)</span>
      </div>
    </div>
  );
}

export default StatusBar;
