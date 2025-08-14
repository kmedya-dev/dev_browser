import webview
import http.server
import socketserver
import threading
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from urllib.parse import urlparse, quote_plus

# --- Live Reload Server ---
class ReloadHandler(FileSystemEventHandler):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"Detected change in {event.src_path}, reloading...")
        self.window.load_url(self.window.get_current_url())

def start_server(directory, port):
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(directory)
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

def start_file_watcher(directory, window):
    event_handler = ReloadHandler(window)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

# --- Main Application ---
class Api:
    def __init__(self, window):
        self.window = window
        self.bookmarks = []
        self.theme = 'light'
        self.language = 'en'

    def log(self, message):
        print(f"JS console: {message}")

    def load_url(self, url):
        if not urlparse(url).scheme:
            url = f"https://www.google.com/search?q={quote_plus(url)}"
        self.window.load_url(url)

    def toggle_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
            self.window.evaluate_js('document.body.classList.add("dark-mode")')
        else:
            self.theme = 'light'
            self.window.evaluate_js('document.body.classList.remove("dark-mode")')

    def toggle_language(self):
        if self.language == 'en':
            self.language = 'bn'
            self.window.evaluate_js('document.getElementById("lang-btn").textContent = "English"')
            self.window.evaluate_js('document.getElementById("go-btn").textContent = "যান"')
            self.window.evaluate_js('document.getElementById("theme-btn").textContent = "থিম পরিবর্তন"')
            self.window.evaluate_js('document.getElementById("bookmark-btn").textContent = "বুকমার্ক"')
        else:
            self.language = 'en'
            self.window.evaluate_js('document.getElementById("lang-btn").textContent = "বাংলা"')
            self.window.evaluate_js('document.getElementById("go-btn").textContent = "Go"')
            self.window.evaluate_js('document.getElementById("theme-btn").textContent = "Toggle Theme"')
            self.window.evaluate_js('document.getElementById("bookmark-btn").textContent = "Bookmark"')

    def add_bookmark(self, url):
        if url not in self.bookmarks:
            self.bookmarks.append(url)

    def get_bookmarks(self):
        return self.bookmarks

    def get_current_url(self):
        return self.window.get_current_url()

if __name__ == '__main__':
    # --- Server and Watcher Setup ---
    local_web_project_dir = os.path.join(os.path.dirname(__file__), 'local_web_project')
    port = 8000
    server_thread = threading.Thread(target=start_server, args=(local_web_project_dir, port), daemon=True)
    server_thread.start()

    # --- WebView Setup ---
    window = webview.create_window(
        'Dev Browser',
        f'http://localhost:{port}',
        width=800,
        height=600
    )
    api = Api(window)
    window.js_api = api

    # --- Start File Watcher ---
    watcher_thread = threading.Thread(target=start_file_watcher, args=(local_web_project_dir, window), daemon=True)
    watcher_thread.start()

    webview.start(debug=True)