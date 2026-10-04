# OmniBCI Discovery Lab: 3-Minute Technical Pitch Script
**Hack-Nation 7th Global AI Hackathon — Challenge 03: Agentic Scientific Discovery**  
**Presenter:** Mario De Lorenzo  
**Target Duration:** Exactly 180 Seconds (3:00) · 9 Slides (20s per slide)  
**Deliverables:** 
- High-Definition Slide Deck (PNG): [`omnibci/submission/slides/`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/)
- Multi-Page PDF: [`omnibci/submission/pitch_slides.pdf`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/pitch_slides.pdf)
- Interactive Presentation Webapp: [`omnibci/submission/pitch_slides.html`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/pitch_slides.html)

---

## Slide 1: Title & System Overview (Banner Aesthetic)
*Time: 0:00 – 0:20 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_01_title.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_01_title.png)

### Visual Layout:
- Electric cyan-and-blue aesthetic echoing the repository banner.
- Glowing $\Psi$ emblem, Hack-Nation Challenge 03 badge, and author credit (*"Created by Mario De Lorenzo"*).
- Summary cards highlighting the core workflow: Literature $\rightarrow$ Databricks Omnigent $\rightarrow$ Stanford Paper2Agent $\rightarrow$ Kaggle Benchmark.

### Spoken Pitch Script:
> "Motor imagery brain-computer interfaces allow stroke patients to control robotic rehabilitation devices with neural intent. But clinical adoption stalls on one fundamental bottleneck: every brain is anatomically distinct, and translating newly published machine learning papers to a clinic's hardware takes months of engineering.
> 
> We built OmniBCI Discovery Lab to close this gap. It is an autonomous agentic platform that discovers peer-reviewed algorithms in literature, converts their code into verified execution tools, and optimizes them for real patient datasets in minutes rather than months."

---

## Slide 2: The Research Bottleneck (Empirical Workload Data)
*Time: 0:20 – 0:40 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_02_literature_bottleneck.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_02_literature_bottleneck.png)

### Visual Layout:
- Three empirical metric cards:
  - **35% – 45%** of research time spent reading literature (over 15,000 papers/year).
  - **Up to 80%** of ML engineering trapped in pipeline plumbing and montage translation.
  - **70%+** of published academic codebases failing to run out-of-the-box.
- Direct comparison table: Manual Workflow (48.0 Hours) vs. OmniBCI Autonomous Turnaround (70 Seconds / 0.14 Minutes).

### Spoken Pitch Script:
> "Examine where research time actually disappears. Workload surveys show neuroengineers dedicate up to forty-five percent of their working hours simply reading literature to identify relevant baselines.
> 
> Once selected, industry benchmarks reveal that up to eighty percent of project time goes into plumbing: adapting channel montages, resolving library deprecations, and debugging unverified GitHub codebases. More than seventy percent of published repositories fail to run without manual intervention.
> 
> On our 17-subject Kaggle benchmark, building a manual literature screening and cross-validation pipeline took 48 hours. OmniBCI completes that exact cycle in 70 seconds—a 40-fold acceleration."

---

## Slide 3: GitHub Repository & Databricks Omnigent Harness
*Time: 0:40 – 1:00 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_03_github_repo_omnigent.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_03_github_repo_omnigent.png)

### Visual Layout:
- Left card: `mattin89/OmniBCI` directory structure showing modular agent architecture, MCP tool wrappers, and Kaggle data splits.
- Right card: `omnigent_config.yaml` showing Omnibox container sandboxing, \$25 Anthropic token cap, and the Clinical Safety Governor enforcing a 10.0% ceiling on resting false positive rates.

### Spoken Pitch Script:
> "Inside our open repository, Databricks Omnigent orchestrates a six-stage meta-harness inside isolated Omnibox containers.
> 
> Omnigent enforces strict financial and clinical policies. A twenty-five dollar token cap prevents runaway API expenditures, while a Clinical Safety Governor monitors real-time decoding metrics. Any architecture producing a resting false positive rate above ten percent is automatically flagged and rejected. In stroke rehabilitation, false triggers actuate robotic arms without patient intent, posing physical risks."

---

## Slide 4: Autonomous Literature Harvesting (Stage 1)
*Time: 1:00 – 1:20 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_04_literature_harvesting.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_04_literature_harvesting.png)

### Visual Layout:
- Left card: Live queries against arXiv Export API (`export.arxiv.org`) and OpenAlex REST API (`api.openalex.org`).
- Right card: Ingested publications with author citations, verified repository links, and parsed mathematical formulas (He & Wu 2020, Duggento & De Lorenzo 2022, Lawhern et al. 2018).

### Spoken Pitch Script:
> "When a researcher states an objective, the Literature Harvester queries the arXiv and OpenAlex APIs directly. It scans motor intention preprints across computer science and quantitative biology, indexing peer-reviewed citations, author venues, and verified repository links.
> 
> For our benchmark, the harvester retrieved He and Wu's Riemannian Euclidean Alignment, Duggento and De Lorenzo's Intertwined Neural Network, and Lawhern's EEGNet. It extracted mathematical formulations and tensor bounds directly from the text."

---

## Slide 5: Automatic GitHub Model Import into MCP Tools (Stage 2)
*Time: 1:20 – 1:40 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_05_paper2agent_mcp_import.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_05_paper2agent_mcp_import.png)

### Visual Layout:
- Three active Model Context Protocol (MCP) tool cards:
  - `riemannian_ea_mcp.py`: Manifold pre-whitening ($\tilde{\mathbf{X}} = \bar{\mathbf{R}}_s^{-1/2} \mathbf{X}$).
  - `intertwined_mcp.py`: Spatio-temporal time-distributed convolutions and bidirectional GRUs.
  - `eegnet_mcp.py`: Compact separable convolutional neural network.

### Spoken Pitch Script:
> "Stanford's Paper2Agent synthesizer converts these cloned GitHub repositories into active Model Context Protocol tools.
> 
> Instead of treating code as unverified text, the synthesizer inspects the abstract syntax tree, extracts canonical PyTorch model classes, and binds them to our target montage: eight wearable electrodes sampled at 250 Hertz. Each model becomes an isolated, unit-tested tool ready for execution."

---

## Slide 6: Verified Execution Primitives vs. Conventional LLM Hallucinations
*Time: 1:40 – 2:00 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_06_verified_primitives_vs_hallucination.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_06_verified_primitives_vs_hallucination.png)

### Visual Layout:
- Comparison layout:
  - ❌ Conventional LLM Code Generation: hallucinates non-existent APIs, crashes on tensor shapes, introduces silent data leakage, ignores clinical safety.
  - ✅ OmniBCI Grounded MCP Primitives: AST extraction from original codebases, guaranteed tensor harmonization, sandboxed unit tests, strict cross-subject isolation.

### Spoken Pitch Script:
> "This architectural choice separates OmniBCI from standard code-generation LLMs. Raw language models hallucinate non-existent PyTorch parameters, fail on spatial tensor dimensions, and frequently leak test data into training normalization.
> 
> OmniBCI provides the reasoning agent with grounded execution primitives. Alignment matrices and covariance statistics are computed strictly on training subjects, ensuring verified numerical integrity and genuine clinical generalization."

---

## Slide 7: Grounded Citation Popovers with Verbatim Excerpts
*Time: 2:00 – 2:20 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_07_grounded_citation_popovers.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_07_grounded_citation_popovers.png)

### Visual Layout:
- High-resolution screenshot of the interactive citation hover card (`02_omnibci_citation_hover.png`).
- Side panel detailing verbatim excerpt extraction, exact section anchoring (Section 2.3), DOI hyperlinks, and the machine-readable evidence database (`literature_evidence.json`).

### Spoken Pitch Script:
> "In medical systems, traceability is essential. Every claim, tensor modification, or hyperparameter proposed by the co-pilot links directly to verbatim excerpts from the source paper.
> 
> Clinicians hover over citation tags to view the original methodology paragraph, section number, and DOI link. Every reference is logged in a machine-readable literature evidence file, establishing an auditable trail for clinical verification."

---

## Slide 8: 17-Subject Leave-One-Subject-Out (LOSO) Validation Protocol
*Time: 2:20 – 2:40 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_08_loso_validation_protocol.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_08_loso_validation_protocol.png)

### Visual Layout:
- Embedded JupyterLab interface executing cell-by-cell 17-fold cross-validation on the UK BCI Consortium dataset (`04_omnibci_jupyterlab.png`).
- Protocol cards outlining the 17-fold cross-validation split, dynamic multi-notebook compilation, and real-time streaming metrics.

### Spoken Pitch Script:
> "The Experiment Runner executes a 17-fold Leave-One-Subject-Out validation across all 17 participants from the UK BCI Consortium benchmark.
> 
> In the baseline notebook, unaligned deep models suffered from skull impedance drift, dropping to 52.5% accuracy on outlier subjects with a 13.8% resting false positive rate.
> 
> The Co-Pilot diagnosed this domain collapse and formulated **EA-IntertwinedNet**: prepending Riemannian Euclidean Alignment whitening directly before time-distributed neural layers."

---

## Slide 9: Official Kaggle Leaderboard & EA-IntertwinedNet Champion
*Time: 2:40 – 3:00 (20 Seconds)*  
*Slide File:* [`omnibci/submission/slides/slide_09_kaggle_leaderboard_champion.png`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/slides/slide_09_kaggle_leaderboard_champion.png)

### Visual Layout:
- Official Kaggle 17-Subject Cross-Validation Leaderboard:
  - 🥇 **Rank 1: EA-IntertwinedNet** — **99.71% Accuracy ($\pm 1.18\%$)**, $\kappa = 0.994$, Rest FPR = 0.29%, Latency = 5.8 ms.
  - 🥈 **Rank 2: Riemannian EA-TS** — 96.91%, $\kappa = 0.938$, Rest FPR = 1.47%, Latency = 4.2 ms.
  - 🥉 **Rank 3: EEGNet** — 87.06%, $\kappa = 0.741$, Rest FPR = 8.50%, Latency = 12.8 ms.
  - **4th: Unaligned Intertwined Net** — 90.15%, Rest FPR = 13.8% (clinical ceiling breached).
- Highlights: Outlier Sub-03 recovered from 55.0% to 96.67%; Sub-11 recovered from 52.5% to 95.0%; `submission_ea_intertwined.csv` verified.

### Spoken Pitch Script:
> "When approved, OmniBCI compiled a new Jupyter notebook and executed the pipeline.
> 
> The resulting model delivered **99.71% accuracy** with a Cohen's kappa of **0.994**, cutting the resting false alarm rate to **0.29%**. It recovered outlier subject Sub-03 from 55.0% to 96.67% and secured Rank 1 on the Kaggle benchmark.
> 
> By converting passive scientific literature into active AI discovery tools, OmniBCI reduces a two-week engineering barrier to seventy seconds. Thank you."

---

## Summary Timing & Checklist for Presenter

| Slide # | Title / Topic | Spoken Time | Pace | Key Takeaway |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Title & Overview | 0:00 – 0:20 | 58 words | Sets the clinical problem & introduces OmniBCI. |
| **2** | The Research Bottleneck | 0:20 – 0:40 | 66 words | Empirical stats (45% lit, 80% plumbing, 48h vs. 70s). |
| **3** | GitHub Repo & Omnigent | 0:40 – 1:00 | 59 words | \$25 budget cap & 10% clinical FPR safety gate. |
| **4** | Autonomous Literature Harvesting | 1:00 – 1:20 | 56 words | arXiv/OpenAlex APIs & mathematical extraction. |
| **5** | Paper2Agent MCP Import | 1:20 – 1:40 | 55 words | AST model class extraction to 8-channel wearable montage. |
| **6** | Verified Primitives vs. Hallucinations | 1:40 – 2:00 | 58 words | Eliminating LLM bugs, tensor errors, and data leakage. |
| **7** | Grounded Citation Popovers | 2:00 – 2:20 | 54 words | Verbatim text, DOI links, and clinical provenance. |
| **8** | 17-Subject LOSO Protocol | 2:20 – 2:40 | 57 words | Domain collapse diagnosis & EA-IntertwinedNet formulation. |
| **9** | Kaggle Leaderboard Champion | 2:40 – 3:00 | 62 words | **99.71%**, $\kappa = 0.994$, 0.29% FPR, Rank 1 Kaggle. |
| **Total**| **Complete Pitch** | **3:00 (180s)**| **525 words**| **Average speaking pace: 175 wpm (comfortable, authoritative)** |
