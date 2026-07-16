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
    expedition: payload.expedition,
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
  $('#map-app').innerHTML = `
    <section class="map-intro">
      <div class="map-title-row"><p class="eyebrow">YOUR OPPORTUNITY MAP</p><label class="map-name-label"><span class="sr-only">Map name</span><input id="map-name" value="${escapeHtml(map.customName)}" placeholder="Name this Map"></label></div>
      <label class="focus-field"><span>What do you want to explore?</span><textarea id="map-focus" placeholder="Describe the goal, problem, or question your team is exploring.">${escapeHtml(map.mapFocus)}</textarea></label>
    </section>
    <section class="north-star" aria-label="North Star context">
      <div class="compass" aria-hidden="true"><span>N</span><i></i></div>
      <div><p class="eyebrow">NORTH STAR · STRATEGIC CONTEXT</p><p class="north-star-copy">${escapeHtml(map.northStar || 'North Star context has not been set yet.')}</p></div>
    </section>
    <section class="expedition-launch" aria-label="Expedition preparation">
      <div><p class="eyebrow">TEAM PRIORITIES</p><h2>Prepare an Expedition</h2><p>Compare every Island using the team’s visible inputs, then choose the order together.</p></div>
      <button class="primary" id="prepare-expedition" type="button">Prepare an Expedition</button>
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
  $('#prepare-expedition').addEventListener('click', openExpeditionPreparation);
  document.querySelectorAll('[data-island-id]').forEach(island => {
    island.addEventListener('click', () => openIsland(island.dataset.islandId));
  });
}

function scoreOptions(selected) {
  return [1, 2, 3, 4, 5].map(score => `<option value="${score}"${score === selected ? ' selected' : ''}>${score}</option>`).join('');
}

function expeditionValues(form) {
  return Object.fromEntries(currentMap(workspace).opportunities.map(island => [island.id, {
    impact: Number(form.elements[`impact-${island.id}`].value),
    readiness: Number(form.elements[`readiness-${island.id}`].value),
  }]));
}

function openExpeditionPreparation() {
  const map = currentMap(workspace);
  const evaluations = map.expedition.evaluations;
  const rows = map.opportunities.map(island => {
    const values = evaluations[island.id] || {impact: 3, readiness: 3};
    return `<tr><th scope="row">${escapeHtml(island.title)}</th><td><label class="sr-only" for="impact-${escapeHtml(island.id)}">Impact for ${escapeHtml(island.title)}</label><select id="impact-${escapeHtml(island.id)}" name="impact-${escapeHtml(island.id)}">${scoreOptions(values.impact)}</select></td><td><label class="sr-only" for="readiness-${escapeHtml(island.id)}">Readiness for ${escapeHtml(island.title)}</label><select id="readiness-${escapeHtml(island.id)}" name="readiness-${escapeHtml(island.id)}">${scoreOptions(values.readiness)}</select></td></tr>`;
  }).join('');
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="expedition-evaluations"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">PREPARE AN EXPEDITION</p><h2>What is worth exploring now?</h2><p class="dialog-intro">Add the Map evaluation inputs together. The suggested order is the equal average of Impact and readiness—nothing is hidden.</p><table class="evaluation-table"><thead><tr><th>Island</th><th>Impact <small>1–5</small></th><th>Readiness <small>1–5</small></th></tr></thead><tbody>${rows}</tbody></table><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Review suggested order</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#expedition-evaluations').addEventListener('submit', saveExpeditionEvaluations);
}

async function saveExpeditionEvaluations(event) {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    const payload = await post('/api/workspace/expedition/evaluations', {evaluations: expeditionValues(form)});
    workspace = payload;
    openExpeditionConfirmation(payload.expedition.suggested_order.map(entry => entry.island_id));
  } catch (error) {
    $('#form-error').textContent = error.message;
    form.querySelector('button[type="submit"]').disabled = false;
  }
}

function openExpeditionConfirmation(order) {
  const map = currentMap(workspace);
  const suggested = map.expedition.suggested_order.map(entry => entry.island_id);
  const cards = order.map((id, index) => {
    const island = map.opportunities.find(item => item.id === id);
    const values = map.expedition.evaluations[id];
    const suggestedPosition = suggested.indexOf(id) + 1;
    const adjustment = suggestedPosition === index + 1 ? 'Suggested position' : `Team-adjusted from suggested #${suggestedPosition}`;
    return `<li class="expedition-island"><span class="expedition-position">${index + 1}</span><div><strong>${escapeHtml(island.title)}</strong><small>Impact ${values.impact} · readiness ${values.readiness} · ${adjustment}</small></div><span class="order-controls"><button type="button" data-move="up" data-island-id="${escapeHtml(id)}" ${index === 0 ? 'disabled' : ''} aria-label="Move ${escapeHtml(island.title)} up">↑</button><button type="button" data-move="down" data-island-id="${escapeHtml(id)}" ${index === order.length - 1 ? 'disabled' : ''} aria-label="Move ${escapeHtml(island.title)} down">↓</button></span></li>`;
  }).join('');
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<section class="expedition-confirmation"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">TEAM CONFIRMATION</p><h2>Set the Expedition order</h2><p class="dialog-intro">Adjust the suggested order if needed. Confirming preserves this Island and evaluation snapshot; your Map remains editable.</p><ol class="expedition-order">${cards}</ol><p class="form-error" id="form-error" role="alert"></p><button class="primary" id="confirm-expedition" type="button">Confirm this Expedition</button></section>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  document.querySelectorAll('[data-move]').forEach(button => button.addEventListener('click', () => {
    const index = order.indexOf(button.dataset.islandId);
    const swapWith = button.dataset.move === 'up' ? index - 1 : index + 1;
    [order[index], order[swapWith]] = [order[swapWith], order[index]];
    openExpeditionConfirmation(order);
  }));
  $('#confirm-expedition').addEventListener('click', () => confirmExpedition(order));
}

async function confirmExpedition(order) {
  try {
    $('#confirm-expedition').disabled = true;
    const result = await post('/api/workspace/expeditions', {ordered_island_ids: order});
    workspace = result.workspace;
    $('#island-dialog').close();
    render(workspace);
    showConfirmedExpedition(result.expedition);
  } catch (error) {
    $('#form-error').textContent = error.message;
    $('#confirm-expedition').disabled = false;
  }
}

function showConfirmedExpedition(expedition) {
  const islands = Object.fromEntries(expedition.islands.map(island => [island.id, island]));
  const rows = expedition.ordered_island_ids.map((id, index) => `<li class="expedition-island"><span class="expedition-position">${index + 1}</span><div><strong>${escapeHtml(islands[id].title)}</strong><small>Impact ${expedition.evaluations[id].impact} · readiness ${expedition.evaluations[id].readiness}</small></div></li>`).join('');
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<section class="expedition-confirmation"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">EXPEDITION CONFIRMED</p><h2>Your team’s snapshot is preserved</h2><p class="dialog-intro">This read-only Expedition records the Islands and Map evaluation inputs at this moment. Your Map remains open for further work.</p><ol class="expedition-order">${rows}</ol><button class="primary" id="return-to-map" type="button">Return to the Map</button></section>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#return-to-map').addEventListener('click', () => dialog.close());
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
