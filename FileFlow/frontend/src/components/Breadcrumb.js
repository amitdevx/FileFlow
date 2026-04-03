import React from 'react';
import { useFiles } from '../context/FileContext';
import './Breadcrumb.css';

function Breadcrumb() {
  const { breadcrumbs, fetchFiles } = useFiles();
  
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
      <button type="button" className="breadcrumb-link" onClick={handleHomeClick}>
        <i className="fas fa-home"></i> Home
      </button>
      {breadcrumbs && breadcrumbs.map((crumb) => (
        <span key={crumb.id}>
          {' / '}
          <button type="button" className="breadcrumb-link" onClick={(e) => handleBreadcrumbClick(e, crumb.id)}>
            {crumb.name}
          </button>
        </span>
      ))}
    </div>
  );
}

export default Breadcrumb;
