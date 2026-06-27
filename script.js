const icons = {
  Restaurants: "🍔",
  Housing: "🏠",
  Roads: "🛣️",
  Hotels: "🏨",
  Retail: "🛍️",
  Development: "🏗️",
  Business: "💼"
};

let stories = [];
let active = "All";

fetch("data/stories.json?cache=" + Date.now())
  .then(r => r.json())
  .then(data => {
    stories = data;
    render();
  })
  .catch(() => {
    document.getElementById("status").textContent = "Stories could not load. Check data/stories.json.";
  });

document.querySelectorAll("[data-category]").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("[data-category]").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    active = btn.dataset.category;
    render();
  });
});

function render() {
  const filtered = active === "All" ? stories : stories.filter(s => s.category === active);
  document.getElementById("status").textContent = `${filtered.length} positive growth stor${filtered.length === 1 ? "y" : "ies"} showing`;
  document.getElementById("grid").innerHTML = filtered.map(story => `
    <a class="card" href="${story.url}" target="_blank" rel="noopener">
      <div class="thumb">
        ${icons[story.category] || "🏗️"}
        <span class="badge ${story.category}">${story.category}</span>
      </div>
      <div class="body">
        <h2>${story.title}</h2>
        <p>${story.summary}</p>
        <div class="meta">
          <span>📍 ${story.city}</span>
          <span>|</span>
          <span>${story.date || ""}</span>
        </div>
        <div class="read">Read More →</div>
      </div>
    </a>
  `).join("");
}
