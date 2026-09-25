from __future__ import annotations
import argparse
import json
from pathlib import Path

from engine.ingestion import extract_document
from engine.pptx_exporter import export_pptx
from engine.validator import validate_presentation
from engine.ollama_client import generate_presentation, generate_presentation_from_document

ROOT = Path(__file__).parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_skill(*parts: str) -> str:
    return (ROOT / "skills" / Path(*parts) / "SKILL.md").read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="AI Presentation Automation")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--demo", action="store_true", help="Generate deterministic demo PPTX")
    source.add_argument("--topic", type=str, help="Generate a presentation with a local Ollama model")
    source.add_argument("--pdf", type=str, help="Generate a presentation from a PDF using Ollama")
    source.add_argument("--docx", type=str, help="Generate a presentation from a DOCX using Ollama")
    parser.add_argument("--model", type=str, default="llama3.2")
    parser.add_argument("--slides", type=int, default=8)
    parser.add_argument("--output", type=str, default="output/presentation.pptx")
    args = parser.parse_args()

    if args.slides < 1:
        parser.error("--slides must be at least 1")

    if args.demo:
        data = load_json(ROOT / "examples" / "demo_presentation.json")
        out = ROOT / "output" / "demo-presentation.pptx"
    elif args.topic:
        presentation_skill = read_skill("presentation")
        data = generate_presentation(args.topic, args.model, args.slides, presentation_skill)
        out = ROOT / args.output
    elif args.pdf or args.docx:
        input_path = args.pdf or args.docx
        document = extract_document(input_path)
        document_skill = read_skill("document")
        presentation_skill = read_skill("presentation")
        print(
            f"Extracted {len(document.text):,} characters from {document.path.name} "
            f"({document.kind.upper()})."
        )
        data = generate_presentation_from_document(
            document_text=document.text,
            source_name=document.path.name,
            model=args.model,
            slide_count=args.slides,
            document_skill=document_skill,
            presentation_skill=presentation_skill,
        )
        out = ROOT / args.output
    else:
        parser.error("Use --demo, --topic, --pdf or --docx")

    validate_presentation(data, ROOT / "schemas" / "presentation.schema.json")
    export_pptx(data, out)
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
