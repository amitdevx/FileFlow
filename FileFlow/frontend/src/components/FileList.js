import React from 'react';
import { useFiles } from '../context/FileContext';
import './FileList.css';

function FileList({ viewMode, selectedFiles, setSelectedFiles, onContextMenu }) {
  const { files, loading, fetchFiles } = useFiles();

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

  const handleDoubleClick = (file) => {
    if (file.is_folder) {
      fetchFiles(file.id);
      setSelectedFiles([]);
    } else {
      // Open file for viewing
      window.open(`/view_file/${file.id}`, '_blank');
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

  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return '-';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0;
    while (bytes >= 1024 && i < units.length - 1) {
      bytes /= 1024;
      i++;
    }
    return `${bytes.toFixed(1)} ${units[i]}`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  const getFileIcon = (file) => {
    if (file.is_folder) return 'fa-folder';
    const ext = file.filename?.split('.').pop()?.toLowerCase();
    const iconMap = {
      pdf: 'fa-file-pdf',
      doc: 'fa-file-word', docx: 'fa-file-word',
      xls: 'fa-file-excel', xlsx: 'fa-file-excel',
      ppt: 'fa-file-powerpoint', pptx: 'fa-file-powerpoint',
      jpg: 'fa-file-image', jpeg: 'fa-file-image', png: 'fa-file-image', gif: 'fa-file-image',
      mp4: 'fa-file-video', mov: 'fa-file-video', avi: 'fa-file-video',
      mp3: 'fa-file-audio', wav: 'fa-file-audio',
      zip: 'fa-file-archive', tar: 'fa-file-archive', '7z': 'fa-file-archive',
      txt: 'fa-file-alt',
      js: 'fa-file-code', py: 'fa-file-code', html: 'fa-file-code', css: 'fa-file-code',
    };
    return iconMap[ext] || 'fa-file';
  };

  if (loading) {
    return <div className="file-list-loading">Loading...</div>;
  }

  if (!files || !Array.isArray(files) || files.length === 0) {
    return (
      <div className="file-list-empty">
        <i className="fas fa-folder-open"></i>
        <p>This folder is empty</p>
        <p className="hint">Upload files or create a new folder to get started</p>
      </div>
    );
  }

  if (viewMode === 'grid') {
    return (
      <div className="file-list file-list-grid">
        {files.map(file => (
          <div
            key={file.id}
            className={`file-item ${isSelected(file) ? 'selected' : ''}`}
            onClick={(e) => handleClick(file, e)}
            onDoubleClick={() => handleDoubleClick(file)}
            onContextMenu={(e) => handleContextMenu(e, file)}
          >
            <i className={`fas ${getFileIcon(file)}`}></i>
            <span className="file-name">{file.filename}</span>
            {file.is_favorite && <i className="fas fa-star favorite-icon"></i>}
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
            <th>Modified</th>
          </tr>
        </thead>
        <tbody>
          {files.map(file => (
            <tr
              key={file.id}
              className={isSelected(file) ? 'selected' : ''}
              onClick={(e) => handleClick(file, e)}
              onDoubleClick={() => handleDoubleClick(file)}
              onContextMenu={(e) => handleContextMenu(e, file)}
            >
              <td className="file-name-cell">
                <i className={`fas ${getFileIcon(file)}`}></i>
                {' '}{file.filename}
                {file.is_favorite && <i className="fas fa-star favorite-icon"></i>}
              </td>
              <td>{file.is_folder ? '-' : formatFileSize(file.filesize)}</td>
              <td>{formatDate(file.modified_at || file.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FileList;
