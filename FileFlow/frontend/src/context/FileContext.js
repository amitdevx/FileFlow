import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import axios from 'axios';

// Add axios response interceptor to handle authentication
axios.interceptors.response.use(
  response => response,
  error => {
    // If we get a 401 or if the response contains HTML redirect
    if (error.response && error.response.status === 401) {
      console.warn('Authentication required');
      window.location.href = '/login';
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);

const FileContext = createContext();

export const useFiles = () => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useFiles must be used within FileProvider');
  }
  return context;
};

export const FileProvider = ({ children }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentFolderId, setCurrentFolderId] = useState(null);
  const [breadcrumbs, setBreadcrumbs] = useState([]);
  const [clipboard, setClipboard] = useState({ files: [], operation: null });
  const [history, setHistory] = useState([null]);
  const [historyIndex, setHistoryIndex] = useState(0);
  
  const fetchFiles = useCallback(async (folderId = null, addToHistory = true) => {
    setLoading(true);
    try {
      // Use the JSON API endpoint
      const url = folderId 
        ? `/api/files?folder_id=${folderId}` 
        : '/api/files';
      
      const response = await axios.get(url, {
        headers: { 'Accept': 'application/json' }
      });
      
      // Check if we got redirected to login (HTML response instead of JSON)
      if (typeof response.data === 'string' && response.data.includes('Redirecting')) {
        console.warn('Not authenticated, redirecting to login');
        window.location.href = '/login';
        return;
      }
      
      // Ensure we always set an array
      const filesData = response.data;
      if (Array.isArray(filesData)) {
        setFiles(filesData);
      } else {
        console.warn('API returned non-array data:', filesData);
        setFiles([]);
      }
      
      setCurrentFolderId(folderId);
      
      // Update history only if this is a new navigation
      if (addToHistory && history[historyIndex] !== folderId) {
        setHistory(prev => {
          const newHistory = prev.slice(0, historyIndex + 1);
          newHistory.push(folderId);
          return newHistory;
        });
        setHistoryIndex(prev => prev + 1);
      }
      
      // Fetch breadcrumbs if in a folder
      if (folderId) {
        try {
          const breadcrumbResponse = await axios.get(`/api/breadcrumbs/${folderId}`);
          setBreadcrumbs(breadcrumbResponse.data || []);
        } catch {
          setBreadcrumbs([]);
        }
      } else {
        setBreadcrumbs([]);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
      
      // Check if error is due to authentication
      if (error.response && (error.response.status === 401 || error.response.status === 302)) {
        console.warn('Authentication required, redirecting to login');
        window.location.href = '/login';
        return;
      }
      
      setFiles([]);
    } finally {
      setLoading(false);
    }
  }, [historyIndex, history]);
  
  const goBack = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      fetchFiles(history[newIndex], false);
    }
  }, [historyIndex, history, fetchFiles]);
  
  const goForward = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      fetchFiles(history[newIndex], false);
    }
  }, [historyIndex, history, fetchFiles]);
  
  const uploadFile = async (file, folderId = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (folderId || currentFolderId) {
      formData.append('folder_id', folderId || currentFolderId);
    }
    
    try {
      await axios.post('/upload', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      fetchFiles(currentFolderId, false);
      return { success: true };
    } catch (error) {
      console.error('Error uploading file:', error);
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };
  
  const createFolder = async (name) => {
    try {
      await axios.post('/create_folder', {
        folder_name: name,
        parent_folder_id: currentFolderId
      }, {
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      fetchFiles(currentFolderId, false);
      return { success: true };
    } catch (error) {
      console.error('Error creating folder:', error);
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };
  
  const deleteFiles = async (fileIds) => {
    try {
      await Promise.all(fileIds.map(id => 
        axios.delete(`/delete_file/${id}`, {
          headers: { 'Accept': 'application/json' }
        })
      ));
      fetchFiles(currentFolderId, false);
      return { success: true };
    } catch (error) {
      console.error('Error deleting files:', error);
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };
  
  const renameFile = async (fileId, newName) => {
    try {
      await axios.post(`/rename_file/${fileId}`, { new_name: newName }, {
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      fetchFiles(currentFolderId, false);
      return { success: true };
    } catch (error) {
      console.error('Error renaming file:', error);
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };
  
  const moveFiles = async (fileIds, destinationFolderId) => {
    try {
      await Promise.all(fileIds.map(id => 
        axios.post(`/move_file/${id}`, { destination_folder_id: destinationFolderId }, {
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        })
      ));
      fetchFiles(currentFolderId, false);
      return { success: true };
    } catch (error) {
      console.error('Error moving files:', error);
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };
  
  const copyToClipboard = (fileIds) => {
    setClipboard({ files: fileIds, operation: 'copy' });
  };
  
  const cutToClipboard = (fileIds) => {
    setClipboard({ files: fileIds, operation: 'cut' });
  };
  
  const pasteFromClipboard = async () => {
    if (clipboard.operation === 'move' || clipboard.operation === 'cut') {
      await moveFiles(clipboard.files, currentFolderId);
    }
    setClipboard({ files: [], operation: null });
  };
  
  useEffect(() => {
    fetchFiles(null, false);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  
  return (
    <FileContext.Provider value={{
      files,
      loading,
      currentFolderId,
      breadcrumbs,
      clipboard,
      history,
      historyIndex,
      fetchFiles,
      goBack,
      goForward,
      uploadFile,
      createFolder,
      deleteFiles,
      renameFile,
      moveFiles,
      copyToClipboard,
      cutToClipboard,
      pasteFromClipboard
    }}>
      {children}
    </FileContext.Provider>
  );
};
