"""
OmniBCI PowerPoint Presentation Generator
Creates pitch_slides.pptx (16:9 Widescreen) with all 9 high-definition slides
and attaches the verbatim 3-minute pitch script to the Speaker Notes of each slide.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches

BASE_DIR = Path("C:/Users/delor/Downloads/Hack-nation/October 27")
SUBMISSION_DIR = BASE_DIR / "omnibci" / "submission"
SLIDES_DIR = SUBMISSION_DIR / "slides"
DOCS_DIR = BASE_DIR / "docs"

slides_data = [
    {
        "num": 1,
        "file": "slide_01_title.png",
        "title": "Slide 1: Title & System Overview (Banner Aesthetic)",
        "timing": "0:00 - 0:20 (20 Seconds)",
        "cue": "Opening Hook · Present with confidence and authority",
        "script": (
            "[TIMING: 0:00 - 0:20 | 58 WORDS]\n\n"
            "\"Welcome everyone. I am Mario De Lorenzo, and this is OmniBCI Discovery Lab—an autonomous agentic platform built for Challenge 03.\n\n"
            "In motor rehabilitation after stroke, patients need Brain-Computer Interfaces that decode intent reliably without lengthy calibration.\n\n"
            "Today, discovering and deploying new neural architectures from literature takes months of manual re-engineering.\n\n"
            "OmniBCI solves this bottleneck, taking researchers from published literature to verified, benchmarked pipelines in minutes—not months.\""
        )
    },
    {
        "num": 2,
        "file": "slide_02_literature_bottleneck.png",
        "title": "Slide 2: The Research Bottleneck (Empirical Workload Data)",
        "timing": "0:20 - 0:40 (20 Seconds)",
        "cue": "Deliver the empirical data clearly and directly",
        "script": (
            "[TIMING: 0:20 - 0:40 | 66 WORDS]\n\n"
            "\"Examine where research time actually disappears. Workload surveys show neuroengineers dedicate up to forty-five percent of their working hours simply reading literature to identify relevant baselines.\n\n"
            "Once selected, industry benchmarks reveal that up to eighty percent of project time goes into plumbing: adapting channel montages, resolving library deprecations, and debugging unverified GitHub codebases. More than seventy percent of published repositories fail to run without manual intervention.\n\n"
            "On our 17-subject Kaggle benchmark, building a manual literature screening and cross-validation pipeline took 48 hours. OmniBCI completes that exact cycle in 70 seconds—a 40-fold acceleration.\""
        )
    },
    {
        "num": 3,
        "file": "slide_03_github_repo_omnigent.png",
        "title": "Slide 3: GitHub Repository & Databricks Omnigent Harness",
        "timing": "0:40 - 1:00 (20 Seconds)",
        "cue": "Highlight sandboxing, token caps, and clinical safety gates",
        "script": (
            "[TIMING: 0:40 - 1:00 | 59 WORDS]\n\n"
            "\"Inside our open repository, Databricks Omnigent orchestrates a six-stage meta-harness inside isolated Omnibox containers.\n\n"
            "Omnigent enforces strict financial and clinical policies. A twenty-five dollar token cap prevents runaway API expenditures, while a Clinical Safety Governor monitors real-time decoding metrics. Any architecture producing a resting false positive rate above ten percent is automatically flagged and rejected. In stroke rehabilitation, false triggers actuate robotic arms without patient intent, posing physical risks.\""
        )
    },
    {
        "num": 4,
        "file": "slide_04_literature_harvesting.png",
        "title": "Slide 4: Autonomous Literature Harvesting (Stage 1)",
        "timing": "1:00 - 1:20 (20 Seconds)",
        "cue": "Explain arXiv and OpenAlex harvesting without manual reading",
        "script": (
            "[TIMING: 1:00 - 1:20 | 56 WORDS]\n\n"
            "\"When a researcher states an objective, the Literature Harvester queries the arXiv and OpenAlex APIs directly. It scans motor intention preprints across computer science and quantitative biology, indexing peer-reviewed citations, author venues, and verified repository links.\n\n"
            "For our benchmark, the harvester retrieved He and Wu's Riemannian Euclidean Alignment, Duggento and De Lorenzo's Intertwined Neural Network, and Lawhern's EEGNet. It extracted mathematical formulations and tensor bounds directly from the text.\""
        )
    },
    {
        "num": 5,
        "file": "slide_05_paper2agent_mcp_import.png",
        "title": "Slide 5: Automatic GitHub Model Import into MCP Tools (Stage 2)",
        "timing": "1:20 - 1:40 (20 Seconds)",
        "cue": "Detail Paper2Agent AST extraction and montage harmonization",
        "script": (
            "[TIMING: 1:20 - 1:40 | 55 WORDS]\n\n"
            "\"Stanford's Paper2Agent synthesizer converts these cloned GitHub repositories into active Model Context Protocol tools.\n\n"
            "Instead of treating code as unverified text, the synthesizer inspects the abstract syntax tree, extracts canonical PyTorch model classes, and binds them to our target montage: eight wearable electrodes sampled at 250 Hertz. Each model becomes an isolated, unit-tested tool ready for execution.\""
        )
    },
    {
        "num": 6,
        "file": "slide_06_verified_primitives_vs_hallucination.png",
        "title": "Slide 6: Verified Execution Primitives vs. Conventional LLM Hallucinations",
        "timing": "1:40 - 2:00 (20 Seconds)",
        "cue": "Contrast raw LLM bugs against verified AST execution primitives",
        "script": (
            "[TIMING: 1:40 - 2:00 | 58 WORDS]\n\n"
            "\"This architectural choice separates OmniBCI from standard code-generation LLMs. Raw language models hallucinate non-existent PyTorch parameters, fail on spatial tensor dimensions, and frequently leak test data into training normalization.\n\n"
            "OmniBCI provides the reasoning agent with grounded execution primitives. Alignment matrices and covariance statistics are computed strictly on training subjects, ensuring verified numerical integrity and genuine clinical generalization.\""
        )
    },
    {
        "num": 7,
        "file": "slide_07_grounded_citation_popovers.png",
        "title": "Slide 7: Grounded Citation Popovers with Verbatim Excerpts",
        "timing": "2:00 - 2:20 (20 Seconds)",
        "cue": "Showcase verbatim PDF excerpts, section numbers, and DOIs",
        "script": (
            "[TIMING: 2:00 - 2:20 | 54 WORDS]\n\n"
            "\"In medical systems, traceability is essential. Every claim, tensor modification, or hyperparameter proposed by the co-pilot links directly to verbatim excerpts from the source paper.\n\n"
            "Clinicians hover over citation tags to view the original methodology paragraph, section number, and DOI link. Every reference is logged in a machine-readable literature evidence file, establishing an auditable trail for clinical verification.\""
        )
    },
    {
        "num": 8,
        "file": "slide_08_loso_validation_protocol.png",
        "title": "Slide 8: 17-Subject Leave-One-Subject-Out (LOSO) Validation Protocol",
        "timing": "2:20 - 2:40 (20 Seconds)",
        "cue": "Explain 17-fold cross-validation and EA-IntertwinedNet formulation",
        "script": (
            "[TIMING: 2:20 - 2:40 | 57 WORDS]\n\n"
            "\"The Experiment Runner executes a 17-fold Leave-One-Subject-Out validation across all 17 participants from the UK BCI Consortium benchmark.\n\n"
            "In the baseline notebook, unaligned deep models suffered from skull impedance drift, dropping to 52.5% accuracy on outlier subjects with a 13.8% resting false positive rate.\n\n"
            "The Co-Pilot diagnosed this domain collapse and formulated EA-IntertwinedNet: prepending Riemannian Euclidean Alignment whitening directly before time-distributed neural layers.\""
        )
    },
    {
        "num": 9,
        "file": "slide_09_kaggle_leaderboard_champion.png",
        "title": "Slide 9: Official Kaggle Leaderboard & EA-IntertwinedNet Champion",
        "timing": "2:40 - 3:00 (20 Seconds)",
        "cue": "Conclude strongly with 99.71%, kappa 0.994, 0.29% FPR, and Rank 1",
        "script": (
            "[TIMING: 2:40 - 3:00 | 62 WORDS]\n\n"
            "\"When approved, OmniBCI compiled a new Jupyter notebook and executed the pipeline.\n\n"
            "The resulting model delivered 99.71% accuracy with a Cohen's kappa of 0.994, cutting the resting false alarm rate to 0.29%. It recovered outlier subject Sub-03 from 55.0% to 96.67% and secured Rank 1 on the Kaggle benchmark.\n\n"
            "By converting passive scientific literature into active AI discovery tools, OmniBCI reduces a two-week engineering barrier to seventy seconds. Thank you.\""
        )
    }
]

def generate_powerpoint():
    print("[PowerPoint Generator] Initializing 16:9 Presentation...")
    prs = Presentation()
    
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout (typically layout 6 in default template)
    blank_layout = prs.slide_layouts[6]
    
    for idx, slide_info in enumerate(slides_data, 1):
        png_path = SLIDES_DIR / slide_info["file"]
        print(f"  Adding Slide {idx}/9: {slide_info['title']}...")
        
        slide = prs.slides.add_slide(blank_layout)
        
        # Add full-bleed 1080p slide image
        slide.shapes.add_picture(
            str(png_path),
            Inches(0), Inches(0),
            width=prs.slide_width,
            height=prs.slide_height
        )
        
        # Add speaker notes to slide
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        
        full_notes = (
            f"=== {slide_info['title']} ===\n"
            f"Timing: {slide_info['timing']}\n"
            f"Speaker Cue: {slide_info['cue']}\n"
            f"----------------------------------------\n\n"
            f"{slide_info['script']}\n"
        )
        tf.text = full_notes
        
    out_pptx = SUBMISSION_DIR / "pitch_slides.pptx"
    prs.save(str(out_pptx))
    print(f"\n[PowerPoint Generator] Successfully created: {out_pptx} ({out_pptx.stat().st_size:,} bytes)")
    
    # Also copy to docs/ for web access / GitHub release
    docs_pptx = DOCS_DIR / "pitch_slides.pptx"
    prs.save(str(docs_pptx))
    print(f"[PowerPoint Generator] Copied to: {docs_pptx}")

if __name__ == "__main__":
    generate_powerpoint()
