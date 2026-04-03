import asyncio
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable

logger = logging.getLogger(__name__)


class FileEventHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self, callback: Callable | None = None):
        self.callback = callback
        super().__init__()
    
    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"File created: {event.src_path}")
            if self.callback:
                self.callback("created", event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"File deleted: {event.src_path}")
            if self.callback:
                self.callback("deleted", event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"File modified: {event.src_path}")
            if self.callback:
                self.callback("modified", event.src_path)
    
    def on_moved(self, event):
        logger.info(f"File moved: {event.src_path} -> {event.dest_path}")
        if self.callback:
            self.callback("moved", event.src_path, event.dest_path)


class WatcherService:
    """Service for watching file system changes"""
    
    def __init__(self):
        self.observer: Observer | None = None
        self.watched_paths: set[str] = set()
    
    def start_watching(self, path: str, callback: Callable | None = None) -> bool:
        """Start watching a directory for changes"""
        watch_path = Path(path)
        if not watch_path.exists():
            watch_path.mkdir(parents=True, exist_ok=True)
        
        if str(watch_path) in self.watched_paths:
            return False
        
        if self.observer is None:
            self.observer = Observer()
            self.observer.start()
        
        event_handler = FileEventHandler(callback)
        self.observer.schedule(event_handler, str(watch_path), recursive=True)
        self.watched_paths.add(str(watch_path))
        
        logger.info(f"Started watching: {watch_path}")
        return True
    
    def stop_watching(self, path: str | None = None) -> bool:
        """Stop watching a directory or all directories"""
        if self.observer is None:
            return False
        
        if path is None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watched_paths.clear()
        else:
            self.watched_paths.discard(str(path))
        
        return True
    
    def is_watching(self, path: str) -> bool:
        """Check if a path is being watched"""
        return str(path) in self.watched_paths


# Singleton instance
watcher_service = WatcherService()
