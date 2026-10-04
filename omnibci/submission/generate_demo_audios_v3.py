import os
import urllib.request
import json
from pathlib import Path
from dotenv import load_dotenv
import subprocess

load_dotenv(Path.home() / ".env")
api_key = os.getenv("ELEVENLABS_API_KEY")

voice_id = "UEw8Jol3Z7Kb3TdaL0BQ"  # Rocco G. - Italian accent, young male

# ── Video 1: Product Demo ──────────────────────────────────────────────────────
# Target: ≤ 60s. Opening hook added; trimmed scene 5 to compensate.
# Word count budget ~115 words ≈ 58s at Rocco's ~120 wpm pacing.
script_1_text = (
    "OmniBCI helps researchers find and analyze complex datasets and AI models in literature, "
    "then deploy and improve them in minutes — not months. "
    "On the right panel, we select our Kaggle motor rehabilitation dataset across seventeen subjects. "
    "We import our custom intertwined neural network model. "
    "We ask the co-pilot: 'Analyze the literature to deploy and optimize this model for the highest accuracy.' "
    "The agent diagnoses inter-subject covariance shift. "
    "Unaligned accuracy stalls at 87 percent with high false positives. "
    "The AI chat proposes EA-IntertwinedNet. We click proceed. "
    "OmniBCI compiles a new notebook. "
    "The new model hits 99.71 percent accuracy, kappa 0.994, false positive rate 0.29 percent — Rank 1, outperforming the literature."
)

# ── Video 2: Technical Walkthrough ────────────────────────────────────────────
# Target: ≤ 60s. Final result updated to 99.71% with full metrics.
script_2_text = (
    "Here inside the OmniBCI repository, Databricks Omnigent coordinates a multi-agent harness inside isolated sandboxes. "
    "First, the Literature Agent queries arXiv and OpenAlex to fetch peer-reviewed papers on motor decoding and domain shift. "
    "Omnigent found these papers and automatically imported the models from their GitHub repositories as active Model Context Protocol tools. "
    "This gives the AI chat verified execution primitives rather than hallucinated code. "
    "Every architectural suggestion links directly to verbatim excerpts and original publications. "
    "Finally, we run Leave-One-Subject-Out validation across seventeen participants. "
    "The AI-proposed EA-IntertwinedNet reaches 99.71 percent cross-subject accuracy, kappa 0.994, false positive rate 0.29 percent — "
    "outperforming the literature and taking first place on the Kaggle leaderboard."
)

out_dir = Path("omnibci/submission")
out_dir.mkdir(parents=True, exist_ok=True)


def synthesize(text, filename):
    out_path = out_dir / filename
    word_count = len(text.split())
    print(f"Synthesizing {filename} ({word_count} words)...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.48,
            "similarity_boost": 0.85,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        audio = resp.read()
        with open(out_path, "wb") as f:
            f.write(audio)

    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(out_path)
    ]
    dur = float(subprocess.check_output(probe_cmd).decode().strip())
    print(f"  Saved {out_path} ({len(audio):,} bytes, Duration: {dur:.2f}s)")
    assert dur <= 60.0, f"ERROR: Audio {dur:.2f}s exceeds 60s limit!"
    return dur


dur1 = synthesize(script_1_text, "demo_product_audio_v3.mp3")
dur2 = synthesize(script_2_text, "walkthrough_technical_audio_v3.mp3")

print(f"\nAll done. Video 1: {dur1:.2f}s | Video 2: {dur2:.2f}s")
