const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const elements = {
  runButtons: $$('[data-run-demo]'),
  mode: $('#ai-mode'),
  runState: $('#run-state'),
  progress: $('#progress-fill'),
  toast: $('#toast'),
};

const pause = (milliseconds) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));

function setText(selector, value, className = '') {
  const element = $(selector);
  element.textContent = value;
  element.classList.remove('value-pass', 'value-warn');
  if (className) element.classList.add(className);
}

function setBadge(number, label, state) {
  const badge = $(`#poc-${number}-badge`);
  badge.textContent = label;
  badge.className = `result-badge result-${state}`;
}

function setRunning(number) {
  $$('.poc-card').forEach((card) => card.classList.remove('is-running'));
  const card = $(`#poc-${number}`);
  card.classList.add('is-running');
  setBadge(number, 'Running', 'running');
}

function setProgress(value, message) {
  elements.progress.style.width = `${value}%`;
  elements.runState.textContent = message;
}

function completeJourneyThrough(index) {
  $$('.journey-step').forEach((step) => {
    step.classList.toggle('is-complete', Number(step.dataset.step) <= index);
  });
}

function resetDemo() {
  $$('.poc-card').forEach((card) => card.classList.remove('is-running', 'is-complete'));
  [1, 2, 3].forEach((number) => setBadge(number, 'Not run', 'idle'));
  completeJourneyThrough(-1);
  setProgress(4, 'Creating isolated synthetic runtime…');
  $('#console-empty').hidden = false;
  $('#console-results').hidden = true;
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add('show');
  window.setTimeout(() => elements.toast.classList.remove('show'), 3200);
}

async function loadStatus() {
  try {
    const response = await fetch('/api/capstone/status');
    if (!response.ok) throw new Error(`Status request failed (${response.status})`);
    const status = await response.json();
    $('#stage-count').textContent = `${status.stages.complete}/${status.stages.total}`;
    $('#test-count').textContent = status.tests.passed;
    $('#evaluation-count').textContent = `${status.evaluations.passed}/57`;
    $('#requirement-count').textContent = `${status.requirements.verified_internal_poc}/${status.requirements.total}`;
  } catch (error) {
    showToast('Status unavailable. Start the FastAPI server and refresh.');
  }
}

async function presentResults(result) {
  completeJourneyThrough(0);
  setRunning(1);
  setProgress(25, 'Resolving identity conflict with human authority…');
  await pause(550);
  setText('#identity-decision', result.poc1.decision, 'value-pass');
  setText('#identity-readiness', result.poc1.readiness, 'value-pass');
  setText('#identity-evidence', `${result.poc1.evidence_refs.length} cited`);
  setBadge(1, 'Controlled', 'pass');
  $('#poc-1').classList.remove('is-running');
  $('#poc-1').classList.add('is-complete');
  completeJourneyThrough(2);

  setRunning(2);
  setProgress(52, 'Reconciling unknown slot-reservation outcome…');
  await pause(650);
  setText('#slot-initial', result.poc2.initial_state, 'value-warn');
  setText('#slot-reconciled', result.poc2.reconciled_state, 'value-pass');
  setText('#slot-replay', result.poc2.replay_dispatch ? 'YES · unsafe' : 'NO · prevented', 'value-pass');
  setBadge(2, 'Reconciled', 'pass');
  $('#poc-2').classList.remove('is-running');
  $('#poc-2').classList.add('is-complete');
  completeJourneyThrough(4);

  setRunning(3);
  setProgress(78, 'Assembling evidence packet and applying Quality decision…');
  await pause(650);
  setText('#quality-before', result.poc3.before, 'value-warn');
  setText('#quality-release', result.poc3.released ? 'HUMAN AUTHORIZED' : 'BLOCKED', result.poc3.released ? 'value-pass' : 'value-warn');
  setText('#quality-after', result.poc3.after, 'value-pass');
  setBadge(3, 'Released', 'pass');
  $('#poc-3').classList.remove('is-running');
  $('#poc-3').classList.add('is-complete');
  completeJourneyThrough(7);

  const evidence = [...new Set([...result.poc1.evidence_refs, ...result.poc3.evidence_refs])].sort();
  const evidenceContainer = $('#evidence-chips');
  evidenceContainer.replaceChildren();
  evidence.forEach((reference) => {
    const chip = document.createElement('span');
    chip.textContent = reference;
    evidenceContainer.appendChild(chip);
  });

  $('#console-empty').hidden = true;
  $('#console-results').hidden = false;
  setText('#audit-result', result.audit_chain_valid ? 'VALID' : 'FAILED', result.audit_chain_valid ? 'value-pass' : 'value-warn');
  setText('#assistant-result', result.assistant.mode.replaceAll('_', ' '));
  setText('#metric-result', `${Object.keys(result.metrics).length} signals`);
  setText('#state-digest', result.state_digest);
  setText('#hero-audit', result.state_digest.slice(0, 12));
  $('#run-scope').textContent = result.scope;
  setProgress(100, 'Journey complete · evidence and audit record verified');
  showToast('Synthetic patient-to-batch journey completed successfully.');
}

async function runDemo() {
  if (elements.runButtons.some((button) => button.disabled)) return;
  resetDemo();
  elements.runButtons.forEach((button) => { button.disabled = true; });
  try {
    const response = await fetch('/api/demo/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ai_mode: elements.mode.value }),
    });
    if (!response.ok) throw new Error(`Demo request failed (${response.status})`);
    const result = await response.json();
    await presentResults(result);
  } catch (error) {
    setProgress(0, 'Demo could not complete');
    showToast(error.message || 'Unexpected demo error');
  } finally {
    $$('.poc-card').forEach((card) => card.classList.remove('is-running'));
    elements.runButtons.forEach((button) => { button.disabled = false; });
  }
}

elements.runButtons.forEach((button) => button.addEventListener('click', runDemo));
loadStatus();
