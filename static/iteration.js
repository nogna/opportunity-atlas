let workspace;
let mapNameSaveTimer;
let activeDestination = 'map';
let expeditionDraft = {};

const $ = (selector, parent = document) => parent.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, character => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[character]));
const DIMENSIONS = [
  ['value', 'Potential value', 'Meaningful benefit if this Island works.'],
  ['readiness', 'Readiness', 'How prepared the team is to explore it.'],
  ['effort', 'Effort', 'Coordination and delivery effort required.'],
];
const CHART_ROOM_FIELDS = [
  ['workflow_problem', 'Workflow / problem today', 'Who does what today, where does friction or a decision sit, and who is affected?', 'core'],
  ['ai_change', 'Possible AI-enabled change', 'Keep human accountability explicit. This is a proposal, not a promise.', 'core'],
  ['outcome', 'Possible outcome', 'Use an observable or measurable benefit; a formal ROI forecast is not required.', 'core wide'],
  ['evidence', 'Team evidence', 'Observations, links, or constraints the team can stand behind.', 'evidence'],
  ['unknowns', 'Unknowns & assumptions', 'State what is missing or unverified instead of smoothing it over.', 'evidence'],
];
const CHART_ROOM_DETAILS = [
  ['workflow_sketch', 'Workflow sketch', 'Clarify the handoff', 'Today → AI-enabled change → human review → outcome.'],
  ['readiness_data', 'Readiness & data', 'Open when moving toward delivery', 'Check access, quality, consistency, retention, and the integrations needed for a useful review point.'],
  ['safeguards_risk', 'Safeguards & risk', 'Open early for sensitive work', 'Name harms, oversight, escalation, and an accountable owner.'],
  ['ownership_adoption', 'Ownership & adoption', 'Open when roles will change', 'Who reviews the result, who can override it, and what changes in their routine?'],
  ['learning_action', 'Next learning action', 'Open when preparing an Expedition', 'Describe the smallest action that could strengthen or weaken this hypothesis.'],
];

async function post(path, body) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || 'Could not save your Map.');
  return payload;
}

function currentMap(payload) {
  const iteration = payload.iterations.at(-1);
  return {name: payload.map.name, northStar: payload.map.north_star, islands: iteration.opportunities, scoutingNotes: iteration.scouting_notes || []};
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

function scoutingNotesMarkup(notes) {
  if (!notes.length) {
    return `<p class="scouting-empty">A personal observation can wait here until the team is ready to chart it as an Island.</p>`;
  }
  return notes.map(note => {
    const transferred = note.transferred_to_island_id;
    return `<article class="scouting-note ${transferred ? 'scouting-note--transferred' : ''}">
      <p class="eyebrow">${transferred ? 'NOW AN ISLAND' : 'PERSONAL SCOUTING NOTE'}</p>
      <h3>${escapeHtml(note.title)}</h3><p>${escapeHtml(note.body)}</p>
      <footer><span>Added by ${escapeHtml(note.author)}</span>${transferred
        ? `<button class="text-button open-transferred-island" data-island-id="${escapeHtml(transferred)}">Open Island</button>`
        : `<button class="secondary transfer-note" data-note-id="${escapeHtml(note.id)}">Chart as Island</button>`}</footer>
    </article>`;
  }).join('');
}

function render(payload) {
  workspace = payload;
  document.querySelectorAll('[data-destination]').forEach(button => {
    button.classList.toggle('is-active', button.dataset.destination === activeDestination);
  });
  if (activeDestination === 'expedition') {
    renderExpedition(payload);
    return;
  }
  const map = currentMap(payload);
  $('#map-app').innerHTML = `
    <section class="map-intro">
      <p class="eyebrow">YOUR OPPORTUNITY MAP</p><label class="map-name-label"><span class="sr-only">Map name</span><input id="map-name" value="${escapeHtml(map.name)}" aria-label="Map name"></label>
      <p class="map-intro-copy">Chart the AI opportunities your team may explore. Open an Island to record the team's current view of its value, readiness, and effort.</p>
    </section>
    <section class="north-star" aria-label="North Star context">
      <div class="compass" aria-hidden="true"><span>N</span><i></i></div>
      <div><p class="eyebrow">NORTH STAR · STRATEGIC CONTEXT</p><p class="north-star-copy">${escapeHtml(map.northStar || 'North Star context has not been set yet.')}</p></div>
    </section>
    <section class="scouting-dock" aria-label="Personal Scouting notes">
      <div class="scouting-dock-heading"><div><p class="eyebrow">BEFORE EXPEDITION PLANNING</p><h2>Scouting notes</h2><p>Personal early signals—not yet Islands and not team evidence.</p></div><button class="secondary" id="add-scouting-note">+ Add a note</button></div>
      <div class="scouting-notes">${scoutingNotesMarkup(map.scoutingNotes)}</div>
    </section>
    <section class="map-board" aria-label="Island map">
      <div class="board-label"><span>THE SEA OF POSSIBILITIES</span><span>${map.islands.length} Island${map.islands.length === 1 ? '' : 's'} charted</span></div>
      <div class="waves waves--one"></div><div class="waves waves--two"></div>
      ${map.islands.map(islandMarkup).join('')}
      <button class="add-island" id="add-island"><span>+</span>Chart an Island</button>
      <p class="map-hint">Each Island holds its own visible values and the team's reasons for them.</p>
    </section>`;
  $('#add-island').addEventListener('click', openAddIsland);
  $('#add-scouting-note').addEventListener('click', openAddScoutingNote);
  document.querySelectorAll('[data-island-id]').forEach(island => island.addEventListener('click', () => openIsland(island.dataset.islandId)));
  document.querySelectorAll('.transfer-note').forEach(button => button.addEventListener('click', () => openTransferScoutingNote(button.dataset.noteId)));
  document.querySelectorAll('.open-transferred-island').forEach(button => button.addEventListener('click', () => openIsland(button.dataset.islandId)));
  $('#map-name').addEventListener('input', scheduleMapNameSave);
  $('#map-name').addEventListener('blur', saveMapName);
}

function islandExpeditionContext(island) {
  const chart = island.chart_room || {};
  const hypothesis = chart.workflow_problem || island.detail || island.description || island.summary || 'This Island has not yet been described.';
  const gap = chart.unknowns || 'No unknowns have been recorded yet.';
  return `<div class="expedition-context"><p class="eyebrow">FROM THE CHART ROOM · READ ONLY</p><p>${escapeHtml(hypothesis)}</p><p><b>Known gap:</b> ${escapeHtml(gap)}</p><div class="expedition-values">${evaluationSummary(island)}</div></div>`;
}

function charterMarkup(island) {
  const charter = expeditionDraft[island.id] || {};
  return `<article class="island-flag">
    <header><p class="eyebrow">ISLAND CHARTER</p><h3>${escapeHtml(island.title)}</h3></header>
    ${islandExpeditionContext(island)}
    <label class="charter-field charter-action">Next learning action <span>required</span>
      <textarea data-charter-field="next_learning_action" data-island-id="${escapeHtml(island.id)}" maxlength="2000" placeholder="The smallest useful learning move…">${escapeHtml(charter.next_learning_action || '')}</textarea>
    </label>
    <details class="charter-details"><summary>Optional Charter details</summary>
      <label class="charter-field">Participants<input data-charter-field="participants" data-island-id="${escapeHtml(island.id)}" maxlength="500" value="${escapeHtml(charter.participants || '')}" placeholder="Who needs to take part?"></label>
      <label class="charter-field">Intended outcome<textarea data-charter-field="intended_outcome" data-island-id="${escapeHtml(island.id)}" maxlength="2000" placeholder="A useful result for this Island in this Expedition…">${escapeHtml(charter.intended_outcome || '')}</textarea></label>
      <label class="charter-field">Decision evidence<textarea data-charter-field="decision_evidence" data-island-id="${escapeHtml(island.id)}" maxlength="2000" placeholder="What would help the team continue, adjust, or stop?">${escapeHtml(charter.decision_evidence || '')}</textarea></label>
    </details>
  </article>`;
}

function activeExpeditionMarkup(expedition, islands) {
  const islandById = new Map(islands.map(island => [island.id, island]));
  return `<section class="expedition-active"><p class="eyebrow">ACTIVE EXPEDITION · MAP SNAPSHOT CAPTURED</p><h1>Island flags are flying.</h1><p class="expedition-intro">The living Map can continue to evolve. This Expedition keeps the Charters the team confirmed together.</p>
    <section class="active-charters">${expedition.charters.map(charter => {
      const island = islandById.get(charter.island_id) || expedition.map_snapshot.islands.find(item => item.id === charter.island_id) || {title: 'Archived Island'};
      return `<article class="active-charter"><p class="eyebrow">${escapeHtml(island.title)}</p><h3>${escapeHtml(charter.next_learning_action)}</h3>${charter.participants ? `<p><b>With:</b> ${escapeHtml(charter.participants)}</p>` : ''}${charter.intended_outcome ? `<p><b>For:</b> ${escapeHtml(charter.intended_outcome)}</p>` : ''}${charter.decision_evidence ? `<p><b>Evidence:</b> ${escapeHtml(charter.decision_evidence)}</p>` : ''}</article>`;
    }).join('')}</section>
    <aside class="snapshot-note"><b>Map snapshot saved</b><span>${escapeHtml(expedition.map_snapshot.name)} as confirmed. The comparison with today’s Map is intentionally a later step.</span></aside>
    <button class="secondary" id="start-new-expedition">Start another Expedition</button>
  </section>`;
}

function renderExpedition(payload) {
  const map = currentMap(payload);
  const active = payload.expedition;
  if (active && !expeditionDraft.__new) {
    $('#map-app').innerHTML = activeExpeditionMarkup(active, map.islands);
    $('#start-new-expedition').addEventListener('click', () => { expeditionDraft = {__new: true}; render(workspace); });
    return;
  }
  const selectedIds = Object.keys(expeditionDraft).filter(id => id !== '__new');
  const selected = map.islands.filter(island => selectedIds.includes(island.id));
  const allActionsNamed = selected.length && selected.every(island => expeditionDraft[island.id].next_learning_action?.trim());
  $('#map-app').innerHTML = `<section class="expedition-page">
    <header class="expedition-heading"><p class="eyebrow">EXPEDITION · ISLAND FLAGS</p><h1>Give each Island its first leg.</h1><p>Choose prepared Islands from the living Map. Their Chart Room context and values stay inherited; an Island Charter only records what this Expedition will do next.</p></header>
    <section class="expedition-selector"><div><p class="eyebrow">ISLANDS ABOARD</p><h2>Choose the focus set</h2></div><div class="island-picks">${map.islands.map(island => `<label class="island-pick ${selectedIds.includes(island.id) ? 'island-pick--selected' : ''}"><input type="checkbox" data-select-island="${escapeHtml(island.id)}" ${selectedIds.includes(island.id) ? 'checked' : ''}><span><b>${escapeHtml(island.title)}</b><small>${escapeHtml(island.summary || island.description || 'Prepared Island')}</small></span></label>`).join('')}</div></section>
    <section class="charter-flags">${selected.length ? selected.map(charterMarkup).join('') : '<p class="expedition-empty">Select one or more Islands to give them an Expedition-specific Charter. Their durable opportunity work remains in the Chart Room.</p>'}</section>
    <footer class="expedition-summary"><div><p class="eyebrow">EXPEDITION ASSEMBLED FROM CHARTERS</p><h2>${selected.length ? `${selected.length} Island${selected.length === 1 ? '' : 's'} aboard` : 'No Islands aboard yet'}</h2><p id="charter-progress">${selected.length ? `${selected.filter(island => expeditionDraft[island.id].next_learning_action?.trim()).length}/${selected.length} next learning actions named.` : 'No generic Expedition mission is required.'}</p></div><button class="primary" id="confirm-expedition" ${allActionsNamed ? '' : 'disabled'}>Confirm Map snapshot</button></footer>
    <p class="form-error" id="expedition-error" role="alert"></p>
  </section>`;
  document.querySelectorAll('[data-select-island]').forEach(input => input.addEventListener('change', () => {
    if (input.checked) expeditionDraft[input.dataset.selectIsland] = expeditionDraft[input.dataset.selectIsland] || {};
    else delete expeditionDraft[input.dataset.selectIsland];
    render(workspace);
  }));
  document.querySelectorAll('[data-charter-field]').forEach(field => field.addEventListener('input', () => {
    expeditionDraft[field.dataset.islandId][field.dataset.charterField] = field.value;
    updateExpeditionControls();
  }));
  $('#confirm-expedition').addEventListener('click', confirmExpedition);
}

function updateExpeditionControls() {
  const selected = Object.entries(expeditionDraft).filter(([id]) => id !== '__new');
  const actions = selected.filter(([, charter]) => charter.next_learning_action?.trim()).length;
  $('#charter-progress').textContent = `${actions}/${selected.length} next learning actions named.`;
  $('#confirm-expedition').disabled = !selected.length || actions !== selected.length;
}

async function confirmExpedition() {
  const charters = Object.entries(expeditionDraft).filter(([id]) => id !== '__new').map(([island_id, charter]) => ({island_id, ...charter}));
  try {
    $('#confirm-expedition').disabled = true;
    await post('/api/workspace/expeditions', {charters});
    expeditionDraft = {};
    await loadWorkspace();
  } catch (error) {
    $('#expedition-error').textContent = error.message;
    $('#confirm-expedition').disabled = false;
  }
}

function rememberedScoutName() {
  return localStorage.getItem('opportunity-atlas-scout-name') || '';
}

function openAddScoutingNote() {
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="add-scouting-note-form"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">PERSONAL SCOUTING NOTE</p><h2>Leave a signal for the team</h2><p class="dialog-intro">Capture an observation or idea before Expedition planning. This is yours; it does not appear on the Map until someone explicitly charts it as an Island.</p><label>Your name<input name="author" required maxlength="120" value="${escapeHtml(rememberedScoutName())}" placeholder="The person adding this note"></label><label>Short title<input name="title" required maxlength="120" placeholder="e.g. Patterns in escalations"></label><label>Your note<textarea name="body" required maxlength="2000" placeholder="What did you notice, wonder about, or want the team to explore?"></textarea></label><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Save Scouting note</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#add-scouting-note-form').addEventListener('submit', addScoutingNote);
}

function openTransferScoutingNote(noteId) {
  const note = currentMap(workspace).scoutingNotes.find(candidate => candidate.id === noteId);
  if (!note) return;
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="transfer-scouting-note-form" data-note-id="${escapeHtml(note.id)}"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><p class="eyebrow">CHART AN ISLAND FROM A NOTE</p><h2>Transfer “${escapeHtml(note.title)}”</h2><p class="dialog-intro">This explicit action creates an Island. The original personal note stays visible on it as provenance, separate from later team evidence.</p><label>Island name<input name="island-title" required maxlength="120" value="${escapeHtml(note.title)}"></label><p class="form-error" id="form-error" role="alert"></p><button class="primary" type="submit">Create and open Island</button></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  $('#transfer-scouting-note-form').addEventListener('submit', transferScoutingNote);
}

function scheduleMapNameSave() {
  clearTimeout(mapNameSaveTimer);
  $('#save-status').textContent = 'Saving…';
  mapNameSaveTimer = setTimeout(saveMapName, 700);
}

async function saveMapName() {
  clearTimeout(mapNameSaveTimer);
  const name = $('#map-name').value.trim();
  if (!name) return;
  try {
    await post('/api/workspace/map', {name});
    $('#save-status').textContent = 'Saved';
  } catch (error) {
    $('#save-status').textContent = `Not saved — ${error.message}`;
  }
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
  const chartRoom = chartRoomWithStartingPoint(island);
  const dialog = $('#island-dialog');
  dialog.innerHTML = `<form id="edit-island-form" data-island-id="${escapeHtml(island.id)}"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><header class="chart-room-heading"><p class="eyebrow">CHART ROOM · ISLAND DEEP DIVE</p><h2>${escapeHtml(island.title)}</h2><p>Develop a credible opportunity through team-authored material, not a mandatory business case.</p></header>${scoutingNoteProvenance(island)}<div class="chart-room-layout"><main class="chart-workspace"><label class="island-name-field">Island name<input name="title" required maxlength="120" value="${escapeHtml(island.title)}"></label><section class="chart-core"><div class="section-heading"><div><p class="eyebrow">CORE CHART · TEAM AUTHORED</p><h3>Opportunity hypothesis</h3></div><p>Enough to make this Island inspectable.</p></div><div class="chart-core-grid">${chartRoomCoreFields(chartRoom)}</div></section><section class="chart-evidence-grid">${chartEvidenceFields(chartRoom)}</section><section class="evaluation-section"><div class="section-heading"><div><p class="eyebrow">MAP COMPARISON VALUES · TEAM SETS THESE</p><h3>How this Island currently compares</h3></div><p>Visible, adjustable, and explained here—not an Expedition ranking.</p></div>${evaluationFields(island)}</section><section class="chart-details"><p class="eyebrow">DEEPER CHARTING · ONLY WHEN USEFUL</p>${chartRoomDetails(chartRoom)}</section></main>${aiSidecarMarkup()}</div><p class="form-error" id="form-error" role="alert"></p><footer class="chart-room-actions"><p>Only team-authored material is saved. AI guidance remains a prompt.</p><button class="primary" type="submit">Save Chart Room</button></footer></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  document.querySelectorAll('.ai-lens').forEach(button => button.addEventListener('click', () => showAiLens(button.dataset.lens)));
  $('#toggle-ai-sidecar').addEventListener('click', toggleAiSidecar);
  document.querySelectorAll('[name^="chart-"]').forEach(field => field.addEventListener('input', updateAiProgress));
  updateAiProgress();
  $('#edit-island-form').addEventListener('submit', saveIsland);
}

function scoutingNoteProvenance(island) {
  const note = island.scouting_note;
  if (!note) return '';
  return `<aside class="scouting-provenance"><p class="eyebrow">FROM A PERSONAL SCOUTING NOTE</p><h3>${escapeHtml(note.title)}</h3><blockquote>${escapeHtml(note.body)}</blockquote><p>Added by ${escapeHtml(note.author)}. This original note is retained as provenance; it is not team evidence. Record the team’s view below.</p></aside>`;
}

function aiSidecarMarkup() {
  return `<aside class="ai-compass" id="ai-sidecar" aria-label="Optional AI guidance"><header><p class="eyebrow">AI COMPASS · OPTIONAL</p><h3>Guidance while you chart</h3><p>Suggestions are questions, never team content. You choose what to write, save, or ignore.</p></header><ol class="ai-progress" id="ai-progress"><li data-step="workflow_problem">Frame the workflow</li><li data-step="evidence">Separate evidence from assumptions</li><li data-step="outcome">Name a possible outcome</li><li data-step="learning_action">Choose a next learning action</li></ol><div class="ai-guidance"><p class="eyebrow">CURRENT LENS</p><p id="ai-guidance">Start with the work as it is today. What decision is delayed, and who is affected?</p></div><div class="ai-lenses"><button type="button" class="secondary ai-lens" data-lens="workflow">Workflow lens</button><button type="button" class="secondary ai-lens" data-lens="evidence">Evidence lens</button><button type="button" class="secondary ai-lens" data-lens="values">Value lens</button></div><button type="button" class="text-button" id="toggle-ai-sidecar">Hide AI compass</button></aside>`;
}

function chartRoomWithStartingPoint(island) {
  const chartRoom = {...(island.chart_room || {})};
  if (!chartRoom.workflow_problem && !island.scouting_note) {
    // #25 direct creation predates the Chart Room.  Treat its team-authored
    // Map description as a starting point, never as AI or Scouting-note data.
    chartRoom.workflow_problem = island.detail || island.description || island.summary || '';
  }
  return chartRoom;
}

function chartRoomCoreFields(chartRoom) {
  return CHART_ROOM_FIELDS.filter(([, , , group]) => group.startsWith('core')).map(([id, label, hint, group]) => `<label class="chart-field ${group}">${escapeHtml(label)}<textarea name="chart-${id}" maxlength="2000" placeholder="Team-authored…">${escapeHtml(chartRoom[id] || '')}</textarea><small>${escapeHtml(hint)}</small></label>`).join('');
}

function chartEvidenceFields(chartRoom) {
  return CHART_ROOM_FIELDS.filter(([, , , group]) => group === 'evidence').map(([id, label, hint]) => `<section class="chart-evidence ${id === 'unknowns' ? 'chart-unknowns' : ''}"><label>${escapeHtml(label)}<textarea name="chart-${id}" maxlength="2000" placeholder="Team-authored…">${escapeHtml(chartRoom[id] || '')}</textarea><small>${escapeHtml(hint)}</small></label></section>`).join('');
}

function chartRoomDetails(chartRoom) {
  return CHART_ROOM_DETAILS.map(([id, label, summary, hint]) => `<details class="chart-detail" ${chartRoom[id] ? 'open' : ''}><summary>${escapeHtml(label)}<span>${escapeHtml(summary)}</span></summary><label class="sr-only" for="chart-${id}">${escapeHtml(label)}</label><textarea id="chart-${id}" name="chart-${id}" maxlength="2000" placeholder="${escapeHtml(hint)}">${escapeHtml(chartRoom[id] || '')}</textarea></details>`).join('');
}

function showAiLens(lens) {
  const guidance = {
    workflow: 'Which delayed decision would change if this Island worked, who makes it, and what would they do differently?',
    evidence: 'What observation, baseline, or accountable source would strengthen—or weaken—this opportunity hypothesis?',
    values: 'Why is each value high or low? Check the rationale; only the team can change a score.',
  };
  $('#ai-guidance').textContent = guidance[lens];
}

function updateAiProgress() {
  document.querySelectorAll('.ai-progress [data-step]').forEach(item => {
    const value = document.querySelector(`[name="chart-${item.dataset.step}"]`)?.value.trim();
    item.classList.toggle('complete', Boolean(value));
  });
}

function toggleAiSidecar() {
  const sidecar = $('#ai-sidecar');
  const hidden = sidecar.classList.toggle('collapsed');
  $('#toggle-ai-sidecar').textContent = hidden ? 'Show AI compass' : 'Hide AI compass';
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

async function addScoutingNote(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post('/api/workspace/scouting-notes', {title: values.title.trim(), body: values.body.trim(), author: values.author.trim()});
    localStorage.setItem('opportunity-atlas-scout-name', values.author.trim());
    $('#island-dialog').close();
    await loadWorkspace();
  } catch (error) {
    $('#form-error').textContent = error.message;
    form.querySelector('button[type="submit"]').disabled = false;
  }
}

async function transferScoutingNote(event) {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    const result = await post('/api/workspace/scouting-notes/transfer', {note_id: form.dataset.noteId, island_title: form.elements['island-title'].value.trim()});
    $('#island-dialog').close();
    await loadWorkspace();
    openIsland(result.opportunity.id);
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

function chartRoomFrom(form) {
  const result = {};
  [...CHART_ROOM_FIELDS, ...CHART_ROOM_DETAILS].forEach(([id]) => {
    result[id] = form.elements[`chart-${id}`].value.trim();
  });
  return result;
}

async function saveIsland(event) {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    form.querySelector('button[type="submit"]').disabled = true;
    await post(`/api/workspace/opportunities/${encodeURIComponent(form.dataset.islandId)}`, {title: form.elements.title.value.trim(), evaluation: evaluationFrom(form), chart_room: chartRoomFrom(form)});
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

document.querySelectorAll('[data-destination]').forEach(button => button.addEventListener('click', () => {
  activeDestination = button.dataset.destination;
  expeditionDraft = {};
  if (workspace) render(workspace);
}));

loadWorkspace();
