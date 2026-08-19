"use strict";

const Audita = {
  files: [],
  report: null,
  opinion: null,
  chart: null,
  opinionTab: "resumo",
  lastFocused: null,
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const reduceMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const asNumber = (value) => Number.parseFloat(value || 0);
const brl = (value, compact = false) => new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
  notation: compact ? "compact" : "standard",
  maximumFractionDigits: compact ? 1 : 2,
}).format(asNumber(value));

function toast(message, error = false) {
  const node = $("#toast");
  node.textContent = message;
  node.classList.toggle("error", error);
  node.hidden = false;
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => { node.hidden = true; }, 4200);
}

async function api(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = "Não foi possível concluir a operação.";
    try {
      const body = await response.json();
      message = body.detail || body.error || message;
    } catch (_) { /* resposta não JSON */ }
    throw new Error(typeof message === "string" ? message : "Revise os dados enviados.");
  }
  return response;
}

function setLoading(active, message = "Lendo documentos...") {
  const progress = $("#progress");
  const fill = $("#progressFill");
  $("#auditButton").disabled = active;
  $("#demoButton").disabled = active;
  progress.hidden = !active;
  if (!active) return;
  $("#progressText").textContent = message;
  fill.style.width = "18%";
  window.setTimeout(() => { if (!progress.hidden) fill.style.width = "62%"; }, 220);
  window.setTimeout(() => { if (!progress.hidden) fill.style.width = "88%"; }, 650);
}

function animateMoney(target) {
  const node = $("#potentialAmount");
  if (reduceMotion()) {
    node.textContent = brl(target);
    return;
  }
  const started = performance.now();
  const duration = 1050;
  const frame = (now) => {
    const progress = Math.min((now - started) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4);
    node.textContent = brl(target * eased);
    if (progress < 1) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

function celebrate() {
  if (reduceMotion() || typeof window.confetti !== "function") return;
  window.confetti({ particleCount: 95, spread: 72, origin: { y: 0.66 }, colors: ["#22c55e", "#818cf8", "#f8fafc"] });
}

function renderResults(payload) {
  Audita.report = payload.report;
  Audita.opinion = payload.opinion;
  const report = Audita.report;
  $("#results").hidden = false;
  $("#simulationBadge").style.display = report.synthetic_simulation ? "inline-flex" : "none";
  animateMoney(asNumber(report.estimated_overpayment));
  $("#kpiInvoices").textContent = report.invoice_count;
  $("#kpiRevenue").textContent = brl(report.audited_revenue, true);
  $("#kpiConfirmed").textContent = brl(report.confirmed_monophase_revenue, true);
  $("#kpiRate").textContent = `${(asNumber(report.rate.effective_pis_cofins_rate) * 100).toLocaleString("pt-BR", { maximumFractionDigits: 4 })}%`;
  $("#formulaText").textContent = "Receita confirmada × alíquota efetiva PIS/Cofins";
  $("#rateText").textContent = `Anexo I · faixa ${report.rate.band} · DAS efetivo ${(asNumber(report.rate.effective_das_rate) * 100).toLocaleString("pt-BR", { maximumFractionDigits: 3 })}% × 15,5%`;
  $("#opinionSource").textContent = payload.opinion.source === "openai" ? "OpenAI + regras" : "Motor local";
  renderOpinion();
  renderEvidence();
  $("#results").scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "start" });
  if (asNumber(report.estimated_overpayment) > 0) celebrate();
}

async function runDemo() {
  setLoading(true, "Carregando cenário sintético da oficina...");
  try {
    const response = await api("/api/audit/demo-oficina", { method: "POST" });
    $("#progressFill").style.width = "100%";
    renderResults(await response.json());
    toast("Simulação concluída. Confira premissas e evidências.");
  } catch (error) {
    toast(error.message, true);
  } finally {
    setLoading(false);
  }
}

async function runUpload(event) {
  event.preventDefault();
  if (!Audita.files.length) {
    toast("Selecione ao menos um XML ou ZIP.", true);
    $("#dropzone").focus();
    return;
  }
  const form = new FormData();
  Audita.files.forEach((file) => form.append("files", file));
  form.append("rbt12", $("#rbt12").value);
  form.append("period", $("#period").value);
  form.append("pgdas_segregated", String($("#pgdasSegregated").checked));
  setLoading(true, `Auditando ${Audita.files.length} arquivo(s)...`);
  try {
    const response = await api("/api/audit/upload", { method: "POST", body: form });
    $("#progressFill").style.width = "100%";
    renderResults(await response.json());
    toast("Auditoria concluída. O resultado ainda requer validação profissional.");
  } catch (error) {
    toast(error.message, true);
  } finally {
    setLoading(false);
  }
}

function updateFiles(fileList) {
  Audita.files = [...fileList].filter((file) => /\.(xml|zip)$/i.test(file.name));
  const badge = $("#fileBadge");
  if (!Audita.files.length) {
    badge.textContent = "NF-e/NFC-e 4.00 · máximo 25 MB";
    return;
  }
  const bytes = Audita.files.reduce((total, file) => total + file.size, 0);
  badge.textContent = `${Audita.files.length} arquivo(s) · ${(bytes / 1024 / 1024).toLocaleString("pt-BR", { maximumFractionDigits: 2 })} MB`;
}

function renderOpinion() {
  if (!Audita.opinion) return;
  const value = Audita.opinion[Audita.opinionTab];
  const panel = $("#opinionPanel");
  if (Array.isArray(value)) {
    panel.replaceChildren(Object.assign(document.createElement("ul"), {}));
    value.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      panel.firstElementChild.append(li);
    });
  } else {
    const paragraph = document.createElement("p");
    paragraph.textContent = value || "Sem leitura disponível.";
    panel.replaceChildren(paragraph);
  }
}

function renderEvidence() {
  if (!Audita.report) return;
  renderChart();
  renderFindings();
}

function renderChart() {
  const totals = Audita.report.findings.reduce((segments, finding) => {
    const amount = asNumber(finding.estimated_overpayment);
    if (amount > 0) segments[finding.segment] = (segments[finding.segment] || 0) + amount;
    return segments;
  }, {});
  const labels = Object.keys(totals);
  const values = Object.values(totals);
  const fallback = $("#chartFallback");
  fallback.replaceChildren();
  const grandTotal = values.reduce((total, value) => total + value, 0) || 1;
  labels.forEach((label, index) => {
    const row = document.createElement("div");
    row.className = "fallback-row";
    const name = document.createElement("span");
    name.textContent = label;
    const value = document.createElement("strong");
    value.textContent = brl(values[index]);
    const bar = document.createElement("span");
    bar.className = "fallback-bar";
    const fill = document.createElement("span");
    fill.style.width = `${Math.max((values[index] / grandTotal) * 100, 2)}%`;
    bar.append(fill);
    row.append(name, value, bar);
    fallback.append(row);
  });
  const canvas = $("#segmentChart");
  if (typeof window.Chart !== "function" || !labels.length) {
    canvas.hidden = true;
    fallback.hidden = false;
    return;
  }
  fallback.hidden = true;
  canvas.hidden = false;
  if (Audita.chart) Audita.chart.destroy();
  Audita.chart = new window.Chart(canvas, {
    type: "doughnut",
    data: { labels, datasets: [{ data: values, backgroundColor: ["#22c55e", "#818cf8", "#38bdf8", "#fbbf24", "#f472b6"], borderColor: "#0f172a", borderWidth: 4, hoverOffset: 6 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      animation: reduceMotion() ? false : { duration: 600 },
      plugins: {
        legend: { position: "bottom", labels: { color: "#cbd5e1", boxWidth: 9, boxHeight: 9, usePointStyle: true, padding: 18, font: { family: "IBM Plex Sans" } } },
        tooltip: { callbacks: { label: (context) => `${context.label}: ${brl(context.raw)}` } },
      },
    },
  });
}

function statusLabel(status) {
  return { CONFIRMADO: "Confirmado", REVISAR: "Revisar", NAO_ENQUADRADO: "Não enquadrado" }[status] || status;
}

function addTextCell(row, main, detail = "") {
  const cell = row.insertCell();
  const strong = document.createElement("strong");
  strong.textContent = main;
  cell.append(strong);
  if (detail) {
    const small = document.createElement("small");
    small.textContent = detail;
    cell.append(small);
  }
  return cell;
}

function renderFindings() {
  const query = $("#itemSearch").value.trim().toLocaleLowerCase("pt-BR");
  const status = $("#statusFilter").value;
  const body = $("#findingsBody");
  body.replaceChildren();
  const findings = Audita.report.findings.filter((finding) => {
    const haystack = `${finding.description} ${finding.ncm} ${finding.invoice_number}`.toLocaleLowerCase("pt-BR");
    return (!query || haystack.includes(query)) && (status === "ALL" || finding.status === status);
  });
  findings.forEach((finding) => {
    const row = body.insertRow();
    addTextCell(row, finding.description, `Nota ${finding.invoice_number} · item ${finding.item_number}`);
    addTextCell(row, `NCM ${finding.ncm}`, `CFOP ${finding.cfop || "não informado"}`);
    addTextCell(row, `PIS ${finding.pis_cst || "—"} · Cofins ${finding.cofins_cst || "—"}`, `CSOSN ${finding.csosn || "—"} (ICMS, separado)`);
    const evidenceCell = row.insertCell();
    if (finding.evidence) {
      const link = document.createElement("a");
      link.className = "rule-link";
      link.href = finding.evidence.legal_url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = finding.evidence.legal_source;
      const reason = document.createElement("small");
      reason.textContent = finding.evidence.reason;
      evidenceCell.append(link, reason);
    } else {
      evidenceCell.textContent = "Sem correspondência no catálogo MVP";
    }
    if (finding.pending_checks?.length) {
      const pending = document.createElement("small");
      pending.textContent = `Pendente: ${finding.pending_checks.join(" ")}`;
      evidenceCell.append(pending);
    }
    const statusCell = row.insertCell();
    const pill = document.createElement("span");
    pill.className = `status-pill status-${finding.status}`;
    pill.textContent = statusLabel(finding.status);
    statusCell.append(pill);
    const amount = row.insertCell();
    amount.className = "number";
    amount.textContent = brl(finding.estimated_overpayment);
  });
  $("#emptyTable").hidden = findings.length !== 0;
}

function initEvidence() {
  $$("[data-opinion-tab]").forEach((button, index, tabs) => {
    button.addEventListener("click", () => {
      Audita.opinionTab = button.dataset.opinionTab;
      tabs.forEach((tab) => tab.setAttribute("aria-selected", String(tab === button)));
      renderOpinion();
    });
    button.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
      event.preventDefault();
      const offset = event.key === "ArrowRight" ? 1 : -1;
      tabs[(index + offset + tabs.length) % tabs.length].focus();
    });
  });
  $("#itemSearch").addEventListener("input", renderFindings);
  $("#statusFilter").addEventListener("change", renderFindings);
}

async function loadHealth() {
  try {
    const response = await api("/api/health");
    const health = await response.json();
    $("#engineStatus").lastChild.textContent = health.key_configured ? " OpenAI + fallback ativos" : " Motor local ativo";
  } catch (_) {
    $("#engineStatus").lastChild.textContent = " Motor disponível offline";
  }
}

function initIntake() {
  const dropzone = $("#dropzone");
  const input = $("#fileInput");
  dropzone.addEventListener("click", () => input.click());
  dropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); input.click(); }
  });
  ["dragenter", "dragover"].forEach((type) => dropzone.addEventListener(type, (event) => { event.preventDefault(); dropzone.classList.add("is-dragging"); }));
  ["dragleave", "drop"].forEach((type) => dropzone.addEventListener(type, (event) => { event.preventDefault(); dropzone.classList.remove("is-dragging"); }));
  dropzone.addEventListener("drop", (event) => updateFiles(event.dataTransfer.files));
  input.addEventListener("change", () => updateFiles(input.files));
  $("#pgdasSegregated").addEventListener("change", (event) => {
    $("#segregationLabel").textContent = event.target.checked ? "Sim, já segregada" : "Não informada como segregada";
  });
  $("#uploadForm").addEventListener("submit", runUpload);
  $("#demoButton").addEventListener("click", runDemo);
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();
  initIntake();
  initEvidence();
  loadHealth();
});
