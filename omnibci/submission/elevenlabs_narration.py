"""
Automated ElevenLabs Voiceover Generator for Hackathon 2-Minute Demo
Uses ElevenLabs API Creator Tier to synthesize realistic narration from demo_script_2min.md.
"""

import os
import re
import urllib.request
import json

def generate_voiceover(
    script_path: str = "omnibci/submission/demo_script_2min.md",
    output_audio_path: str = "omnibci/submission/demo_narration.mp3",
    voice_id: str = "pNInz6obpgDQGcFmaJgB"  # Default 'Adam' narrator
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("[ElevenLabs] No ELEVENLABS_API_KEY detected in environment or .env.")
        print("  To generate voiceover, run:")
        print("  $env:ELEVENLABS_API_KEY='your-key'; python omnibci/submission/elevenlabs_narration.py")
        return False

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all text inside blockquotes (voiceover lines)
    quotes = re.findall(r'> "(.*?)"', content, re.DOTALL)
    full_narration = " ".join([q.replace("\n", " ").strip() for q in quotes])
    
    print(f"[ElevenLabs] Extracted {len(full_narration.split())} words for narration.")
    print(f"[ElevenLabs] Synthesizing speech using voice ID: {voice_id}...")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": full_narration,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            audio_data = resp.read()
            with open(output_audio_path, "wb") as f_out:
                f_out.write(audio_data)
        print(f"[ElevenLabs] SUCCESS: Voiceover generated at {output_audio_path}")
        return True
    except Exception as e:
        print(f"[ElevenLabs] Error during synthesis: {e}")
        return False

if __name__ == "__main__":
    generate_voiceover()
