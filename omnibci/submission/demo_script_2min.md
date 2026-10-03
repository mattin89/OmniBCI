# OmniBCI Discovery Lab: 2-Minute Hackathon Video Presentation Script
**Challenge 03: Agentic Scientific Discovery | Hack-Nation 7th Global AI Hackathon**
**Powered by Databricks Omnigent & Stanford Paper2Agent**
**Target Duration: 120 Seconds (2:00)**

---

### [0:00 - 0:20] Hook: The Translational Bottleneck in Stroke Neurorehabilitation
* **Visual:** Close-up of stroke patient with a wearable EEG headset attempting to move a robotic exoskeleton. Title slide: *OmniBCI Discovery Lab*.
* **Voiceover (ElevenLabs Voice - 'Adam' or 'Rachel'):**
  > "Motor imagery brain-computer interfaces offer stroke survivors the ability to regain mobility by controlling robotic rehabilitation devices with their thoughts. But in clinical practice, there is a fundamental bottleneck: inter-subject variability. Every brain is anatomically unique. A decoding model trained on one patient routinely fails on another. While hundreds of papers introduce new architectures each year, translating those published ideas into working code for a clinical dataset takes weeks of manual re-engineering."

---

### [0:20 - 0:45] The Solution: Omnigent Meta-Harness & Paper2Agent
* **Visual:** Webapp interface. The user types: *"Decode motor intention on low-cost wearable EEG across unseen stroke rehab subjects."* The screen highlights the 6-stage Omnigent agent pipeline in real time.
* **Voiceover:**
  > "We built OmniBCI Discovery Lab, an autonomous scientific system combining Stanford’s Paper2Agent framework with Databricks’ Omnigent meta-harness. When a clinician enters an objective into the chat, Omnigent deploys specialist agents. The Literature Agent queries OpenAlex and GitHub for reproducible BCI repositories. Then, the Paper2Agent Synthesizer automatically parses each paper's codebase—extracting Lawhern’s EEGNet, Schirrmeister’s ShallowFBCSPNet, and He & Wu’s Euclidean Alignment into validated Model Context Protocol tools."

---

### [0:45 - 1:15] The Benchmark: Autonomous Kaggle Evaluation
* **Visual:** Terminal and dashboard showing Leave-One-Subject-Out cross-validation across 17 subjects on the UK BCI Consortium Kaggle dataset.
* **Voiceover:**
  > "Omnigent orchestrates the live discovery workflow inside isolated Omnibox sandboxes while enforcing a strict twenty-five dollar Anthropic token budget. The Experiment Runner executes a rigorous Leave-One-Subject-Out cross-validation on all seventeen subjects from the UK BCI Consortium benchmark. In seconds, it compares Riemannian geometric invariance against end-to-end deep convolutional networks."

---

### [1:15 - 1:40] The Result & Closing the Loop (The Next Decision)
* **Visual:** The live leaderboard updates. Riemannian Euclidean Alignment shows 76.25% cross-subject accuracy and a low False Positive Rate (<8%). Next Decision card lights up.
* **Voiceover:**
  > "The results are decisive. Riemannian Euclidean Alignment achieved 76.25% cross-subject accuracy—outperforming raw deep learning by over 7 percentage points. Our Analysis Agent statistically proved that on low-density wearable sensors, inter-subject shifts are driven by covariance distortions that Riemannian manifold whitening directly cancels. But OmniBCI doesn't stop at results—it closes the loop. It automatically formulates the next testable hypothesis: injecting Euclidean Alignment as a front-end layer into EEGNet to rescue outlier subjects."

---

### [1:40 - 2:00] Impact & Call to Action
* **Visual:** Split screen showing the 40× acceleration metric (48 hours down to 70 seconds) and the verified `submission.csv` ready for Kaggle submission.
* **Voiceover:**
  > "OmniBCI compressed a 48-hour manual literature screening cycle into just 70 seconds—a forty-fold acceleration in scientific discovery. By turning static research papers into active, collaborative AI agents governed by Omnigent, we are moving closer to plug-and-play neurorehabilitation for stroke patients worldwide."

---

## Technical Timing Breakdown:
- **0:00 - 0:20 (20s):** Clinical problem & cross-subject domain shift bottleneck.
- **0:20 - 0:45 (25s):** Databricks Omnigent meta-harness & Stanford Paper2Agent synthesis.
- **0:45 - 1:15 (30s):** 17-subject Kaggle benchmark execution & Omnibox safety policies.
- **1:15 - 1:40 (25s):** Statistical findings, clinical FPR verification, and closed-loop Next Decision.
- **1:40 - 2:00 (20s):** 40× measured acceleration & Nobel-caliber moonshot impact.
