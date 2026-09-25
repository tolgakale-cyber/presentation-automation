# Document → Presentation

```text
PDF / DOCX
    ↓
Document extraction adapter
    ↓
Document Skill
    ↓
Presentation Skill
    ↓
Presentation JSON
    ↓
JSON Schema validation
    ↓
PPTX renderer
```

Implemented in v1.1 for text-based PDF and DOCX inputs. PDF extraction uses `pypdf`; DOCX extraction uses `python-docx`. Scanned/image-only PDFs require OCR and are not supported yet. URL ingestion and the automatic QA revision loop remain separate next steps.
