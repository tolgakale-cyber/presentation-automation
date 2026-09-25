# AI Presentation & Document Automation

Research, documents and structured inputs are transformed into presentation-ready JSON and PowerPoint decks through a modular skill + orchestration architecture.

## Architecture

```text
Topic / URL / PDF / DOCX / Notes
              |
              v
        Ingestion Layer
              |
              v
      Research / Synthesis
              |
              v
      Presentation Skill
              |
              v
       Slide Architect
              |
              v
        QA / Critic
              |
              v
       Presentation JSON
              |
              v
          PPTX Export
```

## What is included?

- Modular AI skills
- Research → presentation workflow
- Document → presentation workflow
- Presentation QA workflow
- JSON presentation contract
- Working PPTX renderer
- Demo deck generator
- Local-first Ollama orchestration starter
- GitHub Pages project page

## Quick demo

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python app.py --demo
```

Output:

```text
output/demo-presentation.pptx
```

The demo does not require an AI API.

## Local AI mode

Install Ollama separately, pull a model, then:

```bash
python app.py --topic "AI agents in enterprise workflows" --model llama3.2
```

The local model is asked to return presentation JSON following the project's schema. The result is validated and rendered to PPTX.

## Important

This repository is an automation foundation and working renderer, not a claim that every input format is fully parsed in v1. PDF/DOCX ingestion adapters are represented in the workflow and are intended as the next extension.

## Project structure

```text
skills/       AI behavior specifications
workflows/    orchestration definitions
engine/       Python automation / rendering code
schemas/      structured presentation contract
examples/     deterministic demo input
docs/         GitHub Pages showcase
output/       generated files (ignored by git)
```

## License

MIT
