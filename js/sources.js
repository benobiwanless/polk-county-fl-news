fetch("../data/sources.json").then(r=>r.json()).then(sources=>{
  document.getElementById("sourceGrid").innerHTML=sources.map(s=>`
    <article class="card">
      <span class="tag">${s.type}</span>
      <h3>${s.name}</h3>
      <p class="meta">${s.status}</p>
      <p>${s.notes}</p>
      <a class="read-more" href="${s.url}" target="_blank">Open source →</a>
    </article>
  `).join("");
});
