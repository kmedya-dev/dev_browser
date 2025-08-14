console.log("JavaScript from local_web_project loaded.");

document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url-input');
    const goBtn = document.getElementById('go-btn');
    const themeBtn = document.getElementById('theme-btn');
    const langBtn = document.getElementById('lang-btn');
    const bookmarkBtn = document.getElementById('bookmark-btn');
    const bookmarks = document.getElementById('bookmarks');
    const bookmarkList = document.getElementById('bookmark-list');

    goBtn.addEventListener('click', () => {
        const value = urlInput.value;
        if (value) {
            window.pywebview.api.load_url(value);
        }
    });

    themeBtn.addEventListener('click', () => {
        window.pywebview.api.toggle_theme();
    });

    langBtn.addEventListener('click', () => {
        window.pywebview.api.toggle_language();
    });

    bookmarkBtn.addEventListener('click', () => {
        const url = window.pywebview.api.get_current_url();
        window.pywebview.api.add_bookmark(url);
    });

    window.pywebview.api.get_bookmarks().then(bookmarks => {
        bookmarkList.innerHTML = '';
        bookmarks.forEach(url => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = url;
            a.addEventListener('click', () => {
                window.pywebview.api.load_url(url);
            });
            li.appendChild(a);
            bookmarkList.appendChild(li);
        });
    });
});