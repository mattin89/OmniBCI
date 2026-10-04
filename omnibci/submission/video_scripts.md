# OmniBCI Hackathon Demonstration Videos: Scripts & Technical Choreography (v3)

**Hack-Nation 7th Global AI Hackathon — Challenge 03: Agentic Scientific Discovery**  
**Powered by Databricks Omnigent & Stanford Paper2Agent**  
**Narrator Voice:** ElevenLabs Creator Tier — *Rocco G.* (Young adult male, Italian accent speaking natural English, Voice ID: `UEw8Jol3Z7Kb3TdaL0BQ`)  
**Hard Constraint:** Both videos are strictly maximum 1 minute (<= 60.0s).

---

## 1. Video 1: Product Demonstration (Duration: 52.52 Seconds)
*Output Video:* [`omnibci/submission/demo_product_video.mp4`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/demo_product_video.mp4)  
*Audio Track:* [`omnibci/submission/demo_product_audio_v3.mp3`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/demo_product_audio_v3.mp3)  
*Runtime:* **52.52 seconds (Strictly < 60s)**

### Narrative Flow & Real Workstation Choreography

* **[0:00 - 0:04.8] Scene 1: OmniBCI Value Hook + Workstation Overview**
  > "OmniBCI helps researchers find and analyze complex datasets and AI models in literature, then deploy and improve them in minutes — not months."
  * **Visual:** Full high-resolution view of the active OmniBCI web application interface (`01_omnibci_conversation.png`) with a value proposition overlay card.

* **[0:04.8 - 0:11.0] Scene 2: Selecting Kaggle Dataset**
  > "On the right panel, we select our Kaggle motor rehabilitation dataset across seventeen subjects."
  * **Visual:** Smooth zoom onto the real **Target EEG Dataset** card on the right panel (UK BCI Consortium, 17 calibration subjects, 8 wearable electrodes at 250 Hz).

* **[0:11.0 - 0:15.5] Scene 3: Importing Custom Intertwined Model**
  > "We import our custom intertwined neural network model."
  * **Visual:** Camera pans down to the real **Synthesized Models** panel, highlighting `Intertwined Neural Network (Duggento, De Lorenzo, et al., 2022)`.

* **[0:15.5 - 0:27.5] Scene 4: Clinician Research Objective**
  > "We ask the co-pilot: 'Analyze in literature how to deploy and optimize this model for the highest accuracy.'"
  * **Visual:** Focus shifts to the chat conversation, displaying the user prompt in the interactive message bubble.

* **[0:27.5 - 0:33.5] Scene 5: Literature Diagnostic**
  > "The agent diagnoses inter-subject covariance shift."
  * **Visual:** Real Co-Scientist diagnostic response citing He & Wu 2019.

* **[0:33.5 - 0:40.5] Scene 6: Baseline Jupyter Notebook Run**
  > "Unaligned accuracy stalls at 87 percent with high false positives."
  * **Visual:** Real embedded JupyterLab (`04_omnibci_jupyterlab.png`) — 87.21% accuracy, 14.12% FPR (unsafe).

* **[0:40.5 - 0:45.5] Scene 7: Proposal & Governance Approval**
  > "The AI chat proposes EA-IntertwinedNet. We click proceed."
  * **Visual:** Architectural proposal card + clinician clicks `[Proceed]`.

* **[0:45.5 - 0:52.52] Scene 8: New Notebook Synthesis — 99.71% · κ=0.994 · FPR=0.29%**
  > "OmniBCI compiles a new notebook. The new model hits 99.71 percent accuracy, kappa 0.994, false positive rate 0.29 percent — Rank 1, outperforming the literature."
  * **Visual:** Leaderboard (`03_omnibci_benchmark_charts.png`) — **EA-IntertwinedNet Rank 1: 99.71% (±1.18%), κ=0.994, FPR=0.29%**.

---

## 2. Video 2: Technical Walkthrough (Duration: 59.86 Seconds)
*Output Video:* [`omnibci/submission/walkthrough_technical_video.mp4`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/walkthrough_technical_video.mp4)  
*Audio Track:* [`omnibci/submission/walkthrough_technical_audio_v3.mp3`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/walkthrough_technical_audio_v3.mp3)  
*Runtime:* **59.86 seconds (Strictly < 60s)**

### Narrative Flow & Technical Architecture

* **[0:00 - 0:08.5] Scene 1: GitHub Repository & Omnigent Harness**
  > "Here inside the OmniBCI repository, Databricks Omnigent coordinates a multi-agent harness inside isolated sandboxes."
  * **Visual:** `mattin89/OmniBCI` repo tree + `omnigent_config.yaml`.

* **[0:08.5 - 0:17.1] Scene 2: Stage 1 Literature Harvester**
  > "First, the Literature Agent queries arXiv and OpenAlex to fetch peer-reviewed papers on motor decoding and domain shift."
  * **Visual:** Live API queries + ingested publications panel.

* **[0:17.1 - 0:25.5] Scene 3: Automatic GitHub Model Ingestion into MCP Tools**
  > "Omnigent found these papers and automatically imported the models from their GitHub repositories as active Model Context Protocol tools."
  * **Visual:** Paper2Agent ingestion pipeline → `omnibci/mcp_tools/`.

* **[0:25.5 - 0:31.1] Scene 4: Verified Execution Primitives**
  > "This gives the AI chat verified execution primitives rather than hallucinated code."
  * **Visual:** Hallucination vs. MCP grounded primitives comparison.

* **[0:31.1 - 0:36.9] Scene 5: Grounded Citation Popovers**
  > "Every architectural suggestion links directly to verbatim excerpts and original publications."
  * **Visual:** Citation hover card (`02_omnibci_citation_hover.png`).

* **[0:36.9 - 0:44.0] Scene 6: 17-Subject LOSO Validation**
  > "Finally, we run Leave-One-Subject-Out validation across seventeen participants."
  * **Visual:** JupyterLab executing 17-fold LOSO (`04_omnibci_jupyterlab.png`).

* **[0:44.0 - 0:59.86] Scene 7: Leaderboard Rank 1 — 99.71% · κ=0.994 · FPR=0.29%**
  > "The AI-proposed EA-IntertwinedNet reaches 99.71 percent cross-subject accuracy, kappa 0.994, false positive rate 0.29 percent — outperforming the literature and taking first place on the Kaggle leaderboard."
  * **Visual:** Leaderboard table — **EA-IntertwinedNet Rank 1: 99.71% (±1.18%), κ=0.994, FPR=0.29%**, Rank 2: Riemannian EA-TS 96.91%.
