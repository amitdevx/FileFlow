import React from 'react';
import { useFiles } from '../context/FileContext';
import './Breadcrumb.css';

function Breadcrumb() {
  const { breadcrumbs, fetchFiles, currentFolderId } = useFiles();
  
  const handleHomeClick = (e) => {
    e.preventDefault();
    fetchFiles(null);
  };

  const handleBreadcrumbClick = (e, folderId) => {
    e.preventDefault();
    fetchFiles(folderId);
  };
  
  return (
    <div className="breadcrumb">
      <a href="#" onClick={handleHomeClick}>
        <i className="fas fa-home"></i> Home
      </a>
      {breadcrumbs && breadcrumbs.map((crumb, index) => (
        <span key={crumb.id}>
          {' / '}
          <a href="#" onClick={(e) => handleBreadcrumbClick(e, crumb.id)}>
            {crumb.name}
          </a>
        </span>
      ))}
    </div>
  );
}

export default Breadcrumb;
