fetch("data/stories.json?cache=" + Date.now())
  .then(response => response.json())
  .then(stories => {
    const cards = document.getElementById("cards");
    cards.innerHTML = stories.map(story => `
      <a class="card" href="${story.url}" target="_blank" rel="noopener">
        <div class="photo">
          <img src="${story.image}" alt="${story.title}">
          <span class="badge ${story.category}">${story.category}</span>
        </div>
        <div class="content">
          <h2>${story.title}</h2>
          <p>${story.summary}</p>
          <div class="meta">
            <span>📍 ${story.city}</span>
            <span>|</span>
            <span>${story.date}</span>
          </div>
          <span class="read">Read More →</span>
        </div>
      </a>
    `).join("");
  });
