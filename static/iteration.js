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
    sourceNumber: map.source_number,
    reviewPending: map.review_pending,
  };
}

function islandMarkup(opportunity, index) {
  const positions = ['island--northwest', 'island--northeast', 'island--southwest', 'island--southeast', 'island--centre'];
  const description = opportunity.detail || opportunity.description || opportunity.summary || 'A rough team note waiting to be shaped.';
  return `<button class="island ${positions[index % positions.length]}" data-island-id="${escapeHtml(opportunity.id)}" aria-label="Open Island: ${escapeHtml(opportunity.title)}"><span class="island-shore"><span class="island-land"><span class="island-title">${escapeHtml(opportunity.title)}</span><span class="island-note">${escapeHtml(description)}</span></span></span></button>`;
}

function render(payload) {
  workspace = payload;
  const map = currentMap(payload);
  const archivedCount = (payload.carry_forward_review || []).filter(item => item.archived).length;
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
    </section>
    <section class="map-actions" aria-label="Map actions">
      <button class="secondary" id="start-later-map">Start a new Map</button>
      ${map.sourceNumber && archivedCount ? `<button class="secondary" id="review-archives">Review ${archivedCount} archived Island${archivedCount === 1 ? '' : 's'}</button>` : ''}
    </section>`;

  bindMapInteractions();
  if (map.reviewPending) showIslandReview();
}

function bindMapInteractions() {
  ['map-name', 'map-focus'].forEach(id => {
    $(`#${id}`).addEventListener('input', scheduleMapSave);
    $(`#${id}`).addEventListener('blur', saveMap);
  });
  $('#add-island').addEventListener('click', openAddIsland);
  $('#start-later-map').addEventListener('click', openLaterMapStart);
  const reviewArchives = $('#review-archives');
  if (reviewArchives) reviewArchives.addEventListener('click', openArchiveRegister);
  document.querySelectorAll('[data-island-id]').forEach(island => {
    island.addEventListener('click', () => openIsland(island.dataset.islandId));
  });
}

function journeyDialog() {
  return $('#journey-dialog');
}

function openLaterMapStart() {
  const map = currentMap(workspace);
  const dialog = journeyDialog();
  dialog.innerHTML = `<form id="later-map-start"><button type="button" class="dialog-close" id="close-journey" aria-label="Close">×</button><p class="eyebrow">START A NEW MAP</p><h2>Where should the next Map point?</h2><p class="dialog-intro">Keep the focus from the previous Map, or reshape it for what the team needs now.</p><label>Keep the focus from the previous Map?<textarea name="focus" required maxlength="800">${escapeHtml(map.mapFocus)}</textarea></label><p class="form-error" id="journey-error" role="alert"></p><button class="primary" type="submit">Review inherited Islands</button></form>`;
  dialog.showModal();
  $('#close-journey').addEventListener('click', () => dialog.close());
  $('#later-map-start').addEventListener('submit', beginLaterMap);
}

async function beginLaterMap(event) {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    workspace = await post('/api/workspace/later-map', {focus: new FormData(form).get('focus').trim()});
    showIslandReview();
  } catch (error) {
    $('#journey-error').textContent = error.message;
    form.querySelector('button[type="submit"]').disabled = false;
  }
}

function reviewableIslands() {
  return (workspace.carry_forward_review || []).filter(item => !item.reviewed);
}

function keepJourneyOpen(dialog) {
  dialog.addEventListener('cancel', event => event.preventDefault());
}

async function showIslandReview() {
  const islands = reviewableIslands();
  if (!islands.length) {
    workspace = await post('/api/workspace/carry-forward/complete', {});
    return showMapReady();
  }
  const reviewedCount = (workspace.carry_forward_review || []).length - islands.length;
  const item = islands[0];
  const island = item.opportunity;
  const dialog = journeyDialog();
  dialog.innerHTML = `<section class="journey-step"><p class="eyebrow">INHERITED ISLAND ${reviewedCount + 1} OF ${(workspace.carry_forward_review || []).length}</p><h2>${escapeHtml(island.title)}</h2><p class="journey-note">${escapeHtml(island.detail || island.description || island.summary || 'No note recorded.')}</p><p class="dialog-intro">Keep this Island on the new Map by default, or archive it if it no longer belongs.</p><div class="journey-actions"><button class="primary" id="keep-island">Keep on this Map</button><button class="secondary" id="archive-island">Archive Island</button></div></section>`;
  if (!dialog.open) {
    dialog.showModal();
    keepJourneyOpen(dialog);
  }
  $('#keep-island').addEventListener('click', async () => {
    workspace = await post('/api/workspace/keep', {opportunity_id: island.id});
    showIslandReview();
  });
  $('#archive-island').addEventListener('click', () => showArchiveReason(item));
}

function showArchiveReason(item) {
  const island = item.opportunity;
  const dialog = journeyDialog();
  dialog.innerHTML = `<form id="archive-island-form" data-island-id="${escapeHtml(island.id)}"><button type="button" class="dialog-close" id="close-journey" aria-label="Close">×</button><p class="eyebrow">ARCHIVE ISLAND</p><h2>Why archive ${escapeHtml(island.title)}?</h2><p class="dialog-intro">This short reason stays with the new Map. You can restore the Island while this Map is open.</p><label>Archive reason<textarea name="reason" required maxlength="500" placeholder="e.g. This no longer fits the focus of this Map."></textarea></label><p class="form-error" id="journey-error" role="alert"></p><div class="journey-actions"><button class="primary" type="submit">Archive Island</button><button class="secondary" type="button" id="back-to-island">Back</button></div></form>`;
  $('#close-journey').addEventListener('click', () => showIslandReview());
  $('#back-to-island').addEventListener('click', () => showIslandReview());
  $('#archive-island-form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    try {
      form.querySelector('button[type="submit"]').disabled = true;
      workspace = await post('/api/workspace/archive', {opportunity_id: form.dataset.islandId, reason: new FormData(form).get('reason').trim()});
      showIslandReview();
    } catch (error) {
      $('#journey-error').textContent = error.message;
      form.querySelector('button[type="submit"]').disabled = false;
    }
  });
}

function showMapReady() {
  const map = currentMap(workspace);
  const dialog = journeyDialog();
  dialog.innerHTML = `<form id="map-ready-form"><p class="eyebrow">MAP READY</p><h2>${escapeHtml(map.name)}</h2><p class="dialog-intro">Your new Map is open for exploration. Name it now, or keep the atlas suggestion.</p><label>Name this Map<input name="name" required maxlength="120" value="${escapeHtml(map.name)}"></label><p class="form-error" id="journey-error" role="alert"></p><button class="primary" type="submit">Open this Map</button></form>`;
  $('#map-ready-form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    try {
      workspace = await post('/api/workspace/map', {name: new FormData(form).get('name').trim(), focus: map.mapFocus});
      dialog.close();
      render(workspace);
    } catch (error) {
      $('#journey-error').textContent = error.message;
    }
  });
}

function openArchiveRegister() {
  const archived = (workspace.carry_forward_review || []).filter(item => item.archived);
  const dialog = journeyDialog();
  dialog.innerHTML = `<section class="journey-step"><button type="button" class="dialog-close" id="close-journey" aria-label="Close">×</button><p class="eyebrow">ARCHIVED ISLANDS</p><h2>Still within reach</h2><p class="dialog-intro">Archived Islands are excluded from this Map, but you can restore them while it remains open.</p>${archived.map(item => `<article class="archive-entry"><strong>${escapeHtml(item.opportunity.title)}</strong><p>${escapeHtml(item.opportunity.summary || item.opportunity.description || '')}</p><button class="secondary" data-restore-id="${escapeHtml(item.opportunity.id)}">Restore to this Map</button></article>`).join('')}</section>`;
  dialog.showModal();
  $('#close-journey').addEventListener('click', () => dialog.close());
  dialog.querySelectorAll('[data-restore-id]').forEach(button => button.addEventListener('click', async () => {
    workspace = await post('/api/workspace/restore', {opportunity_id: button.dataset.restoreId});
    dialog.close();
    render(workspace);
  }));
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

function openIsland(islandId) {
  const map = currentMap(workspace);
  const island = map.opportunities.find(opportunity => opportunity.id === islandId);
  if (!island) return;
  const originalNote = island.description || island.summary || 'No original team note was recorded.';
  const aiFormulation = island.ai_formulation
    ? escapeHtml(island.ai_formulation)
    : '<em>No AI formulation has been added.</em>';
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="develop-island-form" data-island-id="${escapeHtml(island.id)}"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">ISLAND CHART</p><h2>${escapeHtml(island.title)}</h2><section class="island-original-note"><span>ORIGINAL TEAM NOTE</span><p>${escapeHtml(originalNote)}</p></section><section class="island-ai-formulation"><span>AI FORMULATION</span><p>${aiFormulation}</p></section><section class="island-context"><span>MAP CONTEXT</span><strong>${escapeHtml(map.mapFocus)}</strong><small>North Star: ${escapeHtml(map.northStar || 'Not set')}</small></section><label>Develop this Island<textarea name="detail" maxlength="1000" placeholder="Add the problem, workflow, or opportunity as the team understands it.">${escapeHtml(island.detail || '')}</textarea></label><label>Next move<textarea name="next_move" maxlength="500" placeholder="What should the team do next?">${escapeHtml(island.next_move || '')}</textarea></label><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Save Island detail</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#develop-island-form').addEventListener('submit', saveIsland);
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

async function saveIsland(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post(`/api/workspace/opportunities/${encodeURIComponent(form.dataset.islandId)}`, values);
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
