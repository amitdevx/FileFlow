import React, { useState } from 'react';
import './SearchPanel.css';

function SearchPanel() {
  const [query, setQuery] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSearch = () => {
    console.log('Searching for:', query);
  };

  return (
    <div className="search-panel">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search files..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch}>
          <i className="fas fa-search"></i>
        </button>
        <button onClick={() => setShowAdvanced(!showAdvanced)}>
          <i className="fas fa-filter"></i> Advanced
        </button>
      </div>
      
      {showAdvanced && (
        <div className="advanced-search">
          <p>Advanced search options will appear here</p>
        </div>
      )}
    </div>
  );
}

export default SearchPanel;
