document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

document.getElementById('toggleDarkMode').addEventListener('click', function() {
    const enabled = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', enabled ? 'enabled' : 'disabled');
});

document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const message = document.getElementById('message');
    if (!/^\S+@\S+\.\S+$/.test(email.value)) {
        message.textContent = 'Zadejte prosim platny e-mail.';
        message.className = 'error';
        email.focus();
        return;
    }
    message.textContent = `Dekujeme, ${name.value.trim()}, brzy se vam ozveme!`;
    message.className = 'success';
    name.value = '';
    email.value = '';
});
