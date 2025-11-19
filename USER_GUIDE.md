# FileFlow - User Guide

## 🎯 Quick Start

### Installation & Running

1. **Quick Start (Recommended)**
   ```bash
   ./start.sh
   ```
   This script will:
   - Install all dependencies
   - Initialize the database
   - Start both backend and frontend servers

2. **Manual Start**
   
   Backend:
   ```bash
   cd FileFlow/backend
   pip install -r ../requirements.txt
   flask init-db
   flask run
   ```
   
   Frontend:
   ```bash
   cd FileFlow/frontend
   npm install
   npm start
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📚 Feature Guide

### 1. File Management

#### Uploading Files
- Click the **Upload** button in the toolbar
- Or drag and drop files directly into the file browser
- Multiple file upload supported

#### Creating Folders
- Click **New Folder** button
- Enter folder name
- Folder appears in current directory

#### Viewing Files
- **List View**: Detailed information with file names, sizes, and dates
- **Grid View**: Thumbnail/icon-based view for quick browsing
- **Details View**: Comprehensive file information
- Toggle views using the view buttons in the toolbar

#### File Operations
- **Rename**: Select file → Press `F2` or right-click → Rename
- **Delete**: Select file(s) → Press `Delete` or right-click → Delete
- **Copy**: Select file(s) → `Ctrl+C`
- **Cut**: Select file(s) → `Ctrl+X`
- **Paste**: Navigate to destination → `Ctrl+V`

### 2. Navigation

#### Breadcrumb Navigation
- Click any folder in the breadcrumb path to jump to that location
- Breadcrumbs show your current path from root

#### Back/Forward Navigation
- Use **Back** (Alt+Left) and **Forward** (Alt+Right) buttons
- Browser-style history navigation
- Navigate through previously visited folders

#### Folder Navigation
- Double-click folders to open them
- Click folder names in breadcrumb to jump directly

### 3. Selection

#### Selecting Files
- **Single**: Click on a file
- **Multiple**: Hold `Ctrl` (Windows/Linux) or `Cmd` (Mac) while clicking
- **Range**: Click first file, hold `Shift`, click last file
- **All**: Press `Ctrl+A` or right-click → Select All

#### Deselecting
- Press `Escape` to clear selection
- Click in empty area to deselect all

### 4. Search & Filtering

#### Basic Search
1. Click the search bar at the top
2. Type your search query
3. Press `Enter` or click the search button

#### Advanced Search
1. Click the **Advanced** button next to search
2. Set filters:
   - **File Types**: Select image, video, audio, PDF, or text
   - **Size Range**: Set minimum and maximum file size
   - **Date Range**: Filter by creation/modification date
3. Click **Search**

#### Saved Search Profiles
1. Create an advanced search
2. Click **Save Profile**
3. Name your search profile
4. Access saved searches from the dropdown menu

### 5. File Preview

The preview panel on the right shows:
- **Images**: Full preview with zoom
- **Videos**: Built-in video player
- **Audio**: Audio player with controls
- **PDFs**: Embedded PDF viewer
- **Text Files**: Syntax highlighting for code

#### Preview Controls
- Toggle preview panel with the preview button
- Close preview by clicking the X button
- Resize preview panel by dragging the divider

### 6. Compression & Archives

#### Creating Archives
1. Select files/folders to compress
2. Right-click → **Create Archive**
3. Choose format:
   - ZIP (with optional password)
   - TAR (with gz, bz2, or xz compression)
   - 7Z (with optional password)
4. Enter archive name
5. Click **Create**

#### Extracting Archives
1. Select an archive file
2. Right-click → **Extract**
3. Enter password if required
4. Files extract to a new folder

#### Browsing Archives
1. Select an archive file
2. Right-click → **View Contents**
3. See list of files without extracting

### 7. Context Menu (Right-Click)

Right-click on any file or folder to access:
- **Open**: Open file or navigate into folder
- **Rename**: Change file/folder name
- **Copy**: Copy to clipboard
- **Cut**: Cut to clipboard
- **Download**: Download file to your computer
- **Delete**: Remove file/folder
- **Properties**: View detailed information

### 8. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all files |
| `Ctrl+C` | Copy selected files |
| `Ctrl+X` | Cut selected files |
| `Ctrl+V` | Paste files |
| `Ctrl+Z` | Undo last operation |
| `Delete` | Delete selected files |
| `F2` | Rename selected file |
| `F5` | Refresh file list |
| `Escape` | Clear selection / Close dialogs |
| `Alt+Left` | Navigate back |
| `Alt+Right` | Navigate forward |
| `Alt+Up` | Go to parent folder |
| `Ctrl+F` | Focus search bar |

### 9. Theme Customization

#### Switching Themes
- Click the **Theme** button (Sun/Moon icon) in the toolbar
- Choose between Light and Dark themes
- Theme preference is automatically saved

#### Theme Features
- **Light Theme**: Bright, clean interface for daytime use
- **Dark Theme**: Reduced eye strain for nighttime use
- **Smooth Transitions**: Animated theme switching
- **Persistent**: Your choice is remembered across sessions

### 10. Status Bar

The status bar at the bottom shows:
- **Total Files**: Number of items in current folder
- **Selected**: Number of selected items
- **Total Size**: Combined size of all files
- **Keyboard Hints**: Quick reference for shortcuts

### 11. Drag & Drop

#### Moving Files
1. Click and hold on a file/folder
2. Drag to destination folder
3. Release to drop
4. File moves to new location

#### Uploading Files
1. Drag files from your computer
2. Drop them into the file browser
3. Files upload automatically

### 12. Bulk Operations

#### Bulk Rename
1. Select multiple files
2. Right-click → **Bulk Rename**
3. Enter pattern with wildcards:
   - `{name}`: Original filename
   - `{num}`: Sequential number
   - `{date}`: Current date
4. Preview changes
5. Click **Apply**

#### Bulk Move
1. Select multiple files
2. Cut or Copy (`Ctrl+X` or `Ctrl+C`)
3. Navigate to destination
4. Paste (`Ctrl+V`)
5. Confirm operation

#### Bulk Delete
1. Select multiple files
2. Press `Delete` key
3. Confirm deletion dialog
4. All selected files removed

### 13. Favorites & Bookmarks

#### Adding Favorites
1. Navigate to a folder
2. Click the **Star** icon
3. Folder added to favorites sidebar

#### Accessing Favorites
- Click on favorite in the sidebar
- Instantly navigate to bookmarked location
- Organize your most-used folders

### 14. File Organization

#### Auto-Organize
- Right-click in empty space → **Auto-Organize**
- Choose organization method:
  - By Type (Images, Documents, Videos, etc.)
  - By Date (Year/Month folders)
  - By Size (Small, Medium, Large)

#### Duplicate Finder
1. Right-click → **Find Duplicates**
2. System scans for duplicate files
3. Review list of duplicates
4. Choose which copies to keep/delete

## 🎨 Tips & Tricks

### Power User Tips
1. **Quick Navigation**: Use `Alt+Left/Right` to jump through folder history
2. **Fast Selection**: Hold `Shift` and click to select ranges
3. **Multi-Select**: Hold `Ctrl` to select non-consecutive files
4. **Quick Preview**: Select a file and press `Space` for quick look
5. **Batch Operations**: Select multiple files for bulk actions

### Performance Tips
1. Use **Grid View** for folders with many files (faster rendering)
2. Enable **Virtual Scrolling** for large file lists
3. **Search Profiles** save time on repeated searches
4. **Favorites** provide instant access to frequently used folders

### Organization Tips
1. Create a consistent folder structure
2. Use descriptive folder names
3. Tag files for easier searching
4. Regular cleanup with duplicate finder
5. Archive old files to save space

## 🔧 Troubleshooting

### Files Not Showing
- Press `F5` to refresh the file list
- Check if you're in the correct folder
- Verify file permissions

### Upload Fails
- Check file size (max 100MB by default)
- Verify file type is allowed
- Ensure sufficient disk space

### Preview Not Working
- Check if file type is supported
- Try downloading and opening locally
- Clear browser cache

### Search Not Finding Files
- Verify search terms
- Check filters (type, size, date)
- Ensure files exist in current location

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review error messages in the status bar
3. Check console logs (F12 in browser)
4. File an issue on GitHub

## 🎓 Advanced Usage

### API Integration
Use the REST API for programmatic access:
```javascript
// Upload file
const formData = new FormData();
formData.append('file', file);
await axios.post('/api/upload', formData);

// Search files
const results = await axios.post('/api/search', {
  query: 'document',
  file_types: ['application/pdf']
});

// Create archive
await axios.post('/api/compress/create', {
  file_ids: [1, 2, 3],
  archive_name: 'backup',
  format: 'zip'
});
```

### Custom Themes
Edit CSS variables in `App.css`:
```css
:root[data-theme="custom"] {
  --bg-primary: #your-color;
  --text-primary: #your-color;
  --accent-color: #your-color;
}
```

## 📝 Best Practices

1. **Regular Backups**: Download important files regularly
2. **Organize Frequently**: Keep folders tidy
3. **Use Search Profiles**: Save common searches
4. **Tag Files**: Add tags for better organization
5. **Archive Old Files**: Compress infrequently used files
6. **Check Duplicates**: Run duplicate finder monthly
7. **Update Regularly**: Keep FileFlow up to date

---

**Enjoy using FileFlow! 🚀**
