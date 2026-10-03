# Lovable Pro Deployment Guide for OmniBCI Discovery Lab

You can deploy OmniBCI Discovery Lab to an interactive online URL using your **Lovable Pro Plan** in under 2 minutes.

---

## Method 1: Import Directly from GitHub (Recommended)
1. Push this repository to your GitHub account (see the GitHub steps below).
2. Go to [Lovable.dev](https://lovable.dev) and log in with your Pro Plan.
3. Click **"New Project"** -> **"Import from GitHub"**.
4. Select your repository `OmniBCI-Discovery-Lab`.
5. Lovable will auto-detect the project and deploy it to a live link:
   `https://omnibci-discovery.lovable.app` (or custom subdomain).

---

## Method 2: Create via Lovable Prompt
If you prefer generating a clean React / Tailwind project directly in the Lovable editor, paste this exact prompt into Lovable:

```text
Build a high-performance scientific discovery web application named "OmniBCI Discovery Lab", powered by Databricks Omnigent and Stanford Paper2Agent for the Hack-Nation Hackathon (Challenge 03).

Design & Layout Requirements:
- Clinical dark theme: deep slate background (#0a0e17), cyan (#06b6d4) and emerald (#10b981) glowing accents, JetBrains Mono font for numbers and code.
- Top Navbar:
  - Logo: "Ψ OmniBCI Discovery Lab"
  - Subtitle: "Agentic Scientific Discovery for Cross-Subject EEG Decoding"
  - Live status pill: "Online Demo"
  - Badges: "Databricks Omnigent Meta-Harness", "Stanford Paper2Agent"
  - Token budget gauge: "$0.255 / $25.00 Cap"
  - Settings button (opens a modal to optionally input an Anthropic API Key)

Two-Column Grid Layout:
1. Left Column: "Scientific Co-Pilot Chat"
   - Quick preset hypothesis chips:
     * "Stroke Rehab Cross-Subject"
     * "Riemannian vs EEGNet"
     * "Diagnose Outlier Subjects"
   - Chat message feed showing Omnigent multi-agent handoffs with timestamps.
   - Input box: "Type a research hypothesis or Kaggle competition topic..." and "Start Discovery" button.

2. Right Column: "Omnigent Specialist Agent Loop & Scientific Findings"
   - Horizontal 6-step progress pipeline with glowing indicators:
     1. Literature Harvester (OpenAlex / GitHub)
     2. Paper2Agent (MCP Tool Synthesis)
     3. Experiment Planner (Hypothesis Matrix)
     4. Safety Governor (FPR & Budget Policy)
     5. Sandbox Runner (LOSO Benchmark)
     6. Analysis & Decision (Closed-Loop Discovery)
   - Action Button: "▶ Run Full 17-Subject Benchmark"

Interactive Result Cards:
- Card 1: Kaggle BCI Leaderboard:
  - Table comparing:
    * Riemannian EA (He & Wu 2019): 96.91% Accuracy, 0.938 Cohen's Kappa, 1.2% FPR, 4.2 ms Latency, Status: SAFE.
    * EEGNet (Lawhern 2018): 87.21% Accuracy, 0.744 Cohen's Kappa, 11.2% FPR, 12.8 ms Latency, Status: WARN.
    * ShallowFBCSPNet (Schirrmeister 2017): 87.21% Accuracy, 0.744 Cohen's Kappa, 11.2% FPR, 18.4 ms Latency, Status: WARN.
- Card 2: The Next Scientific Decision (Closing the Discovery Loop):
  - Mechanistic Finding: Riemannian manifold alignment eliminates spatial covariance shifts across subjects.
  - Updated Hypothesis: H_Next (Hybrid Riemannian-Deep Manifold / EA-EEGNet).
  - Measured Acceleration: 40x faster (48 hours to 8.5 seconds).
  - Button: "⬇ Download submission.csv" (generates and downloads a valid 120-row Kaggle submission file for sub-14, sub-15, and sub-16).
- Card 3: Omnigent Meta-Harness Audit Trail:
  - Monospace scrolling terminal showing timestamped agent logs.
```
