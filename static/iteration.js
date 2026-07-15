let workspace;
let saveTimer;

const $ = (selector, parent = document) => parent.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, character => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[character]));

async function post(path, body) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || 'Could not save your Map.');
  return payload;
}

function currentMap(payload) {
  const iteration = payload.iterations.at(-1);
  const map = payload.map;
  return {
    customName: map.name,
    mapFocus: map.focus,
    northStar: map.north_star,
    opportunities: iteration.opportunities,
  };
}

function islandMarkup(opportunity, index) {
  const positions = ['island--northwest', 'island--northeast', 'island--southwest', 'island--southeast', 'island--centre'];
  const description = opportunity.description || opportunity.summary || 'A rough team note waiting to be shaped.';
  return `<article class="island ${positions[index % positions.length]}" aria-label="Island: ${escapeHtml(opportunity.title)}"><span class="island-shore"><span class="island-land"><span class="island-title">${escapeHtml(opportunity.title)}</span><span class="island-note">${escapeHtml(description)}</span></span></span></article>`;
}

function render(payload) {
  workspace = payload;
  const map = currentMap(payload);
  $('#map-app').innerHTML = `
    <section class="map-intro">
      <div class="map-title-row"><p class="eyebrow">YOUR OPPORTUNITY MAP</p><label class="map-name-label"><span class="sr-only">Map name</span><input id="map-name" value="${escapeHtml(map.customName)}" placeholder="Name this Map"></label></div>
      <label class="focus-field"><span>What do you want to explore?</span><textarea id="map-focus" placeholder="Describe the goal, problem, or question your team is exploring.">${escapeHtml(map.mapFocus)}</textarea></label>
    </section>
    <section class="north-star" aria-label="North Star context">
      <div class="compass" aria-hidden="true"><span>N</span><i></i></div>
      <div><p class="eyebrow">NORTH STAR · STRATEGIC CONTEXT</p><p class="north-star-copy">${escapeHtml(map.northStar || 'North Star context has not been set yet.')}</p></div>
    </section>
    <section class="map-board" aria-label="Island map">
      <div class="board-label"><span>THE SEA OF POSSIBILITIES</span><span>${map.opportunities.length} island${map.opportunities.length === 1 ? '' : 's'} charted</span></div>
      <div class="waves waves--one"></div><div class="waves waves--two"></div>
      ${map.opportunities.map(islandMarkup).join('')}
      <button class="add-island" id="add-island"><span>+</span>Add an opportunity</button>
      <p class="map-hint">Start with a rough idea. You can develop an Island together later.</p>
    </section>`;

  bindMapInteractions();
}

function bindMapInteractions() {
  ['map-name', 'map-focus'].forEach(id => {
    $(`#${id}`).addEventListener('input', scheduleMapSave);
    $(`#${id}`).addEventListener('blur', saveMap);
  });
  $('#add-island').addEventListener('click', openAddIsland);
}

function scheduleMapSave() {
  clearTimeout(saveTimer);
  $('#save-status').textContent = 'Saving…';
  saveTimer = setTimeout(saveMap, 700);
}

async function saveMap() {
  clearTimeout(saveTimer);
  const body = {name: $('#map-name').value.trim(), focus: $('#map-focus').value.trim()};
  try {
    $('#save-status').textContent = 'Saving…';
    await post('/api/workspace/map', body);
    $('#save-status').textContent = 'Saved';
  } catch (error) {
    $('#save-status').textContent = `Not saved — ${error.message}`;
  }
}

function openAddIsland() {
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="add-island-form"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">CHART A NEW ISLAND</p><h2>Add an opportunity</h2><p class="dialog-intro">A simple note is enough. The team can develop it later.</p><label>Opportunity name<input name="title" required maxlength="120" placeholder="e.g. Help agents find the right answer faster"></label><label>What is the opportunity?<textarea name="description" required maxlength="500" placeholder="A rough problem, workflow, or use-case idea…"></textarea></label><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Add to this Map</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#add-island-form').addEventListener('submit', addIsland);
}

async function addIsland(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  const opportunity = {id: `island-${Date.now()}`, title: values.title.trim(), description: values.description.trim()};
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post('/api/workspace/opportunities', {opportunity});
    $('#island-dialog').close();
    await loadWorkspace();
  } catch (error) {
    $('#form-error').textContent = error.message;
    form.querySelector('button[type="submit"]').disabled = false;
  }
}

async function loadWorkspace() {
  try {
    const response = await fetch('/api/workspace');
    if (!response.ok) throw new Error('Could not load this Map.');
    render(await response.json());
  } catch (error) {
    $('#map-app').innerHTML = `<p class="load-error">${escapeHtml(error.message)}</p>`;
  }
}

loadWorkspace();
