async function loadNews() {
    try {
        const response = await fetch('news.json');
        const newsItems = await response.json();
        const container = document.getElementById('news-container');
        newsItems.forEach(item => {
            const article = document.createElement('article');

            const title = document.createElement('h2');
            title.textContent = item.title;
            article.appendChild(title);

            const date = document.createElement('p');
            date.className = 'date';
            date.textContent = item.date;
            article.appendChild(date);

            if (item.image) {
                const img = document.createElement('img');
                img.src = item.image;
                img.alt = item.title;
                article.appendChild(img);
            }

            const content = document.createElement('p');
            content.textContent = item.content;
            article.appendChild(content);

            container.appendChild(article);
        });
    } catch (err) {
        console.error('Nepodařilo se načíst zprávy:', err);
    }
}

window.addEventListener('DOMContentLoaded', loadNews);
