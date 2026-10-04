import os
import urllib.request
import json
from pathlib import Path
from dotenv import load_dotenv
import subprocess

load_dotenv(Path.home() / ".env")
api_key = os.getenv("ELEVENLABS_API_KEY")

voice_id = "UEw8Jol3Z7Kb3TdaL0BQ" # Rocco G. - Italian accent, young male

script_1_text = (
    "Welcome to the OmniBCI workstation. "
    "On the right panel, we select our Kaggle motor rehabilitation dataset across seventeen subjects. "
    "Next, we import our custom intertwined neural network model. "
    "Now, we ask our co-pilot: 'I want to use this intertwined neural network model to analyze the Kaggle dataset. "
    "Analyze in literature how to deploy this model and optimize it for this dataset so it can achieve the highest accuracy in literature.' "
    "The agent analyzes published benchmarks and diagnoses inter-subject covariance shift. "
    "In the baseline Jupyter notebook, unaligned accuracy stalls at 87 percent with high false positives. "
    "The AI chat proposes EA-IntertwinedNet. "
    "We click proceed. "
    "OmniBCI compiles a new Jupyter notebook, and the new model reaches 96.67 percent accuracy, outperforming the literature."
)

script_2_text = (
    "Here inside the OmniBCI repository, Databricks Omnigent coordinates a multi-agent harness inside isolated sandboxes. "
    "First, the Literature Agent queries arXiv and OpenAlex to fetch peer-reviewed papers on motor decoding and domain shift. "
    "Omnigent found these papers and automatically imported the models from their GitHub repositories as active Model Context Protocol tools. "
    "This gives the AI chat verified execution primitives rather than hallucinated code. "
    "Every architectural suggestion links directly to verbatim excerpts and original publications. "
    "Finally, we run Leave-One-Subject-Out validation across seventeen participants. "
    "The AI-proposed architecture reaches 96.67 percent cross-subject accuracy, outperforming the literature and taking first place on the Kaggle leaderboard."
)

out_dir = Path("omnibci/submission")
out_dir.mkdir(parents=True, exist_ok=True)

def synthesize(text, filename):
    out_path = out_dir / filename
    print(f"Synthesizing {filename} ({len(text.split())} words)...")
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
            
    probe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(out_path)]
    dur = float(subprocess.check_output(probe_cmd).decode().strip())
    print(f"Saved {out_path} ({len(audio)} bytes, Duration: {dur:.2f}s)")
    assert dur <= 60.0, f"ERROR: Audio duration {dur}s exceeds 60s limit!"

synthesize(script_1_text, "demo_product_audio_v2.mp3")
synthesize(script_2_text, "walkthrough_technical_audio_v2.mp3")
