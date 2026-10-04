# OmniBCI Hackathon Demonstration Videos: Scripts & Technical Choreography (v2)

**Hack-Nation 7th Global AI Hackathon — Challenge 03: Agentic Scientific Discovery**  
**Powered by Databricks Omnigent & Stanford Paper2Agent**  
**Narrator Voice:** ElevenLabs Creator Tier — *Rocco G.* (Young adult male, Italian accent speaking natural English, Voice ID: `UEw8Jol3Z7Kb3TdaL0BQ`)  
**Hard Constraint:** Both videos are strictly maximum 1 minute (<= 60.0s).

---

## 1. Video 1: Product Demonstration (Duration: 54.06 Seconds)
*Output Video:* [`omnibci/submission/demo_product_video.mp4`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/demo_product_video.mp4)  
*Audio Track:* [`omnibci/submission/demo_product_audio_v2.mp3`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/demo_product_audio_v2.mp3)  
*Runtime:* **54.06 seconds (Strictly < 60s)**

### Narrative Flow & Real Workstation Choreography

* **[0:00 - 0:02.4] Scene 1: Workstation Overview**
  > "Welcome to the OmniBCI workstation."
  * **Visual:** Full high-resolution view of the active OmniBCI web application interface (`01_omnibci_conversation.png`).

* **[0:02.4 - 0:08.4] Scene 2: Selecting Kaggle Dataset**
  > "On the right panel, we select our Kaggle motor rehabilitation dataset across seventeen subjects."
  * **Visual:** Smooth zoom onto the real **Target EEG Dataset** card on the right panel (UK BCI Consortium, 17 calibration subjects, 8 wearable electrodes at 250 Hz, 1,795 trials).

* **[0:08.4 - 0:12.7] Scene 3: Importing Custom Intertwined Model**
  > "Next, we import our custom intertwined neural network model."
  * **Visual:** Camera pans down to the real **Synthesized Models** panel, highlighting `1. An intertwined neural network model for EEG classification in brain-computer interfaces (Duggento, De Lorenzo, et al., 2022)`.

* **[0:12.7 - 0:27.4] Scene 4: Clinician Research Objective**
  > "Now, we ask our co-pilot: 'I want to use this intertwined neural network model to analyze the Kaggle dataset. Analyze in literature how to deploy this model and optimize it for this dataset so it can achieve the highest accuracy in literature.'"
  * **Visual:** Focus shifts to the chat conversation, displaying the user prompt in the interactive message bubble with active literature search indicators.

* **[0:27.4 - 0:33.1] Scene 5: Literature Diagnostic**
  > "The agent analyzes published benchmarks and diagnoses inter-subject covariance shift."
  * **Visual:** Real Co-Scientist diagnostic response explaining cross-subject covariance shifts caused by skull impedance and volume conduction on low-density 8-channel headsets (citing He & Wu 2019).

* **[0:33.1 - 0:40.2] Scene 6: Baseline Jupyter Notebook Run**
  > "In the baseline Jupyter notebook, unaligned accuracy stalls at 87 percent with high false positives."
  * **Visual:** Real embedded JupyterLab interface (`04_omnibci_jupyterlab.png`) executing Cell [4], showing 17-fold LOSO cross-validation where unaligned accuracy stalls at 87.21% and resting false positive rate reaches 14.12% (breaching the 10.0% safety ceiling).

* **[0:40.2 - 0:45.2] Scene 7: Proposal & Governance Approval**
  > "The AI chat proposes EA-IntertwinedNet. We click proceed."
  * **Visual:** Architectural proposal card in chat introducing Riemannian manifold pre-whitening ($\tilde{\mathbf{X}} = \bar{\mathbf{R}}_s^{-1/2} \mathbf{X}$), followed by the clinician clicking `[Proceed]`.

* **[0:45.2 - 0:54.1] Scene 8: New Notebook Synthesis & Outperforming Literature (96.67%)**
  > "OmniBCI compiles a new Jupyter notebook, and the new model reaches 96.67 percent accuracy, outperforming the literature."
  * **Visual:** Dynamically compiled `EA_Intertwined_Pipeline.ipynb` execution and final cross-subject leaderboard (`03_omnibci_benchmark_charts.png`), confirming **Rank 1 at 96.67% accuracy** (recovering Subject 03 from 55.0% to 96.67%, and compressing resting FPR to 1.15%).

---

## 2. Video 2: Technical Walkthrough (Duration: 53.96 Seconds)
*Output Video:* [`omnibci/submission/walkthrough_technical_video.mp4`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/walkthrough_technical_video.mp4)  
*Audio Track:* [`omnibci/submission/walkthrough_technical_audio_v2.mp3`](file:///c:/Users/delor/Downloads/Hack-nation/October%2027/omnibci/submission/walkthrough_technical_audio_v2.mp3)  
*Runtime:* **53.96 seconds (Strictly < 60s)**

### Narrative Flow & Technical Architecture

* **[0:00 - 0:08.5] Scene 1: GitHub Repository & Omnigent Harness**
  > "Here inside the OmniBCI repository, Databricks Omnigent coordinates a multi-agent harness inside isolated sandboxes."
  * **Visual:** Navigating the [`mattin89/OmniBCI`](https://github.com/mattin89/OmniBCI) repository, displaying the multi-agent directory tree and `omnigent_config.yaml` container sandboxing.

* **[0:08.5 - 0:17.1] Scene 2: Stage 1 Literature Harvester**
  > "First, the Literature Agent queries arXiv and OpenAlex to fetch peer-reviewed papers on motor decoding and domain shift."
  * **Visual:** Live API querying across arXiv and OpenAlex, downloading papers on cross-subject transfer learning and low-density montages.

* **[0:17.1 - 0:25.5] Scene 3: Automatic GitHub Model Ingestion into MCP Tools**
  > "Omnigent found these papers and automatically imported the models from their GitHub repositories as active Model Context Protocol tools."
  * **Visual:** Stanford Paper2Agent framework parsing cloned GitHub repositories into standardized Model Context Protocol tools in `omnibci/mcp_tools/`.

* **[0:25.5 - 0:31.1] Scene 4: Verified Execution Primitives**
  > "This gives the AI chat verified execution primitives rather than hallucinated code."
  * **Visual:** Comparison matrix contrasting conventional LLM code hallucinations with verified, unit-tested PyTorch forward passes and tensor harmonization gates.

* **[0:31.1 - 0:36.9] Scene 5: Grounded Citation Popovers**
  > "Every architectural suggestion links directly to verbatim excerpts and original publications."
  * **Visual:** High-resolution zoom on the interactive citation hover card (`02_omnibci_citation_hover.png`) displaying verbatim source text from Duggento & De Lorenzo (2022) Section 2.3 with live DOI links.

* **[0:36.9 - 0:54.0] Scene 6: 17-Subject LOSO Validation & Leaderboard Rank 1 (96.67%)**
  > "Finally, we run Leave-One-Subject-Out validation across seventeen participants. The AI-proposed architecture reaches 96.67 percent cross-subject accuracy, outperforming the literature and taking first place on the Kaggle leaderboard."
  * **Visual:** 17-subject cross-validation results and official leaderboard table confirming **Rank 1 at 96.67% accuracy** (1.15% FPR, 5.8 ms latency), outperforming published literature baselines on the Kaggle benchmark.
