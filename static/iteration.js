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

function islandSummary(island, fallback) {
  const chart = island.chart_room || {};
  return chart.workflow_problem || island.detail || island.description || island.summary || fallback;
}

function render(payload) {
  workspace = payload;
  document.querySelectorAll('[data-destination]').forEach(button => {
    button.classList.toggle('is-active', button.dataset.destination === activeDestination);
  });
  if (activeDestination === 'map-changes') {
    $('#map-app').innerHTML = mapChangesMarkup(payload);
    $('#back-to-expedition').addEventListener('click', () => { activeDestination = 'expedition'; render(workspace); });
    return;
  }
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
    ${map.islands.length ? `<section class="map-board" aria-label="Island map">
      <div class="board-label"><span>THE SEA OF POSSIBILITIES</span><span>${map.islands.length} Island${map.islands.length === 1 ? '' : 's'} charted</span></div>
      <div class="waves waves--one"></div><div class="waves waves--two"></div>
      ${map.islands.map(islandMarkup).join('')}
      <button class="add-island" id="add-island"><span>+</span>Chart an Island</button>
      <p class="map-hint">Each Island holds its own visible values and the team's reasons for them.</p>
    </section>` : `<section class="map-empty" aria-label="Empty Opportunity Map"><p class="eyebrow">YOUR MAP IS OPEN</p><h2>Start with an opportunity your team could explore.</h2><p>Chart an Island directly, or add a personal Scouting note to bring into the team conversation later.</p><button class="primary" id="add-island">Chart the first Island</button><button class="text-button" id="open-map-help-empty">How does this work?</button></section>`}`;
  $('#add-island').addEventListener('click', openAddIsland);
  $('#add-scouting-note').addEventListener('click', openAddScoutingNote);
  $('#open-map-help-empty')?.addEventListener('click', openMapHelp);
  document.querySelectorAll('[data-island-id]').forEach(island => island.addEventListener('click', () => openIsland(island.dataset.islandId)));
  document.querySelectorAll('.transfer-note').forEach(button => button.addEventListener('click', () => openTransferScoutingNote(button.dataset.noteId)));
  document.querySelectorAll('.open-transferred-island').forEach(button => button.addEventListener('click', () => openIsland(button.dataset.islandId)));
  $('#map-name').addEventListener('input', scheduleMapNameSave);
  $('#map-name').addEventListener('blur', saveMapName);
}

function islandExpeditionContext(island) {
  const chart = island.chart_room || {};
  const hypothesis = islandSummary(island, 'This Island has not yet been described.');
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

function mapChangeCount(comparison) {
  if (!comparison?.has_changes) return 'The Map still matches this Expedition’s snapshot.';
  const parts = [
    comparison.added.length && `${comparison.added.length} added`,
    comparison.added_scouting_notes.length && `${comparison.added_scouting_notes.length} new note${comparison.added_scouting_notes.length === 1 ? '' : 's'}`,
    comparison.changed.length && `${comparison.changed.length} changed`,
    comparison.archived.length && `${comparison.archived.length} archived`,
  ].filter(Boolean);
  return `The Map has moved on: ${parts.join(', ')}.`;
}

function scoutingNoteChangeGroup(notes) {
  if (!notes.length) return '';
  return `<section class="map-change-group map-change-group--notes"><header><p class="eyebrow">SCOUTED SINCE CONFIRMATION</p><h2>${notes.length} personal note${notes.length === 1 ? '' : 's'}</h2></header><div class="map-change-list">${notes.map(note => `<article class="map-change-card"><p class="eyebrow">NOT YET AN ISLAND</p><h3>${escapeHtml(note.title)}</h3><p>${escapeHtml(note.body)}</p><p class="scouting-note-author">Added by ${escapeHtml(note.author)}</p></article>`).join('')}</div></section>`;
}

function strongerIslandNotices(notices, islands) {
  if (!notices.length) return '';
  const islandById = new Map(islands.map(island => [island.id, island]));
  return `<section class="map-value-notices" aria-label="Current Map value notices"><p class="eyebrow">CURRENT MAP VALUE NOTICE</p>${notices.map(notice => {
    const island = islandById.get(notice.island_id);
    const selected = islandById.get(notice.selected_island_id);
    return `<p><b>${escapeHtml(island?.title || 'An unselected Island')}</b> is now stronger on the current Map values (${notice.island_score.toFixed(1)}) than <b>${escapeHtml(selected?.title || 'a selected Island')}</b> (${notice.selected_island_score.toFixed(1)}). The Expedition is unchanged.</p>`;
  }).join('')}</section>`;
}

function mapChangeIslandSummary(island) {
  return islandSummary(island, 'No description recorded.');
}

function mapValueDeltas(valueChanges) {
  if (!valueChanges.length) return '<p class="map-value-deltas-empty">Evaluation values are unchanged.</p>';
  const labels = new Map(DIMENSIONS.map(([id, label]) => [id, label]));
  return `<section class="map-value-deltas" aria-label="Changed Island values"><p class="eyebrow">ISLAND VALUES</p><dl>${valueChanges.map(change => `<div><dt>${escapeHtml(labels.get(change.id) || change.id)}</dt><dd><span>Then ${change.before ?? 'not assessed'} / 5</span><b>→</b><span>Now ${change.after ?? 'not assessed'} / 5</span></dd></div>`).join('')}</dl></section>`;
}

function mapChangeGroup(label, changes, type) {
  if (!changes.length) return '';
  return `<section class="map-change-group map-change-group--${type}"><header><p class="eyebrow">${label}</p><h2>${changes.length} Island${changes.length === 1 ? '' : 's'}</h2></header><div class="map-change-list">${changes.map(change => {
    if (type === 'changed') {
      return `<article class="map-change-card"><p class="eyebrow">CHANGED ON THE LIVING MAP</p><h3>${escapeHtml(change.after.title)}</h3><p>${escapeHtml(mapChangeIslandSummary(change.after))}</p>${mapValueDeltas(change.value_changes || [])}<details><summary>See snapshot detail</summary><p><b>When confirmed:</b> ${escapeHtml(change.before.title)} — ${escapeHtml(mapChangeIslandSummary(change.before))}</p></details></article>`;
    }
    const island = change.island;
    const verb = type === 'added' ? 'CHARTED AFTER THIS EXPEDITION' : 'NO LONGER ON THE ACTIVE MAP';
    return `<article class="map-change-card"><p class="eyebrow">${verb}</p><h3>${escapeHtml(island.title)}</h3><p>${escapeHtml(mapChangeIslandSummary(island))}</p>${type === 'archived' ? `<p class="archive-reason"><b>Archived because:</b> ${escapeHtml(change.reason)}</p>` : ''}</article>`;
  }).join('')}</div></section>`;
}

function mapChangesMarkup(payload) {
  const expedition = payload.expedition;
  const comparison = payload.map_changes;
  const map = currentMap(payload);
  if (!expedition || !comparison) return '<p class="load-error">There is no confirmed Expedition to compare yet.</p>';
  return `<section class="map-changes-page"><button class="text-button" id="back-to-expedition">← Back to Expedition</button><header class="map-changes-heading"><p class="eyebrow">MAP CHANGES · READ ONLY</p><h1>The Map keeps moving.</h1><p>This is a calm comparison with the Map snapshot saved when this Expedition was confirmed. It does not freeze the Map or ask the team for a change note.</p></header><aside class="map-changes-note"><b>${escapeHtml(expedition.map_snapshot.name)} then · living Map now</b><span>${escapeHtml(mapChangeCount(comparison))}</span></aside>${strongerIslandNotices(comparison.newly_stronger_unselected, map.islands)}${comparison.has_changes ? `<div class="map-change-groups">${mapChangeGroup('ADDED ISLANDS SINCE CONFIRMATION', comparison.added, 'added')}${scoutingNoteChangeGroup(comparison.added_scouting_notes)}${mapChangeGroup('CHANGED SINCE CONFIRMATION', comparison.changed, 'changed')}${mapChangeGroup('ARCHIVED SINCE CONFIRMATION', comparison.archived, 'archived')}</div>` : '<section class="map-changes-empty"><h2>No Map changes yet</h2><p>The Map remains editable whenever the team discovers something new.</p></section>'}</section>`;
}

function activeExpeditionMarkup(expedition, islands, comparison) {
  const islandById = new Map(islands.map(island => [island.id, island]));
  return `<section class="expedition-active"><p class="eyebrow">ACTIVE EXPEDITION · MAP SNAPSHOT CAPTURED</p><h1>Island flags are flying.</h1><p class="expedition-intro">The living Map can continue to evolve. This Expedition keeps the Charters the team confirmed together.</p>
    <section class="active-charters">${expedition.charters.map(charter => {
      const island = islandById.get(charter.island_id) || expedition.map_snapshot.islands.find(item => item.id === charter.island_id) || {title: 'Archived Island'};
      return `<article class="active-charter"><p class="eyebrow">${escapeHtml(island.title)}</p><h3>${escapeHtml(charter.next_learning_action)}</h3>${charter.participants ? `<p><b>With:</b> ${escapeHtml(charter.participants)}</p>` : ''}${charter.intended_outcome ? `<p><b>For:</b> ${escapeHtml(charter.intended_outcome)}</p>` : ''}${charter.decision_evidence ? `<p><b>Evidence:</b> ${escapeHtml(charter.decision_evidence)}</p>` : ''}</article>`;
    }).join('')}</section>
    <aside class="snapshot-note"><div><b>Map snapshot saved</b><span>${escapeHtml(expedition.map_snapshot.name)} as confirmed. ${escapeHtml(mapChangeCount(comparison))}</span></div><button class="secondary" id="show-map-changes">Compare Map changes</button></aside>
    <button class="secondary" id="start-new-expedition">Start another Expedition</button>
  </section>`;
}

function renderExpedition(payload) {
  const map = currentMap(payload);
  const active = payload.expedition;
  if (active && !expeditionDraft.__new) {
    $('#map-app').innerHTML = activeExpeditionMarkup(active, map.islands, payload.map_changes);
    $('#start-new-expedition').addEventListener('click', () => { expeditionDraft = {__new: true}; render(workspace); });
    $('#show-map-changes').addEventListener('click', () => { activeDestination = 'map-changes'; render(workspace); });
    return;
  }
  const selectedIds = Object.keys(expeditionDraft).filter(id => id !== '__new');
  const selected = map.islands.filter(island => selectedIds.includes(island.id));
  const allActionsNamed = selected.length && selected.every(island => expeditionDraft[island.id].next_learning_action?.trim());
  $('#map-app').innerHTML = `<section class="expedition-page">
    <header class="expedition-heading"><p class="eyebrow">EXPEDITION · ISLAND FLAGS</p><h1>Give each Island its first leg.</h1><p>Choose prepared Islands from the living Map. Their Chart Room context and values stay inherited; an Island Charter only records what this Expedition will do next.</p></header>
    <section class="expedition-selector"><div><p class="eyebrow">ISLANDS ABOARD</p><h2>Choose the focus set</h2></div><div class="island-picks">${map.islands.map(island => `<label class="island-pick ${selectedIds.includes(island.id) ? 'island-pick--selected' : ''}"><input type="checkbox" data-select-island="${escapeHtml(island.id)}" ${selectedIds.includes(island.id) ? 'checked' : ''}><span><b>${escapeHtml(island.title)}</b><small>${escapeHtml(island.summary || island.description || 'Prepared Island')}</small></span></label>`).join('')}</div></section>
    ${selected.length ? `<aside class="expedition-ai-guide"><div><p class="eyebrow">AI COMPASS · OPTIONAL</p><h2>Check the focus set</h2><p>Ask AI to connect these Islands and their next learning actions to the North Star. It only advises; the team keeps the decision.</p></div><button type="button" class="secondary" id="check-expedition-guidance">Check with AI</button><div class="expedition-ai-response" id="expedition-ai-response" aria-live="polite"></div></aside>` : ''}
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
  $('#check-expedition-guidance')?.addEventListener('click', () => requestExpeditionGuidance(selected));
  $('#confirm-expedition').addEventListener('click', confirmExpedition);
}

async function requestExpeditionGuidance(selected) {
  const response = $('#expedition-ai-response');
  response.textContent = 'Checking the focus set…';
  const island = {title: selected.map(item => item.title).join(', '), chart_room: {workflow_problem: selected.map(item => islandSummary(item, '')).join(' ')}};
  try {
    const result = await post('/api/workspace/ai-guidance', {action: 'expedition', island});
    response.innerHTML = `<p class="eyebrow">${escapeHtml(result.source === 'local' ? 'LOCAL AI SUGGESTION' : 'AI SUGGESTION')}</p><ul>${result.suggestions.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul><small><b>Assumptions:</b> ${escapeHtml(result.assumptions.join(' '))}</small>`;
  } catch (error) { response.textContent = error.message; }
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
  dialog.innerHTML = `<form id="edit-island-form" data-island-id="${escapeHtml(island.id)}"><button type="button" class="dialog-close" id="close-dialog" aria-label="Close">×</button><header class="chart-room-heading"><p class="eyebrow">CHART ROOM · ISLAND DEEP DIVE</p><h2>${escapeHtml(island.title)}</h2><p>Develop a credible opportunity through team-authored material, not a mandatory business case.</p></header>${scoutingNoteProvenance(island)}<main class="chart-workspace"><label class="island-name-field">Island name<input name="title" required maxlength="120" value="${escapeHtml(island.title)}"></label><section class="chart-core"><div class="section-heading"><div><p class="eyebrow">CORE CHART · TEAM AUTHORED</p><h3>Opportunity hypothesis</h3></div><p>Enough to make this Island inspectable.</p></div><div class="chart-core-grid">${chartRoomCoreFields(chartRoom)}</div></section><section class="chart-evidence-grid">${chartEvidenceFields(chartRoom)}</section><section class="evaluation-section"><div class="section-heading"><div><p class="eyebrow">MAP COMPARISON VALUES · TEAM SETS THESE</p><h3>How this Island currently compares</h3></div><p>Visible, adjustable, and explained here—not an Expedition ranking.</p></div>${evaluationFields(island)}</section><section class="chart-details"><p class="eyebrow">DEEPER CHARTING · ONLY WHEN USEFUL</p>${chartRoomDetails(chartRoom)}</section></main><p class="form-error" id="form-error" role="alert"></p><footer class="chart-room-actions"><p>Only team-authored material is saved. AI guidance remains a prompt.</p><button class="primary" type="submit">Save Chart Room</button></footer></form>`;
  dialog.showModal();
  $('#close-dialog').addEventListener('click', () => dialog.close());
  document.querySelectorAll('[data-ai-action]').forEach(button => button.addEventListener('click', () => requestIslandGuidance(button.dataset.aiAction, island, button.closest('.chart-field, .chart-evidence'))));
  $('#edit-island-form').addEventListener('submit', saveIsland);
}

function scoutingNoteProvenance(island) {
  const note = island.scouting_note;
  if (!note) return '';
  return `<aside class="scouting-provenance"><p class="eyebrow">FROM A PERSONAL SCOUTING NOTE</p><h3>${escapeHtml(note.title)}</h3><blockquote>${escapeHtml(note.body)}</blockquote><p>Added by ${escapeHtml(note.author)}. This original note is retained as provenance; it is not team evidence. Record the team’s view below.</p></aside>`;
}

function aiSidecarMarkup() {
  return `<aside class="ai-compass" id="ai-sidecar" aria-label="Optional AI guidance"><header><p class="eyebrow">AI COMPASS · OPTIONAL</p><h3>Shape, explore, or challenge</h3><p>AI advice is separate from team content. It uses the visible Island and North Star; you choose what to write, save, or ignore.</p></header><div class="ai-actions"><button type="button" class="secondary" data-ai-action="formulate">Help formulate</button><button type="button" class="secondary" data-ai-action="alternatives">Explore alternatives</button><button type="button" class="secondary" data-ai-action="challenge">Challenge this Island</button></div><ol class="ai-progress" id="ai-progress"><li data-step="workflow_problem">Frame the workflow</li><li data-step="evidence">Separate evidence from assumptions</li><li data-step="outcome">Name a possible outcome</li><li data-step="learning_action">Choose a next learning action</li></ol><div class="ai-guidance"><p class="eyebrow">CURRENT LENS</p><p id="ai-guidance">Start with the work as it is today. What decision is delayed, and who is affected?</p></div><div class="ai-lenses"><button type="button" class="secondary ai-lens" data-lens="workflow">Workflow lens</button><button type="button" class="secondary ai-lens" data-lens="evidence">Evidence lens</button><button type="button" class="secondary ai-lens" data-lens="values">Value lens</button></div><button type="button" class="text-button" id="toggle-ai-sidecar">Hide AI compass</button></aside>`;
}

async function requestIslandGuidance(action, island, card) {
  const form = $('#edit-island-form');
  const currentIsland = {...island, title: form.elements.title.value.trim(), chart_room: chartRoomFrom(form)};
  const guidance = $('.ai-inline-response', card);
  guidance.textContent = 'Preparing transparent guidance…';
  try {
    const result = await post('/api/workspace/ai-guidance', {action, island: currentIsland});
    const draft = action === 'formulate' ? result.suggestions.join('\n') : result.suggestions.map(item => `• ${item}`).join('\n');
    const target = action === 'formulate' ? 'chart-workflow_problem' : action === 'alternatives' ? 'chart-ai_change' : 'chart-unknowns';
    const bullets = action === 'formulate' ? `<p class="ai-draft">${escapeHtml(draft)}</p><button type="button" class="text-button use-ai-draft" data-target="${target}">Use this instead</button>` : `<ul class="ai-suggestion-list">${result.suggestions.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
    guidance.innerHTML = `<p class="eyebrow">${escapeHtml(result.source === 'local' ? 'LOCAL AI SUGGESTION' : 'AI SUGGESTION')}</p>${bullets}<small><b>Assumptions:</b> ${escapeHtml(result.assumptions.join(' '))}</small>`;
    $('.use-ai-draft', guidance)?.addEventListener('click', event => { const targetField = document.querySelector(`[name="${event.currentTarget.dataset.target}"]`); if (targetField) { targetField.value = draft; targetField.dispatchEvent(new Event('input')); } });
  } catch (error) {
    guidance.textContent = error.message;
  }
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
  const actions = {workflow_problem: ['formulate', 'Help frame this'], ai_change: ['alternatives', 'Explore alternatives']};
  return CHART_ROOM_FIELDS.filter(([, , , group]) => group.startsWith('core')).map(([id, label, hint, group]) => `<label class="chart-field ${group}">${escapeHtml(label)}<textarea name="chart-${id}" maxlength="2000" placeholder="Team-authored…">${escapeHtml(chartRoom[id] || '')}</textarea><small>${escapeHtml(hint)}</small>${actions[id] ? `<button type="button" class="text-button ai-inline-action" data-ai-action="${actions[id][0]}">${actions[id][1]} with AI</button><div class="ai-inline-response" aria-live="polite"></div>` : ''}</label>`).join('');
}

function chartEvidenceFields(chartRoom) {
  return CHART_ROOM_FIELDS.filter(([, , , group]) => group === 'evidence').map(([id, label, hint]) => `<section class="chart-evidence ${id === 'unknowns' ? 'chart-unknowns' : ''}"><label>${escapeHtml(label)}<textarea name="chart-${id}" maxlength="2000" placeholder="Team-authored…">${escapeHtml(chartRoom[id] || '')}</textarea><small>${escapeHtml(hint)}</small>${id === 'unknowns' ? '<button type="button" class="text-button ai-inline-action" data-ai-action="challenge">Challenge this Island with AI</button><div class="ai-inline-response" aria-live="polite"></div>' : ''}</label></section>`).join('');
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

function openMapHelp() { $('#map-help-dialog').showModal(); }
$('#open-map-help')?.addEventListener('click', openMapHelp);
$('#close-map-help')?.addEventListener('click', () => $('#map-help-dialog').close());

loadWorkspace();
