let workspace;

const $ = (selector, parent = document) => parent.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, character => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[character]));
const DIMENSIONS = [
  ['value', 'Potential value', 'Meaningful benefit if this Island works.'],
  ['readiness', 'Readiness', 'How prepared the team is to explore it.'],
  ['effort', 'Effort', 'Coordination and delivery effort required.'],
];

async function post(path, body) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || 'Could not save your Map.');
  return payload;
}

function currentMap(payload) {
  const iteration = payload.iterations.at(-1);
  return {name: payload.map.name, northStar: payload.map.north_star, islands: iteration.opportunities};
}

function evaluationSummary(island) {
  const values = island.evaluation || {};
  const known = DIMENSIONS.filter(([id]) => values[id]);
  if (!known.length) return '<span class="island-values-empty">Values to be explored</span>';
  return known.map(([id, label]) => `<span title="${escapeHtml(values[id].rationale)}"><b>${escapeHtml(label)}</b> ${values[id].score}/5</span>`).join('');
}

function islandMarkup(island, index) {
  const positions = ['island--northwest', 'island--northeast', 'island--southwest', 'island--southeast', 'island--centre'];
  const description = island.detail || island.description || island.summary || 'A newly charted Island.';
  return `<button class="island ${positions[index % positions.length]}" data-island-id="${escapeHtml(island.id)}" aria-label="Open Island: ${escapeHtml(island.title)}"><span class="island-shore"><span class="island-land"><span class="island-title">${escapeHtml(island.title)}</span><span class="island-note">${escapeHtml(description)}</span><span class="island-values">${evaluationSummary(island)}</span></span></span></button>`;
}

function render(payload) {
  workspace = payload;
  const map = currentMap(payload);
  $('#map-app').innerHTML = `
    <section class="map-intro">
      <p class="eyebrow">YOUR OPPORTUNITY MAP</p><h1>${escapeHtml(map.name)}</h1>
      <p class="map-intro-copy">Chart the AI opportunities your team may explore. Open an Island to record the team's current view of its value, readiness, and effort.</p>
    </section>
    <section class="north-star" aria-label="North Star context">
      <div class="compass" aria-hidden="true"><span>N</span><i></i></div>
      <div><p class="eyebrow">NORTH STAR · STRATEGIC CONTEXT</p><p class="north-star-copy">${escapeHtml(map.northStar || 'North Star context has not been set yet.')}</p></div>
    </section>
    <section class="map-board" aria-label="Island map">
      <div class="board-label"><span>THE SEA OF POSSIBILITIES</span><span>${map.islands.length} Island${map.islands.length === 1 ? '' : 's'} charted</span></div>
      <div class="waves waves--one"></div><div class="waves waves--two"></div>
      ${map.islands.map(islandMarkup).join('')}
      <button class="add-island" id="add-island"><span>+</span>Chart an Island</button>
      <p class="map-hint">Each Island holds its own visible values and the team's reasons for them.</p>
    </section>`;
  $('#add-island').addEventListener('click', openAddIsland);
  document.querySelectorAll('[data-island-id]').forEach(island => island.addEventListener('click', () => openIsland(island.dataset.islandId)));
}

function openAddIsland() {
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="add-island-form"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">CHART A NEW ISLAND</p><h2>Add an Island</h2><p class="dialog-intro">Give the Map a clear starting point. You can add the team's core view and values immediately, or return to it later.</p><label>Island name<input name="title" required maxlength="120" placeholder="e.g. Help agents find the right answer faster"></label><label>Initial description<textarea name="description" required maxlength="500" placeholder="A problem, workflow, or AI opportunity the team wants to explore…"></textarea></label><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Add to this Map</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#add-island-form').addEventListener('submit', addIsland);
}

function evaluationFields(island) {
  const evaluation = island.evaluation || {};
  return DIMENSIONS.map(([id, label, help]) => {
    const value = evaluation[id] || {};
    return `<section class="evaluation-field"><div><label>${escapeHtml(label)}<small>${escapeHtml(help)}</small></label><select name="${id}-score"><option value="">Not assessed</option>${[1,2,3,4,5].map(score => `<option value="${score}" ${value.score === score ? 'selected' : ''}>${score} / 5</option>`).join('')}</select></div><label class="rationale-label">Why does the team think this?<textarea name="${id}-rationale" maxlength="500" placeholder="Team rationale — visible alongside this value.">${escapeHtml(value.rationale || '')}</textarea></label></section>`;
  }).join('');
}

function openIsland(islandId) {
  const map = currentMap(workspace);
  const island = map.islands.find(candidate => candidate.id === islandId);
  if (!island) return;
  const originalNote = island.description || island.summary || 'This Island was created directly on the Map.';
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="edit-island-form" data-island-id="${escapeHtml(island.id)}"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">ISLAND DETAILS</p><h2>Chart this Island</h2><label>Island name<input name="title" required maxlength="120" value="${escapeHtml(island.title)}"></label><section class="island-original-note"><span>INITIAL DESCRIPTION</span><p>${escapeHtml(originalNote)}</p></section><label>Team's current view<textarea name="detail" maxlength="1000" placeholder="Describe the opportunity as the team understands it today.">${escapeHtml(island.detail || '')}</textarea></label><section class="evaluation-section"><div class="section-heading"><p class="eyebrow">ISLAND VALUES</p><p>These stay with this Island on the Map. They are not an Expedition ranking.</p></div>${evaluationFields(island)}</section><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Save Island</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#edit-island-form').addEventListener('submit', saveIsland);
}

async function addIsland(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post('/api/workspace/opportunities', {opportunity: {id: `island-${Date.now()}`, title: values.title.trim(), description: values.description.trim()}});
    $('#island-dialog').close();
    await loadWorkspace();
  } catch (error) {
    $('#form-error').textContent = error.message;
    form.querySelector('button[type="submit"]').disabled = false;
  }
}

function evaluationFrom(form) {
  const result = {};
  for (const [id] of DIMENSIONS) {
    const score = form.elements[`${id}-score`].value;
    const rationale = form.elements[`${id}-rationale`].value.trim();
    if (score || rationale) result[id] = {score: Number(score), rationale};
  }
  return result;
}

async function saveIsland(event) {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post(`/api/workspace/opportunities/${encodeURIComponent(form.dataset.islandId)}`, {title: form.elements.title.value.trim(), detail: form.elements.detail.value.trim(), evaluation: evaluationFrom(form)});
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
