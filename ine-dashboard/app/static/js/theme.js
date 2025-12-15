document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const storageKey = 'ine-theme';

    // 1. Cargar preferencia guardada
    const savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === 'dark') {
        htmlElement.classList.add('dark-theme');
    }

    // 2. Manejar el click
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            htmlElement.classList.toggle('dark-theme');
            
            if (htmlElement.classList.contains('dark-theme')) {
                localStorage.setItem(storageKey, 'dark');
            } else {
                localStorage.setItem(storageKey, 'light');
            }
        });
    }
});