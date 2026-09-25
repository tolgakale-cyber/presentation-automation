from __future__ import annotations
import argparse
import json
from pathlib import Path

from engine.pptx_exporter import export_pptx
from engine.validator import validate_presentation
from engine.ollama_client import generate_presentation

ROOT = Path(__file__).parent

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser(description="AI Presentation Automation")
    parser.add_argument("--demo", action="store_true", help="Generate deterministic demo PPTX")
    parser.add_argument("--topic", type=str, help="Generate a presentation with a local Ollama model")
    parser.add_argument("--model", type=str, default="llama3.2")
    parser.add_argument("--slides", type=int, default=8)
    parser.add_argument("--output", type=str, default="output/presentation.pptx")
    args = parser.parse_args()

    if args.demo:
        data = load_json(ROOT / "examples" / "demo_presentation.json")
        out = ROOT / "output" / "demo-presentation.pptx"
    elif args.topic:
        skill = (ROOT / "skills" / "presentation" / "SKILL.md").read_text(encoding="utf-8")
        data = generate_presentation(args.topic, args.model, args.slides, skill)
        out = ROOT / args.output
    else:
        parser.error("Use --demo or --topic")

    validate_presentation(data, ROOT / "schemas" / "presentation.schema.json")
    export_pptx(data, out)
    print(f"Created: {out}")

if __name__ == "__main__":
    main()
