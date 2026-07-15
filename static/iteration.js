async function loadIterationView() {
  const response = await fetch('/api/workspace');
  const workspace = await response.json();
  const current = workspace.iterations.at(-1);
  const currentIsSet = Boolean(current.next_opportunity_decision);
  const currentElement = document.querySelector('#current-iteration');
  const historyElement = document.querySelector('#iteration-history');

  currentElement.innerHTML = `
    <p class="eyebrow">CURRENT ${currentIsSet ? 'SET ITERATION' : 'DRAFT ITERATION'}</p>
    <h2>${current.custom_name || `Iteration ${current.number}`}</h2>
    <p>${current.decision_frame.goal}</p>
    <p class="muted">${currentIsSet ? 'Read-only decision record.' : 'Editable exploration workspace.'}</p>
    <h3>Opportunities</h3>
    <ul>${current.opportunities.map(item => `<li>${item.title}</li>`).join('')}</ul>
    ${currentIsSet ? '' : `<form id="set-iteration-form">
      <h3>Set this Iteration</h3>
      <label>Next Opportunity <select name="next_opportunity_id">${current.shortlist.map(id => `<option value="${id}">${current.opportunities.find(item => item.id === id).title}</option>`).join('')}</select></label>
      <label>Your name <input name="recorded_by" required></label>
      <label>Decision rationale <textarea name="rationale" required></textarea></label>
      <button type="submit">Set Iteration</button>
    </form>`}`;

  const history = workspace.iterations.slice(0, -1).reverse();
  historyElement.innerHTML = history.length
    ? history.map(item => `<article><h3>${item.custom_name || `Iteration ${item.number}`}</h3><p>${item.what_changed || 'Initial decision'}</p><p class="muted">From Iteration ${item.source_iteration_number || 'initial'} · ${item.created_at || 'creation time unavailable'}</p><p class="muted">Set decision: ${item.next_opportunity_decision.opportunity_id}</p></article>`).join('')
    : '<p class="muted">No completed Iterations yet.</p>';

  document.querySelector('#set-iteration-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    const values = Object.fromEntries(new FormData(event.currentTarget));
    const response = await fetch('/api/workspace/decision', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(values),
    });
    if (response.ok) loadIterationView();
  });
}

loadIterationView();
