document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const message = document.getElementById('message');
    message.textContent = `Dekujeme, ${name}, brzy se vam ozveme!`;
});
