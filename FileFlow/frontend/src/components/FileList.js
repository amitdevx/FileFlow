import React from 'react';
import './FileList.css';

function FileList({ viewMode, selectedFiles, setSelectedFiles, onContextMenu }) {
  const files = [
    { id: 1, name: 'File 1.txt', size: '1 KB', date: '2025-11-19', type: 'file' },
    { id: 2, name: 'File 2.jpg', size: '10 KB', date: '2025-11-18', type: 'file' },
    { id: 3, name: 'Folder 1', size: '', date: '2025-11-17', type: 'folder' },
  ];

  const handleClick = (file, e) => {
    if (e.ctrlKey || e.metaKey) {
      const isSelected = selectedFiles.some(f => f.id === file.id);
      if (isSelected) {
        setSelectedFiles(selectedFiles.filter(f => f.id !== file.id));
      } else {
        setSelectedFiles([...selectedFiles, file]);
      }
    } else {
      setSelectedFiles([file]);
    }
  };

  const handleContextMenu = (e, file) => {
    e.preventDefault();
    if (!selectedFiles.some(f => f.id === file.id)) {
      setSelectedFiles([file]);
    }
    onContextMenu({ x: e.clientX, y: e.clientY });
  };

  const isSelected = (file) => selectedFiles.some(f => f.id === file.id);

  if (viewMode === 'grid') {
    return (
      <div className="file-list file-list-grid">
        {files.map(file => (
          <div
            key={file.id}
            className={`file-item ${isSelected(file) ? 'selected' : ''}`}
            onClick={(e) => handleClick(file, e)}
            onContextMenu={(e) => handleContextMenu(e, file)}
          >
            <i className={`fas ${file.type === 'folder' ? 'fa-folder' : 'fa-file'}`}></i>
            <span>{file.name}</span>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="file-list file-list-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {files.map(file => (
            <tr
              key={file.id}
              className={isSelected(file) ? 'selected' : ''}
              onClick={(e) => handleClick(file, e)}
              onContextMenu={(e) => handleContextMenu(e, file)}
            >
              <td>
                <i className={`fas ${file.type === 'folder' ? 'fa-folder' : 'fa-file'}`}></i>
                {' '}{file.name}
              </td>
              <td>{file.size}</td>
              <td>{file.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FileList;
