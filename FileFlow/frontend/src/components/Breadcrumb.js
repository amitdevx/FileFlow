import React from 'react';
import './Breadcrumb.css';

function Breadcrumb({ currentPath }) {
  const pathParts = currentPath ? currentPath.split('/').filter(p => p) : [];
  
  return (
    <div className="breadcrumb">
      <a href="/">Home</a>
      {pathParts.map((part, index) => (
        <span key={index}>
          {' / '}
          <a href={`/${pathParts.slice(0, index + 1).join('/')}`}>{part}</a>
        </span>
      ))}
    </div>
  );
}

export default Breadcrumb;
