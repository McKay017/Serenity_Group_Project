document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menu-button');
    const menu = document.getElementById('menu');

    menuButton.addEventListener('click', function() {
        if (menu.style.display === 'block') {
            menu.style.maxHeight = '0';
            setTimeout(() => { menu.style.display = 'none'; }, 300); // Match the transition duration
        } else {
            menu.style.display = 'block';
            setTimeout(() => { menu.style.maxHeight = menu.scrollHeight + 'px'; }, 10); // Match the transition duration
        }
    });
});

