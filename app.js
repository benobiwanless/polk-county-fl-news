const fallbackImage = 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80';

function badgeClass(category='development'){
  return category.toLowerCase().replace(/\s+/g,'-');
}
function formatDate(value){
  if(!value) return '';
  const date = new Date(value);
  if(Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(undefined,{month:'short',day:'numeric',year:'numeric'});
}
function badge(label, extra=''){
  return `<span class="badge ${extra || badgeClass(label)}">${label}</span>`;
}
function renderFeatured(item){
  const el = document.getElementById('featuredProject');
  el.innerHTML = `
    <img src="${item.image || fallbackImage}" alt="${item.title}">
    <div class="featured-body">
      <div class="badges">${badge(item.category)}${item.status ? badge(item.status,'status') : ''}</div>
      <h3>${item.title}</h3>
      <div class="meta">📍 ${item.city || 'Polk County'}, FL</div>
      <p>${item.summary || ''}</p>
      <div class="details-row">
        <span>🗓 ${formatDate(item.date)}</span>
        ${item.units ? `<span>🏢 ${item.units}</span>` : ''}
        <a class="button" href="${item.url || '#'}" target="_blank" rel="noopener">View Details →</a>
      </div>
    </div>`;
}
function renderCards(items){
  const grid = document.getElementById('newsGrid');
  grid.innerHTML = items.map(item => `
    <article class="news-card">
      <div class="news-image-wrap">
        <img src="${item.image || fallbackImage}" alt="${item.title}">
        ${badge(item.category)}
      </div>
      <div class="news-body">
        <h3>${item.title}</h3>
        <div class="meta">📍 ${item.city || 'Polk County'}, FL</div>
        <p>${item.summary || ''}</p>
        <div class="card-footer"><span>${formatDate(item.date)}</span><a href="${item.url || '#'}" target="_blank" rel="noopener">Read More →</a></div>
      </div>
    </article>`).join('');
}
async function init(){
  try{
    const res = await fetch('data/news.json', {cache:'no-store'});
    const data = await res.json();
    const items = data.items || [];
    renderFeatured(data.featured || items[0]);
    renderCards(items.filter(i => !i.featured).slice(0,12));
    document.getElementById('lastUpdated').textContent = data.updated ? `Last updated ${formatDate(data.updated)}` : '';
  }catch(err){
    console.error(err);
    document.getElementById('newsGrid').innerHTML = '<p>News feed loading.</p>';
  }
}
init();
