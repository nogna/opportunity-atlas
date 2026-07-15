const DISPLAY_NAME_KEY = 'opportunity-atlas.display-name';
let autoSaveTimer;

async function post(path, body) {
  const response = await fetch(path, {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error((await response.json()).error || 'Could not save the Workspace.');
  return response.json();
}

function displayName() {
  return localStorage.getItem(DISPLAY_NAME_KEY) || '';
}

function rankingMarkup(ranking) {
  return `<h3>Current ranking</h3><ol>${ranking.map(entry => entry.state === 'ranked'
    ? `<li>#${entry.rank} ${entry.title} <span class="muted">${entry.score.toFixed(2)} / 5</span></li>`
    : `<li>${entry.title} <span class="muted">Unranked — missing ${entry.missing_dimension_ids.join(', ')}</span></li>`).join('')}</ol>`;
}

function carryForwardMarkup(current) {
  if (!current.inherited_opportunities || !Object.keys(current.inherited_opportunities).length) return '';
  const archived = new Set((current.archive_decisions || []).filter(item => !item.restored_at).map(item => item.opportunity_id));
  return `<section><h3>Carry-forward review</h3><p class="muted">Review inherited opportunities before changing this draft.</p><ul>${Object.entries(current.inherited_opportunities).map(([id, inherited]) => {
    const item = inherited.opportunity;
    const archive = (current.archive_decisions || []).find(decision => decision.opportunity_id === id && !decision.restored_at);
    return `<li><strong>${item.title}</strong>${item.not_pursuing_decision ? ' <span class="muted">Previously not pursuing</span>' : ''}
      ${archived.has(id) ? `<span class="muted"> Archived: ${archive.reason}</span> <button data-restore="${id}">Restore</button>` : `<button data-archive="${id}">Archive</button>`}</li>`;
  }).join('')}</ul></section>`;
}

async function loadIterationView() {
  const response = await fetch('/api/workspace');
  const workspace = await response.json();
  const current = workspace.iterations.at(-1);
  const currentIsSet = Boolean(current.next_opportunity_decision);
  if (!currentIsSet && !displayName()) {
    const name = prompt('Choose the name your team will see while you edit.');
    if (name?.trim()) localStorage.setItem(DISPLAY_NAME_KEY, name.trim());
  }
  const currentElement = document.querySelector('#current-iteration');
  const historyElement = document.querySelector('#iteration-history');

  currentElement.innerHTML = `
    <p class="eyebrow">CURRENT ${currentIsSet ? 'SET ITERATION' : 'DRAFT ITERATION'}</p>
    <h2>${current.custom_name || `Iteration ${current.number}`}</h2>
    ${currentIsSet ? `<p>${current.decision_frame.goal}</p>` : `<label>Decision Frame goal <textarea id="decision-frame-goal" data-field-id="decision-frame.goal">${current.decision_frame.goal}</textarea><small id="field-status" class="muted">Saved automatically after you pause.</small></label>`}
    <p class="muted">${currentIsSet ? 'Read-only decision record.' : 'Editable exploration workspace.'}</p>
    <h3>Opportunities</h3><ul>${current.opportunities.map(item => `<li>${item.title}</li>`).join('')}</ul>
    ${rankingMarkup(workspace.ranking)}
    ${currentIsSet ? '' : `<section><h3>AI review suggestions</h3><p class="muted">Suggestions are drafts only; they never change this Workspace until you choose an action.</p><button id="ai-suggestions">Generate review suggestions</button><div id="ai-suggestion-results"></div></section>`}
    ${currentIsSet ? `<form id="next-iteration-form"><h3>Start a new Iteration</h3><label>What changed <textarea name="what_changed" required></textarea></label><label>Name (optional) <input name="custom_name"></label><button type="submit">Start draft</button></form>` : `${carryForwardMarkup(current)}<form id="set-iteration-form">
      <h3>Set this Iteration</h3>
      <label>Next Opportunity <select name="next_opportunity_id">${current.shortlist.map(id => `<option value="${id}">${current.opportunities.find(item => item.id === id)?.title || id}</option>`).join('')}</select></label>
      <label>Your name <input name="recorded_by" value="${displayName()}" required></label>
      <label>Decision rationale <textarea name="rationale" required></textarea></label>
      <label>Unranked override rationale <textarea name="unranked_override_rationale" placeholder="Required only if you choose an unranked opportunity."></textarea></label>
      <button type="submit">Set Iteration</button>
    </form>`}`;

  const history = workspace.iterations.slice(0, -1).reverse();
  historyElement.innerHTML = history.length
    ? history.map(item => `<article><h3>${item.custom_name || `Iteration ${item.number}`}</h3><p>${item.what_changed || 'Initial decision'}</p><p class="muted">From Iteration ${item.source_iteration_number || 'initial'} · ${item.created_at || 'creation time unavailable'}</p><p class="muted">Set decision: ${item.next_opportunity_decision.opportunity_id}</p></article>`).join('')
    : '<p class="muted">No completed Iterations yet.</p>';

  document.querySelector('#set-iteration-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    const values = Object.fromEntries(new FormData(event.currentTarget));
    localStorage.setItem(DISPLAY_NAME_KEY, values.recorded_by.trim());
    await post('/api/workspace/decision', values); loadIterationView();
  });
  document.querySelector('#next-iteration-form')?.addEventListener('submit', async event => {
    event.preventDefault(); await post('/api/workspace/next-iteration', Object.fromEntries(new FormData(event.currentTarget))); loadIterationView();
  });
  document.querySelectorAll('[data-archive]').forEach(button => button.addEventListener('click', async () => {
    const reason = prompt('Why is this opportunity no longer relevant to this iteration?');
    if (reason) { await post('/api/workspace/archive', {opportunity_id: button.dataset.archive, reason}); loadIterationView(); }
  }));
  document.querySelectorAll('[data-restore]').forEach(button => button.addEventListener('click', async () => {
    await post('/api/workspace/restore', {opportunity_id: button.dataset.restore}); loadIterationView();
  }));
  document.querySelector('#ai-suggestions')?.addEventListener('click', async () => {
    const suggestions = await post('/api/ai/suggestions', {});
    document.querySelector('#ai-suggestion-results').innerHTML = `<p><strong>Draft candidate:</strong> ${suggestions.candidates[0].title}<br><span class="muted">Assumptions: ${suggestions.candidates[0].assumptions.join(' ')} Uncertainties: ${suggestions.candidates[0].uncertainties.join(' ')}</span><br><button id="accept-ai-candidate">Add this candidate</button></p><p><strong>Suggested weights</strong> <button id="apply-ai-weights" title="${suggestions.weight_suggestion.map(item => item.rationale).join(' ')}">Apply proposed weights</button></p><p class="muted">${suggestions.trade_offs}</p>`;
    document.querySelector('#accept-ai-candidate').addEventListener('click', async () => { await post('/api/workspace/opportunities', {opportunity: suggestions.candidates[0]}); loadIterationView(); });
    document.querySelector('#apply-ai-weights').addEventListener('click', async () => { await post('/api/workspace/apply-suggested-weights', {weights: suggestions.weight_suggestion}); loadIterationView(); });
  });
  bindDecisionFrameEditor();
}

function bindDecisionFrameEditor() {
  const field = document.querySelector('#decision-frame-goal');
  if (!field) return;
  const status = document.querySelector('#field-status');
  field.addEventListener('focus', async () => {
    const name = displayName() || prompt('Choose the name your team will see while you edit.');
    if (!name) return field.blur();
    localStorage.setItem(DISPLAY_NAME_KEY, name.trim());
    try { await post('/api/collaboration/start-editing', {field_id: field.dataset.fieldId, display_name: name}); status.textContent = `Editing as ${name}.`; }
    catch (error) { status.textContent = error.message; field.blur(); }
  });
  field.addEventListener('input', async () => {
    const name = displayName();
    if (!name) return;
    try {
      await post('/api/collaboration/input', {field_id: field.dataset.fieldId, display_name: name, value: field.value});
      clearTimeout(autoSaveTimer);
      autoSaveTimer = setTimeout(async () => {
        const result = await post('/api/collaboration/autosave', {});
        status.textContent = result.saved_fields.length ? 'Saved automatically.' : 'Waiting to save…';
      }, 800);
    } catch (error) { status.textContent = error.message; }
  });
}

loadIterationView();
