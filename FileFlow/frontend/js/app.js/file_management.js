document.addEventListener('DOMContentLoaded', () => {
    const fileBrowser = document.getElementById('file-browser');
    const listViewBtn = document.getElementById('list-view-btn');
    const gridViewBtn = document.getElementById('grid-view-btn');
    const searchInput = document.getElementById('search-input');
    const itemCount = document.getElementById('item-count');
    const selectionInfo = document.getElementById('selection-info');
    const renameBtn = document.getElementById('rename-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const createFolderBtn = document.getElementById('create-folder-btn');
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const createFolderForm = document.getElementById('create-folder-form');
    const folderNameInput = document.getElementById('folder-name-input');

    // View switcher
    listViewBtn.addEventListener('click', () => {
        fileBrowser.classList.remove('file-browser-grid-view');
        fileBrowser.classList.add('file-browser-list-view');
        listViewBtn.classList.add('active');
        gridViewBtn.classList.remove('active');
    });

    gridViewBtn.addEventListener('click', () => {
        fileBrowser.classList.remove('file-browser-list-view');
        fileBrowser.classList.add('file-browser-grid-view');
        gridViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
    });

    // File selection
    let selectedItems = [];

    fileBrowser.addEventListener('click', (e) => {
        const item = e.target.closest('.file-item');
        if (!item) return;

        if (e.ctrlKey || e.metaKey) {
            item.classList.toggle('selected');
        } else {
            document.querySelectorAll('.file-item.selected').forEach(el => el.classList.remove('selected'));
            item.classList.add('selected');
        }
        updateSelection();
    });

    function updateSelection() {
        selectedItems = Array.from(document.querySelectorAll('.file-item.selected'));
        selectionInfo.textContent = `${selectedItems.length} items selected`;
        renameBtn.disabled = selectedItems.length !== 1;
        deleteBtn.disabled = selectedItems.length === 0;
    }

    // Search
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        document.querySelectorAll('.file-item').forEach(item => {
            const fileName = item.dataset.name.toLowerCase();
            if (fileName.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });

    // Toolbar actions
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => uploadForm.submit());

    createFolderBtn.addEventListener('click', () => {
        const folderName = prompt('Enter folder name:');
        if (folderName) {
            folderNameInput.value = folderName;
            createFolderForm.submit();
        }
    });

    renameBtn.addEventListener('click', () => {
        if (selectedItems.length !== 1) return;
        const item = selectedItems[0];
        const oldName = item.dataset.name;
        const newName = prompt('Enter new name:', oldName);
        if (newName && newName !== oldName) {
            fetch(`/rename_file/${item.dataset.id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ new_name: newName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    item.dataset.name = newName;
                    item.querySelector('.file-name').textContent = newName;
                } else {
                    alert('Error renaming file.');
                }
            });
        }
    });

    deleteBtn.addEventListener('click', () => {
        if (selectedItems.length === 0) return;
        if (confirm('Are you sure you want to delete the selected items?')) {
            const ids = selectedItems.map(item => item.dataset.id);
            Promise.all(ids.map(id =>
                fetch(`/delete_file/${id}`, { method: 'DELETE' })
            )).then(() => {
                selectedItems.forEach(item => item.remove());
                updateSelection();
            });
        }
    });

    // Drag and drop for moving files
    let draggedItem = null;

    fileBrowser.addEventListener('dragstart', (e) => {
        const item = e.target.closest('.file-item');
        if (item) {
            draggedItem = item;
            e.dataTransfer.setData('text/plain', item.dataset.id);
            e.dataTransfer.effectAllowed = 'move';
        }
    });

    fileBrowser.addEventListener('dragover', (e) => {
        e.preventDefault();
        const targetItem = e.target.closest('.file-item');
        if (targetItem && targetItem.dataset.type === 'folder') {
            targetItem.classList.add('drag-over-folder');
        }
    });

    fileBrowser.addEventListener('dragleave', (e) => {
        const targetItem = e.target.closest('.file-item');
        if (targetItem) {
            targetItem.classList.remove('drag-over-folder');
        }
    });

    fileBrowser.addEventListener('drop', (e) => {
        e.preventDefault();
        const destinationItem = e.target.closest('.file-item');
        if (!draggedItem || !destinationItem || destinationItem.dataset.type !== 'folder') {
            if(destinationItem) destinationItem.classList.remove('drag-over-folder');
            return;
        }
        destinationItem.classList.remove('drag-over-folder');

        const fileId = draggedItem.dataset.id;
        const destinationFolderId = destinationItem.dataset.id;

        if (fileId === destinationFolderId) return;

        fetch(`/move_file/${fileId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination_folder_id: destinationFolderId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                draggedItem.remove();
                updateSelection();
            } else {
                alert('Error moving file.');
            }
        });
    });
});

function deleteFile(fileId) {
    if (confirm('Are you sure you want to delete this file?')) {
        fetch(`/delete_file/${fileId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Error deleting file.');
            }
        });
    }
}
