# Clinical AI Evaluation Engineer: first 90 days in a large health system

**Audience:** You were hired as a Clinical AI Evaluation Engineer (or equivalent title) at a large integrated health system (IDN): academic medical center, community hospitals, employed clinics, central IT, compliance, and often an innovation or digital health group.

**Voice:** This document is written as a **realistic playbook**—what typically exists, what friction you should expect, and what *you* do in the first weeks. It is not legal advice and not a substitute for your employer's policies.

**Assumption:** The organization already has *some* interest in LLM-style tools (documentation assistant, patient messaging draft support, ambient documentation, coding/ops assistants, etc.) and is **not** handing you a greenfield science project with no governance.

**Remote / hybrid:** Many health-system roles in this lane are **remote-friendly for the evaluation engineer** but **not** “work from any network on any device.” Sections 1 and the **Remote and hybrid work** addendum below spell out what changes when you are not on campus.

---

## How this maps to the six onboarding buckets

1. Access and identity  
2. The system under evaluation  
3. Evaluation artifacts (plans, data, rubrics, tickets)  
4. People and process (clinical, legal, privacy, security, product)  
5. Tools (where work actually lives)  
6. What you often *do not* get on day one—and what you build anyway  

---

## 0. Pre-start reality check (what "big health system" implies)

- **Compliance is not optional.** HIPAA, state privacy, enterprise security, audit logging, and often union/labor considerations shape *every* evaluation workflow.
- **"Clinical AI" rarely means one model.** You will evaluate **systems**: EHR integration, prompts, retrieval layers, human-in-the-loop UX, disclaimers, escalation paths, and operational monitoring.
- **Data movement is controlled.** Expect: no patient data on personal devices, restricted environments, approved workstations, VPN/VDI, encryption, DLP tooling, and mandatory training certificates before access expands.
- **Evaluation is political as well as technical.** Your job includes producing evidence that leadership can defend to risk, compliance, and clinicians.

---

## 1) Access and identity (Week 0–1)

### What you are usually given

- **Corporate identity:** HR onboarding, payroll, badge, device policy (CYOD/COBO), acceptable use agreements.
- **Security training:** HIPAA awareness, phishing, incident reporting, "clean desk," social engineering basics—often required before broader technical access.
- **Core collaboration:** Email, calendar, corporate chat (Teams/Slack Enterprise), video conferencing.
- **Work device posture:** A managed laptop or a virtual desktop (VDI) for accessing internal apps and restricted resources.

### What you should do (practical)

- **Clarify your "evaluation persona" access class** early: are you allowed to see **real PHI** for evaluation, or only **de-identified/synthetic** sets? Many teams start you on **synthetic** or **limited datasets** until additional approvals complete.
- **Ask for the onboarding checklist** from your manager: *"What access gates block me from running my first offline eval suite?"*
- **Document your access requests as tickets** (do not rely on verbal approvals). Big systems run on **audit trails**.

### Typical friction (normal)

- Waiting **days to weeks** for elevated access (especially anything touching production-like environments).
- Being told "use the approved path only"—shadow IT is a career-risk in healthcare enterprises.

---

## 2) The system under evaluation (Week 1–3)

### What you are usually given

In a mature program, you receive **one or more** of:

- **A staging / pre-production environment** that mirrors production behavior closely enough for evaluation.
- **API access** through an internal gateway (not raw public keys in a notebook on your laptop—often a broker with token rotation, IP allow lists, and logging).
- **Product documentation:** intended use, prohibited use, user personas, workflow diagrams, and the "clinical safety narrative" the legal team wants defended.

In an immature program, you receive:

- A vendor demo, a pilot chat UI, and a Slack channel—**and you help define** what "evaluation-ready" means.

### What you should do (practical)

- **Write down the evaluation unit** explicitly:
  - Are you evaluating **(A)** model only, **(B)** model + retrieval + policy layer, or **(C)** full workflow in the EHR/app?
- **Freeze a baseline configuration** for any serious evaluation:
  - model identifier / version, prompt template version, retrieval index version, feature flags, locale, clinical content packs.
- **Demand a "known-good smoke test"** from engineering: a minimal reproducible call path (curl/Postman/internal script) with stable endpoints.

### Typical friction (normal)

- "Staging isn't stable." You will need **retry policies**, maintenance windows, and a written agreement on what counts as an **environment fault** vs a **model defect**.

---

## 3) Evaluation artifacts (Week 1–6, continuous)

### What you are usually given (forms)

These arrive as a mix of:

- **Word/Google Docs / Confluence:** charter, intended use, risk framing.
- **Spreadsheets or structured tables:** scenario libraries (prompt sets), sometimes with metadata (specialty, acuity, vulnerable populations, medication class).
- **Work trackers:** Jira/Azure DevOps/ServiceNow for defects, severity, owners, due dates.
- **Datasets:**
  - Often **not** "CSV on laptop." More commonly: **approved project folder**, **internal blob store**, **Snowflake/BigQuery** table with access roles, **IRB protocol** linkage if human subjects research, or a **vendor-provided** benchmark under contract.
- **Rubric materials:** what "good" means, sometimes with exemplar responses.

### What you should produce (this is your job)

Even if artifacts are incomplete, you drive creation of:

1. **Evaluation plan** aligned to intended use (explicit in-scope / out-of-scope).
2. **Scenario taxonomy** with risk tiers (P0/P1 style mapping is common in practice, even if informal at first).
3. **Pass/fail definitions** that separate:
   - **Hard safety failures** (missed emergency escalation, prescribing-like instructions, etc.—defined with clinical partners)
   - **Quality failures** (unhelpful but not immediately harmful)
   - **Policy failures** (discloses restricted content, violates consent, etc.)
4. **Defect taxonomy** consistent with engineering workflows (repro steps, environment, severity, affected cohort).
5. **Reporting templates** for leadership: "what we tested, what failed, residual risk, mitigations, and what we recommend blocking vs shipping with guardrails."

### Typical friction (normal)

- Clinical stakeholders are **time-limited.** You will need **async review** packs (short briefs, highlighted cases) and standing meetings with crisp agendas.
- Legal/privacy may require you to avoid retaining certain prompt/response content. Plan **logging minimization** + **controlled sampling** from the start.

---

## 4) People and process (Week 1 onward—never "done")

### The coalition you navigate (typical)

- **Clinical SMEs:** specialty experts for chart review–adjacent judgment; often part-time.
- **CMIO / clinical informatics:** bridges IT, clinicians, operations.
- **Compliance & privacy:** HIPAA min necessary, BAAs, data use agreements.
- **Information security:** threat modeling, penetration testing coordination, secure SDLC expectations.
- **Legal / risk:** contracts, product claims, malpractice sensitivities.
- **Product / program management:** scope, roadmap, prioritization.
- **Engineering / ML ops:** deployability, monitoring, rollback, configs.

### Processes you should clarify early

- **Who can declare a release "safe enough"?** Often: a **multi-disciplinary review** with documented outcomes—not an evaluator acting alone.
- **How failures are escalated:** severity rubric, SLA for fixes, emergency kill-switch path for production pilots.
- **How human review is operationalized:** who reviews, how many reviewers, adjudication for disagreement, and how feedback trains the next rubric version.

### What you should do (practical)

- **Schedule a 30-minute intake with each stakeholder group** in the first 2 weeks. Goal: map decisions, not deep dives.
- **Create a one-page RACI** (Responsible/Accountable/Consulted/Informed) for evaluation milestones.
- **Establish a weekly defect triage** with engineering representation—otherwise evaluations become shelf-ware.

---

## 5) Tools (what you will actually use—messy and real)

Expect a portfolio of:

- **Spreadsheets** for early scenario tracking (yes, even in large enterprises).
- **Git** for internal harness code *if* the org allows engineering-owned repos; sometimes you start in a shared drive until security approves.
- **Ticketing** as the system of record for defects.
- **BI/dashboards** later for monitoring; early pilots often export CSV summaries from approved warehouses.

How this portfolio repository maps:

- **Manifest / versioning mindset** becomes: config/version tracking in enterprise tooling + change control.
- **Automated triage scoring** becomes: mixed methods—rules, classifiers, sometimes LLM-as-judge *with governance*, always calibrated against humans on a sample.

### Typical friction (normal)

- You may not get your favorite stack. **Adopt the enterprise toolchain** unless you have explicit permission otherwise.

---

## 6) What you often do *not* get immediately—and what you do instead

### Common gaps on arrival

- No clean "golden dataset."  
- No stable staging.  
- No unified rubric.  
- No agreement on severity.  
- No clarity on whether evaluation is **research** vs **quality** vs **regulatory evidence**.

### What a senior evaluator does (realistic playbook)

1. **Start with risk-based scoping:** identify the top failure modes that could harm patients *in this specific workflow*.
2. **Build a minimum viable evaluation loop:**
   - scenarios to runs to captured outputs to defects to fixes to rerun (regression).
3. **Pilot human review on a small stratified sample** (high risk categories oversampled).
4. **Negotiate data handling** with privacy/security *before* scaling (avoid "we already collected everything").
5. **Write like an auditor:** tie conclusions to evidence, cite versions, avoid over-claiming model "accuracy" where the real claim is "meets agreed safety gates under defined limitations."

---

## Remote and hybrid work (what changes when you are not on campus)

Large health systems **do** hire Clinical AI evaluation staff remotely, but the job is **high-trust** and **high-compliance**. The work pattern differs from generic software remote roles in predictable ways.

### What usually stays the same

- **Governance:** HIPAA, minimum necessary, BAAs, audit expectations, and “who signs off on risk” do not disappear because you work from home.
- **The evaluation loop:** scenarios, runs, capture, defects, fixes, regression—still your core craft.
- **Stakeholders:** you still need clinical, legal, privacy, security, product, and engineering in the loop; you just meet them differently.

### What gets harder (and how senior people handle it)

1. **Network and endpoint discipline**  
   Remote access is almost always **VPN and/or VDI**, **managed device**, and sometimes **region-locked** (employer country/state). Personal PCs, consumer VPNs, or “just SSH from the coffee shop” are commonly **out of policy** for anything involving sensitive artifacts.  
   **Do:** confirm the approved remote stack on day one (device, MFA, split tunnel rules, whether PHI may ever hit the local disk).

2. **“Hallway” clinical context disappears**  
   You will not overhear how nurses talk about a workflow or how attendings react to draft text.  
   **Do:** schedule **short recurring touchpoints** with 1–2 clinical partners; ask for **screen-share** walkthroughs of the real UI; record **de-identified** workflow notes in the approved wiki (not ad hoc notes on paper).

3. **Asynchronous review becomes the default**  
   Clinical SMEs will not live in your Slack.  
   **Do:** send **small packets** (5–10 cases, one-page summary) with a clear ask and deadline; use **tracked decisions** in tickets/docs so remote handoffs do not lose nuance.

4. **Time zones and on-call realities**  
   Incidents (model misbehavior in pilot) may need fast triage across regions.  
   **Do:** clarify **coverage expectations** up front—evaluation engineers are not always 24/7, but pilots sometimes expect a human escalation path.

5. **Shipping and handling of artifacts**  
   Some systems **forbid** exporting evaluation sets to personal cloud drives. Remote work increases the temptation to “just use Dropbox.” **Do not.**  
   **Do:** use **approved** repositories, file shares, or data platforms; treat DLP warnings as a signal to stop and open a ticket.

6. **Occasional on-site expectations**  
   Even “remote” roles may require **quarterly** visits, kickoffs, vendor audits, security intros, or clinical immersion days.  
   **Do:** budget travel and calendar it before you commit to side projects that assume zero travel.

### Remote-specific collaboration patterns that work

- **Written decision logs:** after key meetings, a three-bullet summary: decision, owner, date—stored where the org retains records.
- **Living risk register:** simple table (risk, likelihood, impact, mitigation, owner). Remote teams die when risk lives only in verbal calls.
- **Office hours:** a predictable weekly slot for engineers/clinicians to drop in async or live—reduces random ping fatigue.

### How this ties back to your portfolio harness

Everything you built around **manifests, versioning, CI, and documented calibration** is *more* valuable remotely: it replaces some of the trust you would get from sitting beside an engineer. In a job, you push the same habit—**evidence over vibes**—into Confluence/Jira and approved data stores.

---

## A concrete 30/60/90 outline (big health system style)

### First 30 days

- Complete access trainings; establish secure working pattern (approved device, approved storage).  
- Document the system boundary you evaluate (model vs workflow).  
- Inventory existing scenarios/tests; identify duplicates and gaps.  
- Run a **baseline evaluation pass** on staging with manifests/config capture (whatever your org permits).  
- Produce a **first defects report** with severity recommendations *and* explicit limitations.

### First 60 days

- Establish rubric v1 with clinical sign-off on **hard failures.**  
- Implement regression set v1 (small but painful).  
- Formalize triage meeting cadence; integrate with engineering estimation.  
- Begin agreement metrics on a sample if human review exists (even lightweight).

### First 90 days

- Define release gate criteria ("must pass" vs "waivers allowed").  
- Pilot monitoring plan for production-limited rollouts (sampling, sentinel cases, escalation triggers).  
- Refine scenario library by specialty/vulnerable populations as needed.  
- Consolidate documentation for audit readiness: what was tested, how, by whom, what failed, what changed.

---

## Hard truths (to stay credible in interviews and on the job)

- **Your evaluation harness does not replace clinical judgment**—it compresses search and supports governance.  
- **Perfect safety is not a reasonable goal; accountable risk management is.**  
- **The hardest part is rarely the API**—it is alignment, data rights, and operational follow-through.

---

## Why "who declares release safe enough" is a process question

Automation can score cases and surface defects, but in a large health system **accountability** sits with defined roles: clinical leadership, product/risk, compliance, and documented governance. The evaluator supplies **evidence and severity recommendations**; the organization decides **acceptance, waivers, or blocks** under its policies. Treating release as a purely technical threshold invites both regulatory and patient-safety gaps.

---

## Appendix: what to ask a hiring manager at offer stage (signals maturity)

1. What environment will I use first (staging, prod-like, synthetic only)?  
2. What PHI classes can I access, under what approvals?  
3. Who owns the clinical sign-off for safety failures?  
4. How are defects tracked and what is the fix SLA for P0?  
5. Is any evaluation considered human subjects research requiring IRB?  
6. What logging/retention policy applies to prompts and responses?

### If the role is remote or hybrid

7. What is the **approved** remote access model (VPN, VDI, managed device only)?  
8. May evaluation artifacts with **PHI** leave approved systems—and if so, under what encryption and retention rules?  
9. Are there **on-site** expectations (frequency, location) for security, clinical immersion, or leadership reviews?  
10. What are the **core hours / escalation** expectations across time zones for pilot incidents?
