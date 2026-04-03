import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import axios from 'axios';

const FileContext = createContext();

// API base URL - change this when switching backends
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with interceptors for JWT
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken
          });
          
          const { access_token, refresh_token } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed - clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export const useFiles = () => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useFiles must be used within FileProvider');
  }
  return context;
};

export const useAuth = () => {
  const context = useContext(FileContext);
  if (!context) {
    throw new Error('useAuth must be used within FileProvider');
  }
  return {
    user: context.user,
    isAuthenticated: context.isAuthenticated,
    login: context.login,
    signup: context.signup,
    logout: context.logout,
  };
};

export const FileProvider = ({ children }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentFolderId, setCurrentFolderId] = useState(null);
  const [breadcrumbs, setBreadcrumbs] = useState([]);
  const [clipboard, setClipboard] = useState({ files: [], operation: null });
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchCurrentUser();
    }
  }, []);
  
  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/api/auth/me');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error fetching user:', error);
      setIsAuthenticated(false);
      setUser(null);
    }
  };
  
  const login = async (username, password) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData);
      const { access_token, refresh_token } = response.data;
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      await fetchCurrentUser();
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };
  
  const signup = async (username, email, password) => {
    try {
      await axios.post(`${API_BASE_URL}/api/auth/signup`, {
        username,
        email,
        password
      });
      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: error.response?.data?.detail || 'Signup failed' };
    }
  };
  
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setIsAuthenticated(false);
    setFiles([]);
  };
  
  const fetchFiles = useCallback(async (folderId = null) => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    try {
      const url = folderId 
        ? `/api/folders/${folderId}` 
        : '/api/folders';
      const response = await api.get(url);
      
      setFiles(response.data.files || response.data);
      setBreadcrumbs(response.data.breadcrumbs || []);
      setCurrentFolderId(folderId);
      
      // Update history
      setHistory(prev => {
        const newHistory = prev.slice(0, historyIndex + 1);
        newHistory.push(folderId);
        return newHistory;
      });
      setHistoryIndex(prev => prev + 1);
    } catch (error) {
      console.error('Error fetching files:', error);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, historyIndex]);
  
  const goBack = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      fetchFiles(history[newIndex]);
    }
  }, [historyIndex, history, fetchFiles]);
  
  const goForward = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      fetchFiles(history[newIndex]);
    }
  }, [historyIndex, history, fetchFiles]);
  
  const uploadFile = async (file, folderId = null) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const url = folderId 
        ? `/api/files/upload?folder_id=${folderId}`
        : '/api/files/upload';
      await api.post(url, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error uploading file:', error);
      return { success: false, error: error.response?.data?.detail || 'Upload failed' };
    }
  };
  
  const createFolder = async (name) => {
    try {
      await api.post('/api/folders', {
        folder_name: name,
        parent_folder_id: currentFolderId
      });
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error creating folder:', error);
      return { success: false, error: error.response?.data?.detail || 'Failed to create folder' };
    }
  };
  
  const deleteFiles = async (fileIds) => {
    try {
      await Promise.all(fileIds.map(id => api.delete(`/api/files/${id}`)));
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error deleting files:', error);
      return { success: false, error: 'Failed to delete files' };
    }
  };
  
  const renameFile = async (fileId, newName) => {
    try {
      await api.post(`/api/files/${fileId}/rename`, { new_name: newName });
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error renaming file:', error);
      return { success: false, error: error.response?.data?.detail || 'Failed to rename' };
    }
  };
  
  const moveFiles = async (fileIds, destinationFolderId) => {
    try {
      await Promise.all(fileIds.map(id => 
        api.post(`/api/files/${id}/move`, { destination_folder_id: destinationFolderId })
      ));
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error moving files:', error);
      return { success: false, error: 'Failed to move files' };
    }
  };
  
  const toggleFavorite = async (fileId) => {
    try {
      await api.post(`/api/files/${fileId}/favorite`);
      fetchFiles(currentFolderId);
      return { success: true };
    } catch (error) {
      console.error('Error toggling favorite:', error);
      return { success: false };
    }
  };
  
  const searchFiles = async (searchParams) => {
    try {
      const response = await api.post('/api/search', searchParams);
      return { success: true, files: response.data };
    } catch (error) {
      console.error('Error searching files:', error);
      return { success: false, error: 'Search failed' };
    }
  };
  
  const createArchive = async (fileIds, archiveName, format = 'zip', password = null) => {
    try {
      const response = await api.post('/api/compress/create', {
        file_ids: fileIds,
        archive_name: archiveName,
        format,
        password
      });
      fetchFiles(currentFolderId);
      return { success: true, file: response.data };
    } catch (error) {
      console.error('Error creating archive:', error);
      return { success: false, error: error.response?.data?.detail || 'Failed to create archive' };
    }
  };
  
  const extractArchive = async (fileId, password = null) => {
    try {
      const response = await api.post(`/api/compress/extract/${fileId}`, { password });
      fetchFiles(currentFolderId);
      return { success: true, folder: response.data };
    } catch (error) {
      console.error('Error extracting archive:', error);
      return { success: false, error: error.response?.data?.detail || 'Failed to extract archive' };
    }
  };
  
  const copyToClipboard = (fileIds) => {
    setClipboard({ files: fileIds, operation: 'copy' });
  };
  
  const cutToClipboard = (fileIds) => {
    setClipboard({ files: fileIds, operation: 'cut' });
  };
  
  const pasteFromClipboard = async () => {
    if (clipboard.operation === 'cut') {
      await moveFiles(clipboard.files, currentFolderId);
    }
    // TODO: Implement copy operation on backend
    setClipboard({ files: [], operation: null });
  };
  
  const downloadFile = (fileId) => {
    const token = localStorage.getItem('access_token');
    window.open(`${API_BASE_URL}/api/files/download/${fileId}?token=${token}`, '_blank');
  };
  
  const viewFile = (fileId) => {
    const token = localStorage.getItem('access_token');
    window.open(`${API_BASE_URL}/api/files/view/${fileId}?token=${token}`, '_blank');
  };
  
  // Fetch files when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchFiles();
    }
  }, [isAuthenticated]);
  
  return (
    <FileContext.Provider value={{
      // File state
      files,
      loading,
      currentFolderId,
      breadcrumbs,
      clipboard,
      history,
      historyIndex,
      
      // Auth state
      user,
      isAuthenticated,
      
      // Auth actions
      login,
      signup,
      logout,
      
      // Navigation actions
      fetchFiles,
      goBack,
      goForward,
      
      // File actions
      uploadFile,
      createFolder,
      deleteFiles,
      renameFile,
      moveFiles,
      toggleFavorite,
      downloadFile,
      viewFile,
      
      // Search actions
      searchFiles,
      
      // Archive actions
      createArchive,
      extractArchive,
      
      // Clipboard actions
      copyToClipboard,
      cutToClipboard,
      pasteFromClipboard
    }}>
      {children}
    </FileContext.Provider>
  );
};

export default FileContext;
