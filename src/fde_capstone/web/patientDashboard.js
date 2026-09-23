/**
 * Modular Centralized Patient Status Dashboard Component
 * Displays active CGT patients and their current orchestration phase.
 */
class PatientStatusDashboard {
  constructor(options = {}) {
    this.containerId = options.containerId || 'patient-dashboard-container';
    this.apiBase = options.apiBase || '/api';
    this.state = {
      patients: [],
      kpis: null,
      pagination: { page: 1, pageSize: 12, totalItems: 0, totalPages: 1 },
      filters: {
        search: '',
        phase: 'ALL',
        product: 'ALL',
        statusFilter: 'active', // 'active', 'all', 'completed'
        sortBy: 'patient_key',
        sortDir: 'asc',
      },
      viewMode: 'table', // 'table' | 'cards'
      selectedPatient: null,
      selectedPatientDetail: null,
      loading: false,
      detailLoading: false,
      error: null,
    };
    this.debounceTimer = null;
  }

  init() {
    this.container = document.getElementById(this.containerId);
    if (!this.container) {
      console.error(`PatientStatusDashboard container #${this.containerId} not found`);
      return;
    }
    this.renderSkeleton();
    this.fetchData();
  }

  async fetchData() {
    this.state.loading = true;
    this.updateLoadingState();

    const { search, phase, product, statusFilter, sortBy, sortDir } = this.state.filters;
    const { page, pageSize } = this.state.pagination;

    const params = new URLSearchParams({
      page: page.toString(),
      pageSize: pageSize.toString(),
      sortBy,
      sortDir,
      statusFilter,
    });
    if (search) params.set('search', search);
    if (phase && phase !== 'ALL') params.set('phase', phase);
    if (product && product !== 'ALL') params.set('product', product);

    try {
      const res = await fetch(`${this.apiBase}/patients?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const data = await res.json();

      this.state.patients = data.patients || [];
      this.state.kpis = data.kpis || null;
      this.state.pagination = {
        page: data.pagination.page,
        pageSize: data.pagination.page_size,
        totalItems: data.pagination.total_items,
        totalPages: data.pagination.total_pages,
      };
      this.state.error = null;
    } catch (err) {
      console.error('Failed to load patient dashboard data:', err);
      this.state.error = 'Failed to load patient records. Please check the API server.';
    } finally {
      this.state.loading = false;
      this.render();
    }
  }

  async openPatientDetail(patientKey) {
    this.state.selectedPatient = patientKey;
    this.state.detailLoading = true;
    this.renderModal();

    try {
      const res = await fetch(`${this.apiBase}/patients/${encodeURIComponent(patientKey)}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const detail = await res.json();
      this.state.selectedPatientDetail = detail;
    } catch (err) {
      console.error(`Failed to load details for ${patientKey}:`, err);
      this.state.selectedPatientDetail = null;
    } finally {
      this.state.detailLoading = false;
      this.renderModal();
    }
  }

  closePatientDetail() {
    this.state.selectedPatient = null;
    this.state.selectedPatientDetail = null;
    const modal = document.getElementById('patient-detail-modal');
    if (modal) modal.remove();
  }

  renderSkeleton() {
    this.container.innerHTML = `
      <div class="patient-dashboard-root">
        <div class="dashboard-head-section">
          <div>
            <span class="panel-kicker">CENTRALIZED ORCHESTRATION</span>
            <h2 class="dashboard-title">Active CGT Patient Status Dashboard</h2>
          </div>
          <p class="dashboard-desc">
            Cross-domain synthetic journey view (demonstrated on frozen synthetic data). Monitor physical journey positions, governing release readiness, chain of identity, and quality dispositions.
          </p>
        </div>
        <div class="dashboard-kpi-strip" id="dashboard-kpi-strip">
          <div class="kpi-card-loading">Loading telemetry...</div>
        </div>
        <div class="dashboard-toolbar-wrap" id="dashboard-toolbar-wrap"></div>
        <div class="dashboard-content-wrap" id="dashboard-content-wrap">
          <div class="dashboard-loading-placeholder">Loading active patient list...</div>
        </div>
      </div>
    `;
  }

  updateLoadingState() {
    const wrap = document.getElementById('dashboard-content-wrap');
    if (wrap && this.state.loading && this.state.patients.length === 0) {
      wrap.innerHTML = `<div class="dashboard-loading-placeholder"><span class="spinner"></span> Loading patient orchestration statuses...</div>`;
    }
  }

  render() {
    this.renderKPIs();
    this.renderToolbar();
    this.renderContent();
  }

  renderKPIs() {
    const strip = document.getElementById('dashboard-kpi-strip');
    if (!strip) return;

    if (!this.state.kpis) {
      strip.innerHTML = '';
      return;
    }

    const { kpis } = this.state;
    const counts = kpis.counts_by_phase || {};

    strip.innerHTML = `
      <div class="kpi-strip-meta" style="grid-column: 1 / -1;">
        <span class="kpi-strip-title">Global synthetic cohort KPIs (${kpis.total_patients} records)</span>
        <span class="kpi-strip-note">Deterministic cohort baseline across all clinical sites &amp; products</span>
      </div>
      <div class="kpi-card kpi-total" data-filter-phase="ALL">
        <span class="kpi-label">Active Therapies</span>
        <strong class="kpi-val">${kpis.active_patients}</strong>
        <span class="kpi-sub">of ${kpis.total_patients} total registered</span>
      </div>
      <div class="kpi-card kpi-mfg" data-filter-phase="IN_MANUFACTURING">
        <span class="kpi-label">In Manufacturing</span>
        <strong class="kpi-val">${kpis.in_manufacturing}</strong>
        <span class="kpi-sub">Cell expansion &amp; vector</span>
      </div>
      <div class="kpi-card kpi-qc" data-filter-phase="QC_PENDING">
        <span class="kpi-label">QC &amp; Release</span>
        <strong class="kpi-val">${(counts['QC_PENDING'] || 0)}</strong>
        <span class="kpi-sub">Assays &amp; batch review</span>
      </div>
      <div class="kpi-card kpi-hold ${kpis.qa_holds > 0 ? 'is-alert' : ''}" data-filter-phase="QA_HOLD">
        <span class="kpi-label">QA Exception Holds</span>
        <strong class="kpi-val">${kpis.qa_holds}</strong>
        <span class="kpi-sub">Active holds &amp; anomalies</span>
      </div>
      <div class="kpi-card kpi-transit" data-filter-phase="RETURN_TRANSIT">
        <span class="kpi-label">Return Transit</span>
        <strong class="kpi-val">${kpis.return_transit}</strong>
        <span class="kpi-sub">Cryo dry-shippers in route</span>
      </div>
      <div class="kpi-card kpi-ready" data-filter-phase="INFUSION_READY">
        <span class="kpi-label">Infusion Ready</span>
        <strong class="kpi-val">${kpis.infusion_ready}</strong>
        <span class="kpi-sub">Authorized for hospital site</span>
      </div>
    `;

    // Click KPI card to filter
    strip.querySelectorAll('.kpi-card').forEach((card) => {
      card.addEventListener('click', () => {
        const phase = card.dataset.filterPhase;
        this.state.filters.phase = phase;
        this.state.pagination.page = 1;
        this.fetchData();
      });
    });
  }

  renderToolbar() {
    const wrap = document.getElementById('dashboard-toolbar-wrap');
    if (!wrap) return;

    const { filters, viewMode, pagination } = this.state;

    const phases = [
      { id: 'ALL', label: 'All Phases' },
      { id: 'ENROLLED', label: 'Enrolled' },
      { id: 'APHERESIS_PENDING', label: 'Apheresis' },
      { id: 'COLLECTED', label: 'Collected' },
      { id: 'IN_MANUFACTURING', label: 'In Manufacturing' },
      { id: 'QC_PENDING', label: 'QC Pending' },
      { id: 'QA_HOLD', label: 'QA Hold' },
      { id: 'RETURN_TRANSIT', label: 'Return Transit' },
      { id: 'INFUSION_READY', label: 'Infusion Ready' },
      { id: 'INFUSED', label: 'Infused' },
    ];

    const products = ['ALL', 'CGT-A1', 'CGT-B2', 'CGT-C3'];

    wrap.innerHTML = `
      <div class="dashboard-toolbar">
        <div class="toolbar-search-box">
          <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
          <input
            type="search"
            id="dashboard-search-input"
            placeholder="Search by Patient Key (e.g. P-00001), Name, MRN, Center..."
            value="${escapeHtml(filters.search)}"
          />
          ${filters.search ? `<button type="button" class="btn-clear-search" id="btn-clear-search" title="Clear search">&times;</button>` : ''}
        </div>

        <div class="toolbar-filters-group">
          <div class="filter-select-wrap">
            <label for="filter-status-scope">Scope:</label>
            <select id="filter-status-scope">
              <option value="active" ${filters.statusFilter === 'active' ? 'selected' : ''}>Active Patients</option>
              <option value="all" ${filters.statusFilter === 'all' ? 'selected' : ''}>All Patients</option>
              <option value="completed" ${filters.statusFilter === 'completed' ? 'selected' : ''}>Completed (Infused)</option>
            </select>
          </div>

          <div class="filter-select-wrap">
            <label for="filter-phase-select">Phase:</label>
            <select id="filter-phase-select">
              ${phases.map(p => `<option value="${p.id}" ${filters.phase === p.id ? 'selected' : ''}>${p.label}</option>`).join('')}
            </select>
          </div>

          <div class="filter-select-wrap">
            <label for="filter-product-select">Product:</label>
            <select id="filter-product-select">
              ${products.map(pr => `<option value="${pr}" ${filters.product === pr ? 'selected' : ''}>${pr === 'ALL' ? 'All Products' : pr}</option>`).join('')}
            </select>
          </div>

          <div class="toolbar-view-toggle">
            <button
              type="button"
              class="view-toggle-btn ${viewMode === 'table' ? 'is-active' : ''}"
              id="view-toggle-table"
              title="Table View"
            >
              <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor">
                <path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm1 2v2h14V4H1zm0 3v2h14V7H1zm0 3v2h14v-2H1zm0 3v1a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1H1z"/>
              </svg>
              Table
            </button>
            <button
              type="button"
              class="view-toggle-btn ${viewMode === 'cards' ? 'is-active' : ''}"
              id="view-toggle-cards"
              title="Cards View"
            >
              <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor">
                <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zm8 0A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm-8 8A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm8 0A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3z"/>
              </svg>
              Cards
            </button>
          </div>
        </div>
      </div>
    `;

    // Bind Search Input with debounce
    const searchInput = document.getElementById('dashboard-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.state.filters.search = e.target.value;
          this.state.pagination.page = 1;
          this.fetchData();
        }, 280);
      });
    }

    const btnClearSearch = document.getElementById('btn-clear-search');
    if (btnClearSearch) {
      btnClearSearch.addEventListener('click', () => {
        this.state.filters.search = '';
        this.state.pagination.page = 1;
        this.fetchData();
      });
    }

    // Bind Filter Selects
    document.getElementById('filter-status-scope')?.addEventListener('change', (e) => {
      this.state.filters.statusFilter = e.target.value;
      this.state.pagination.page = 1;
      this.fetchData();
    });

    document.getElementById('filter-phase-select')?.addEventListener('change', (e) => {
      this.state.filters.phase = e.target.value;
      this.state.pagination.page = 1;
      this.fetchData();
    });

    document.getElementById('filter-product-select')?.addEventListener('change', (e) => {
      this.state.filters.product = e.target.value;
      this.state.pagination.page = 1;
      this.fetchData();
    });

    // View toggle
    document.getElementById('view-toggle-table')?.addEventListener('click', () => {
      if (this.state.viewMode !== 'table') {
        this.state.viewMode = 'table';
        this.render();
      }
    });

    document.getElementById('view-toggle-cards')?.addEventListener('click', () => {
      if (this.state.viewMode !== 'cards') {
        this.state.viewMode = 'cards';
        this.render();
      }
    });
  }

  renderContent() {
    const wrap = document.getElementById('dashboard-content-wrap');
    if (!wrap) return;

    if (this.state.error) {
      wrap.innerHTML = `
        <div class="dashboard-error-banner">
          <p>${escapeHtml(this.state.error)}</p>
          <button type="button" class="button button-secondary" id="btn-retry-dashboard">Retry</button>
        </div>
      `;
      document.getElementById('btn-retry-dashboard')?.addEventListener('click', () => this.fetchData());
      return;
    }

    const { patients, pagination, viewMode, filters } = this.state;

    if (patients.length === 0) {
      wrap.innerHTML = `
        <div class="dashboard-empty-state">
          <div class="empty-icon" aria-hidden="true">📋</div>
          <h3>No matching patients found</h3>
          <p>No active CGT patients match the selected search criteria or phase filters.</p>
          <button type="button" class="button button-secondary" id="btn-reset-filters">Reset all filters</button>
        </div>
      `;
      document.getElementById('btn-reset-filters')?.addEventListener('click', () => {
        this.state.filters = {
          search: '',
          phase: 'ALL',
          product: 'ALL',
          statusFilter: 'active',
          sortBy: 'patient_key',
          sortDir: 'asc',
        };
        this.state.pagination.page = 1;
        this.fetchData();
      });
      return;
    }

    let itemsHtml = '';
    if (viewMode === 'table') {
      itemsHtml = this.renderTableView(patients);
    } else {
      itemsHtml = this.renderCardsView(patients);
    }

    const paginationHtml = this.renderPagination(pagination);

    wrap.innerHTML = `
      <div class="dashboard-results-container">
        <div class="dashboard-results-meta">
          <span class="filter-population-banner">
            Current filtered population: <strong>${pagination.totalItems}</strong> patients (${filters.statusFilter === 'active' ? 'Active cohort' : filters.statusFilter === 'completed' ? 'Completed cohort' : 'All cohorts'}${filters.phase !== 'ALL' ? ` · Phase: ${escapeHtml(filters.phase)}` : ''})
          </span>
          <span class="text-sub">
            Showing <strong>${(pagination.page - 1) * pagination.pageSize + 1}–${Math.min(pagination.page * pagination.pageSize, pagination.totalItems)}</strong> of <strong>${pagination.totalItems}</strong> matching records (of 800 global cohort)
          </span>
        </div>
        ${itemsHtml}
        ${paginationHtml}
      </div>
    `;

    // Bind patient row/card clicks
    wrap.querySelectorAll('[data-patient-key]').forEach((el) => {
      el.addEventListener('click', (e) => {
        const target = e.target;
        if (target.closest('.action-button') || target.closest('button')) {
          return;
        }
        const key = el.dataset.patientKey;
        this.openPatientDetail(key);
      });
    });

    wrap.querySelectorAll('.btn-inspect-patient').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const key = btn.dataset.patientKey;
        this.openPatientDetail(key);
      });
    });

    // Bind pagination controls
    document.getElementById('page-prev')?.addEventListener('click', () => {
      if (pagination.page > 1) {
        this.state.pagination.page--;
        this.fetchData();
      }
    });

    document.getElementById('page-next')?.addEventListener('click', () => {
      if (pagination.page < pagination.totalPages) {
        this.state.pagination.page++;
        this.fetchData();
      }
    });
  }

  renderTableView(patients) {
    return `
      <div class="patient-table-wrap">
        <table class="patient-table" aria-label="Active CGT Patients">
          <thead>
            <tr>
              <th>Patient Key</th>
              <th>Name &amp; Center</th>
              <th>Product</th>
              <th>Journey Position</th>
              <th>Governing Readiness</th>
              <th>Pipeline Progress</th>
              <th>Batch / COI</th>
              <th class="th-actions">Actions</th>
            </tr>
          </thead>
          <tbody>
            ${patients.map((p) => {
              const readinessPill = this.getReadinessPill(p);
              const stepper = this.getMiniStepper(p.journey_status);
              return `
                <tr data-patient-key="${escapeHtml(p.patient_key)}" class="patient-row ${p.has_hold ? 'is-hold-row' : ''}">
                  <td class="td-key">
                    <span class="patient-id-badge">${escapeHtml(p.patient_key)}</span>
                    <small class="text-sub">${escapeHtml(p.mrn)}</small>
                  </td>
                  <td class="td-patient">
                    <strong>${escapeHtml(p.synthetic_name)}</strong>
                    <div class="patient-loc-sub">
                      <span class="country-pill">${escapeHtml(p.country)}</span>
                      <span>${escapeHtml(p.center_id)}</span>
                    </div>
                  </td>
                  <td class="td-product">
                    <span class="product-chip product-${escapeHtml(p.product_code.toLowerCase())}">${escapeHtml(p.product_code)}</span>
                  </td>
                  <td class="td-pos">
                    <span class="position-tag">📍 ${escapeHtml(p.journey_position_display)}</span>
                  </td>
                  <td class="td-readiness">
                    <div class="readiness-cell-wrap">
                      ${readinessPill}
                      ${this.getHoldBadge(p)}
                    </div>
                  </td>
                  <td class="td-stepper">
                    ${stepper}
                  </td>
                  <td class="td-batch">
                    ${p.batch_id ? `<code class="code-batch">${escapeHtml(p.batch_id)}</code>` : '<span class="text-sub">Slot pending</span>'}
                    ${p.coi_id ? `<small class="text-sub d-block">${escapeHtml(p.coi_id)}</small>` : ''}
                  </td>
                  <td class="td-actions">
                    <button type="button" class="btn-inspect-patient action-button" data-patient-key="${escapeHtml(p.patient_key)}" title="Inspect patient orchestration details">
                      View Details
                    </button>
                  </td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>
    `;
  }

  renderCardsView(patients) {
    return `
      <div class="patient-cards-grid">
        ${patients.map((p) => {
          const readinessPill = this.getReadinessPill(p);
          const stepper = this.getMiniStepper(p.journey_status);
          return `
            <div class="patient-status-card ${p.has_hold ? 'is-hold-card' : ''}" data-patient-key="${escapeHtml(p.patient_key)}">
              <div class="card-top-row">
                <div>
                  <span class="patient-id-badge">${escapeHtml(p.patient_key)}</span>
                  <span class="product-chip product-${escapeHtml(p.product_code.toLowerCase())}">${escapeHtml(p.product_code)}</span>
                </div>
              </div>

              <div class="card-name-row">
                <h4>${escapeHtml(p.synthetic_name)}</h4>
                <div class="patient-loc-sub">
                  <span class="country-pill">${escapeHtml(p.country)}</span>
                  <span>${escapeHtml(p.center_id)}</span>
                </div>
              </div>

              <div class="card-status-dimensions">
                <div class="card-dimension">
                  <span class="sub-label">Journey Position (Location)</span>
                  <span class="position-tag">📍 ${escapeHtml(p.journey_position_display)}</span>
                </div>
                <div class="card-dimension">
                  <span class="sub-label">Governing Readiness (Quality)</span>
                  <div class="readiness-cell-wrap">
                    ${readinessPill}
                    ${this.getHoldBadge(p)}
                  </div>
                </div>
              </div>

              <div class="card-stepper-block">
                ${stepper}
              </div>

              <div class="card-footer-facts">
                <div>
                  <small>Batch ID</small>
                  <strong>${p.batch_id ? escapeHtml(p.batch_id) : '—'}</strong>
                </div>
                <div>
                  <small>COI</small>
                  <strong>${p.coi_id ? escapeHtml(p.coi_id) : '—'}</strong>
                </div>
                <div>
                  <small>Deviations</small>
                  <strong class="${p.open_deviations_count > 0 ? 'text-warn' : ''}">${p.deviations_count}</strong>
                </div>
              </div>

              <div class="card-actions">
                <button type="button" class="btn-inspect-patient action-button button-secondary-sm" data-patient-key="${escapeHtml(p.patient_key)}">
                  Inspect Journey
                </button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  renderPagination(pagination) {
    if (!pagination || pagination.totalPages <= 1) return '';
    return `
      <div class="dashboard-pagination">
        <button
          type="button"
          class="page-btn"
          id="page-prev"
          ${pagination.page <= 1 ? 'disabled' : ''}
        >
          &larr; Previous
        </button>
        <span class="page-indicator">
          Page <strong>${pagination.page}</strong> of <strong>${pagination.totalPages}</strong>
        </span>
        <button
          type="button"
          class="page-btn"
          id="page-next"
          ${pagination.page >= pagination.totalPages ? 'disabled' : ''}
        >
          Next &rarr;
        </button>
      </div>
    `;
  }

  getHoldBadge(patient) {
    if (!patient.has_hold) return '';
    const isRetro = patient.governing_readiness_code === 'INVESTIGATION_POST_INFUSION';
    if (isRetro) {
      return `
        <span class="hold-blocking-badge is-investigation" title="Retrospective QA investigation active: discrepancy under audit">
          <span class="badge-icon">⚠</span>
          <span class="badge-label">QA HOLD</span>
          <span class="badge-tag">AUDIT</span>
        </span>
      `;
    }
    return `
      <span class="hold-blocking-badge is-blocking" title="Authoritative Quality Hold: Blocks batch release and clinical administration">
        <span class="badge-icon">⛔</span>
        <span class="badge-label">HOLD</span>
        <span class="badge-tag">BLOCKING</span>
      </span>
    `;
  }

  getReadinessPill(patient) {
    const code = patient.governing_readiness_code || '';
    const label = patient.governing_readiness_display || 'PENDING QUALITY RELEASE';
    const cls = patient.readiness_badge_class || 'readiness-pending';
    let icon = '⏳';
    if (code === 'BLOCKED_QA_HOLD') icon = '⛔';
    else if (code === 'INVESTIGATION_POST_INFUSION') icon = '⚠';
    else if (code === 'RELEASED_AUTHORIZED') icon = '✓';
    else if (code === 'COMPLETED_GOVERNED') icon = '✓';
    else if (code === 'ELIGIBILITY_VERIFIED') icon = '✓';
    return `<span class="readiness-pill ${cls}" title="${escapeHtml(label)}"><span class="pill-icon">${icon}</span> ${escapeHtml(label)}</span>`;
  }

  getInfusionAuthBadge(auth) {
    if (auth === 'AUTHORIZED') {
      return '<span class="status-code status-ok">✓ AUTHORIZED BY HUMAN QUALITY</span>';
    } else if (auth === 'PROHIBITED') {
      return '<span class="status-code text-warn">⛔ PROHIBITED (QA HOLD ACTIVE)</span>';
    } else if (auth === 'ADMINISTERED_UNDER_EXCEPTION') {
      return '<span class="status-code text-warn">⚠ EXCEPTION (INFUSED DESPITE QMS HOLD)</span>';
    } else if (auth === 'ADMINISTERED') {
      return '<span class="status-code status-ok">✓ ADMINISTERED</span>';
    }
    return '<span class="status-code">⏳ NOT READY</span>';
  }

  getPhaseBadge(patient) {
    let display = patient.phase_display;
    if (!display) {
      const status = patient.journey_status;
      const phaseNames = {
        ELIGIBLE: 'Eligible for Enrollment',
        ENROLLED: 'Enrolled & Verified',
        APHERESIS_PENDING: 'Apheresis Scheduled',
        COLLECTED: 'Collected & Outbound',
        IN_MANUFACTURING: 'In Manufacturing',
        QC_PENDING: 'QC & Sterility Testing',
        QA_HOLD: 'QA Exception Hold',
        RETURN_TRANSIT: 'Return Transit (Cryo)',
        INFUSION_READY: 'Infusion Ready',
        INFUSED: 'Infusion Completed',
      };
      display = phaseNames[status] || status;
    }

    // Safety rule: never show "Infusion Ready" if on hold
    if (patient.has_hold && patient.journey_status === 'INFUSION_READY') {
      display = 'Returned to Site (Quarantined)';
    }

    const badgeClass = patient.phase_badge_class || 'phase-default';

    return `
      <span class="phase-badge ${badgeClass}">
        <span class="phase-dot" aria-hidden="true"></span>
        ${escapeHtml(display)}
      </span>
    `;
  }

  getMiniStepper(status) {
    // 5 primary pipeline gates:
    // 1. Enrolled (ELIGIBLE, ENROLLED)
    // 2. Apheresis (APHERESIS_PENDING, COLLECTED)
    // 3. Manufacturing (IN_MANUFACTURING)
    // 4. QC & Release (QC_PENDING, QA_HOLD)
    // 5. Infusion (RETURN_TRANSIT, INFUSION_READY, INFUSED)
    const stageMap = {
      ELIGIBLE: 1,
      ENROLLED: 1,
      APHERESIS_PENDING: 2,
      COLLECTED: 2,
      IN_MANUFACTURING: 3,
      QC_PENDING: 4,
      QA_HOLD: 4,
      RETURN_TRANSIT: 5,
      INFUSION_READY: 5,
      INFUSED: 5,
    };

    const currentStage = stageMap[status] || 1;
    const isCompleted = status === 'INFUSED';

    const stages = [
      { label: 'Enroll', step: 1 },
      { label: 'Apheresis', step: 2 },
      { label: 'Mfg', step: 3 },
      { label: 'QC/QA', step: 4 },
      { label: 'Infusion', step: 5 },
    ];

    return `
      <div class="mini-stepper" aria-label="Phase progress ${currentStage} of 5">
        ${stages.map((st) => {
          const isDone = isCompleted || st.step < currentStage;
          const isCurrent = !isCompleted && st.step === currentStage;
          const statusClass = isDone ? 'step-done' : isCurrent ? 'step-current' : 'step-pending';
          return `
            <div class="mini-step ${statusClass}" title="${st.label}">
              <span class="step-indicator"></span>
              <span class="step-text">${st.label}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  renderModal() {
    let modal = document.getElementById('patient-detail-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'patient-detail-modal';
      modal.className = 'patient-modal-overlay';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      document.body.appendChild(modal);
    }

    if (!this.state.selectedPatient) {
      modal.remove();
      return;
    }

    if (this.state.detailLoading) {
      modal.innerHTML = `
        <div class="patient-modal-dialog">
          <div class="modal-header">
            <h3>Loading patient orchestration data...</h3>
            <button type="button" class="btn-close-modal" id="btn-modal-close" aria-label="Close dialog">&times;</button>
          </div>
          <div class="modal-body-loading">
            <span class="spinner"></span> Loading journey records for ${escapeHtml(this.state.selectedPatient)}...
          </div>
        </div>
      `;
      document.getElementById('btn-modal-close')?.addEventListener('click', () => this.closePatientDetail());
      return;
    }

    const detail = this.state.selectedPatientDetail;
    if (!detail || !detail.patient) {
      modal.innerHTML = `
        <div class="patient-modal-dialog">
          <div class="modal-header">
            <h3>Patient Not Found</h3>
            <button type="button" class="btn-close-modal" id="btn-modal-close" aria-label="Close dialog">&times;</button>
          </div>
          <div class="modal-body">
            <p>Could not load orchestration details for patient key <code>${escapeHtml(this.state.selectedPatient)}</code>.</p>
          </div>
        </div>
      `;
      document.getElementById('btn-modal-close')?.addEventListener('click', () => this.closePatientDetail());
      return;
    }

    const { patient, shipments, slots, qc_results, deviations } = detail;

    modal.innerHTML = `
      <div class="patient-modal-dialog">
        <div class="modal-header">
          <div>
            <div class="modal-eyebrow">
              <span>Patient Detail</span>
              <span class="product-chip product-${escapeHtml(patient.product_code.toLowerCase())}">${escapeHtml(patient.product_code)}</span>
              ${this.getReadinessPill(patient)}
              ${this.getHoldBadge(patient)}
            </div>
            <h2>${escapeHtml(patient.synthetic_name)} <small class="text-sub">(${escapeHtml(patient.patient_key)})</small></h2>
          </div>
          <button type="button" class="btn-close-modal" id="btn-modal-close" aria-label="Close dialog">&times;</button>
        </div>

        <div class="modal-body">
          <div class="modal-phase-banner">
            <div>
              <span class="sub-label">Physical Journey Position</span>
              <div class="position-tag" style="margin-top: 5px; font-size: 13px;">📍 ${escapeHtml(patient.journey_position_display)}</div>
            </div>
            <div>
              <span class="sub-label">Governing Release Readiness</span>
              <div style="margin-top: 5px;" class="readiness-cell-wrap">
                ${this.getReadinessPill(patient)}
                ${this.getHoldBadge(patient)}
              </div>
            </div>
            <div>
              <span class="sub-label">Infusion Authorization</span>
              <div style="margin-top: 5px;">${this.getInfusionAuthBadge(patient.infusion_authorization)}</div>
            </div>
            <div class="modal-stepper-wrap">
              ${this.getMiniStepper(patient.journey_status)}
            </div>
          </div>

          ${patient.has_hold && patient.hold_detail ? `
            <div class="modal-hold-alert-card ${patient.governing_readiness_code === 'INVESTIGATION_POST_INFUSION' ? 'is-retro-card' : ''}">
              <div class="hold-alert-header">
                <span class="hold-alert-title">
                  <span>${patient.governing_readiness_code === 'INVESTIGATION_POST_INFUSION' ? '⚠' : '⛔'}</span>
                  ${escapeHtml(patient.hold_detail.status)}: ${escapeHtml(patient.hold_detail.category)}
                </span>
                <span class="hold-warning-chip">GOVERNING QUALITY HOLD</span>
              </div>
              <div class="modal-section-grid" style="grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px;">
                <dl class="detail-kv">
                  <div><dt>Hold Status</dt><dd><strong>${escapeHtml(patient.hold_detail.status)}</strong></dd></div>
                  <div><dt>Opened At</dt><dd>${escapeHtml(patient.hold_detail.opened_at || '—')}</dd></div>
                  <div><dt>Closed At</dt><dd><strong>${escapeHtml(patient.hold_detail.closed_at || 'None — Currently Open')}</strong></dd></div>
                </dl>
                <dl class="detail-kv">
                  <div><dt>Blocks Release</dt><dd><span class="${patient.hold_detail.blocks_release ? 'text-warn' : ''}"><strong>${patient.hold_detail.blocks_release ? 'YES — Release Withheld' : 'NO'}</strong></span></dd></div>
                  <div><dt>Blocks Infusion</dt><dd><span class="${patient.hold_detail.blocks_infusion ? 'text-warn' : ''}"><strong>${patient.hold_detail.blocks_infusion ? 'YES — Administration Prohibited' : 'NO'}</strong></span></dd></div>
                  <div><dt>Disposition Ref</dt><dd><code>${escapeHtml(patient.hold_detail.quality_disposition_ref)}</code></dd></div>
                </dl>
              </div>
              <div style="background: rgba(0,0,0,0.03); padding: 10px 12px; border-radius: 6px; font-size: 12px; color: #7f1d1d; border-left: 3px solid #dc2626;">
                <strong>Clinical &amp; Regulatory Governance Note:</strong>
                <p style="margin: 4px 0 0; line-height: 1.5;">${escapeHtml(patient.hold_detail.clinical_risk_note)}</p>
              </div>
            </div>
          ` : ''}

          <div class="modal-section-grid">
            <div class="modal-card">
              <h4>Identity &amp; Chain of Custody</h4>
              <dl class="detail-kv">
                <div><dt>Patient Key</dt><dd><code>${escapeHtml(patient.patient_key)}</code></dd></div>
                <div><dt>MRN</dt><dd>${escapeHtml(patient.mrn)}</dd></div>
                <div><dt>CRM ID</dt><dd>${escapeHtml(patient.crm_patient_id)}</dd></div>
                <div><dt>Subject ID</dt><dd>${escapeHtml(patient.clinical_subject_id)}</dd></div>
                <div><dt>Chain of Identity (COI)</dt><dd><strong>${escapeHtml(patient.coi_id || 'Not generated')}</strong></dd></div>
                <div><dt>Treatment Center</dt><dd>${escapeHtml(patient.center_id)} (${escapeHtml(patient.country)})</dd></div>
                <div><dt>Date of Birth</dt><dd>${escapeHtml(patient.dob)}</dd></div>
                <div><dt>Enrolled Date</dt><dd>${escapeHtml(patient.enrolled_at || '—')}</dd></div>
              </dl>
            </div>

            <div class="modal-card">
              <h4>Manufacturing &amp; Quality Status</h4>
              <dl class="detail-kv">
                <div><dt>Batch Identifier</dt><dd><code>${escapeHtml(patient.batch_id || 'Pending')}</code></dd></div>
                <div><dt>MES Execution Status</dt><dd><strong>${escapeHtml(patient.mes_status || 'NOT_STARTED')}</strong></dd></div>
                <div><dt>QMS Release Authority</dt><dd><span class="status-code ${patient.qms_release_status === 'RELEASED' ? 'status-ok' : ''}">${escapeHtml(patient.qms_release_status || 'PENDING')}</span></dd></div>
                <div><dt>Collection ID</dt><dd>${escapeHtml(patient.collection_id || 'Pending')}</dd></div>
                <div><dt>Collection Time</dt><dd>${escapeHtml(patient.collection_time || '—')}</dd></div>
                <div><dt>Cell Viability</dt><dd><strong>${patient.viability_pct ? `${patient.viability_pct}%` : '—'}</strong></dd></div>
                <div><dt>Deviations / Exceptions</dt><dd><span class="${deviations.length > 0 ? 'text-warn' : ''}">${deviations.length} recorded (${patient.open_deviations_count} open)</span></dd></div>
              </dl>
            </div>
          </div>

          ${deviations.length > 0 ? `
            <div class="modal-subsection">
              <h4>Quality Deviations (${deviations.length})</h4>
              <div class="modal-table-wrap">
                <table class="sub-table">
                  <thead>
                    <tr>
                      <th>Deviation ID</th>
                      <th>Type</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Opened</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${deviations.map(d => `
                      <tr>
                        <td><code>${escapeHtml(d.deviation_id)}</code></td>
                        <td>${escapeHtml(d.type)}</td>
                        <td><span class="severity-pill severity-${escapeHtml(d.severity.toLowerCase())}">${escapeHtml(d.severity)}</span></td>
                        <td><strong>${escapeHtml(d.status)}</strong></td>
                        <td>${escapeHtml(d.opened_at || '—')}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          ` : ''}

          ${shipments.length > 0 ? `
            <div class="modal-subsection">
              <h4>Logistics &amp; Chain of Transit (${shipments.length})</h4>
              <div class="modal-table-wrap">
                <table class="sub-table">
                  <thead>
                    <tr>
                      <th>Shipment ID</th>
                      <th>Direction</th>
                      <th>Origin</th>
                      <th>Destination</th>
                      <th>Departed</th>
                      <th>Arrived</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${shipments.map(s => `
                      <tr>
                        <td><code>${escapeHtml(s.shipment_id)}</code></td>
                        <td><span class="direction-badge">${escapeHtml(s.direction)}</span></td>
                        <td>${escapeHtml(s.origin)}</td>
                        <td>${escapeHtml(s.destination)}</td>
                        <td>${escapeHtml(s.departed_at || 'In transit')}</td>
                        <td>${escapeHtml(s.arrived_at || 'Pending')}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          ` : ''}

          <div class="modal-footer-actions">
            <button type="button" class="button button-primary" id="btn-populate-disruption">
              Preview Disruption for this Patient &rarr;
            </button>
            <button type="button" class="button button-secondary" id="btn-modal-close-foot">
              Close
            </button>
          </div>
        </div>
      </div>
    `;

    // Modal listeners
    document.getElementById('btn-modal-close')?.addEventListener('click', () => this.closePatientDetail());
    document.getElementById('btn-modal-close-foot')?.addEventListener('click', () => this.closePatientDetail());
    modal.addEventListener('click', (e) => {
      if (e.target === modal) this.closePatientDetail();
    });

    document.getElementById('btn-populate-disruption')?.addEventListener('click', () => {
      const repInput = document.getElementById('representative-patient');
      if (repInput) {
        repInput.value = patient.patient_key;
        this.closePatientDetail();
        const disruptionSec = document.getElementById('disruptions');
        if (disruptionSec) {
          disruptionSec.scrollIntoView({ behavior: 'smooth' });
          document.getElementById('show-source-inject')?.focus();
        }
      }
    });
  }
}

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Export to global window so it can be instantiated anywhere
window.PatientStatusDashboard = PatientStatusDashboard;
