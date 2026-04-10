#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

import fitz


PAGE_NUMBER_RE = re.compile(r"^\s*(page\s+)?\d+\s*$", re.IGNORECASE)
WHITESPACE_RE = re.compile(r"\s+")


def normalize_line(line: str) -> str:
    line = WHITESPACE_RE.sub(" ", line).strip()
    return line


def page_lines(text: str) -> list[str]:
    return [normalize_line(line) for line in text.splitlines() if normalize_line(line)]


def discover_repeated_lines(pages: list[list[str]], threshold: float = 0.3) -> set[str]:
    counter: Counter[str] = Counter()
    total_pages = len(pages)
    if total_pages == 0:
        return set()

    for lines in pages:
        edge_lines = set(lines[:2] + lines[-2:])
        for line in edge_lines:
            if len(line) >= 4:
                counter[line] += 1

    repeated = {
        line
        for line, count in counter.items()
        if count / total_pages >= threshold or PAGE_NUMBER_RE.match(line)
    }
    return repeated


def clean_page(lines: list[str], repeated_lines: set[str]) -> str:
    kept: list[str] = []
    for line in lines:
        if line in repeated_lines:
            continue
        if PAGE_NUMBER_RE.match(line):
            continue
        kept.append(line)
    return "\n".join(kept)


def extract_pdf(pdf_path: Path, language: str, document_type: str) -> dict:
    doc = fitz.open(pdf_path)
    raw_pages = [page_lines(page.get_text("text")) for page in doc]
    repeated_lines = discover_repeated_lines(raw_pages)

    cleaned_pages = [clean_page(lines, repeated_lines) for lines in raw_pages]
    cleaned_pages = [page for page in cleaned_pages if page.strip()]
    full_text = "\n\n".join(cleaned_pages)
    title = infer_title(pdf_path, raw_pages)

    return {
        "_id": slugify(pdf_path.stem),
        "title": title,
        "text": full_text,
        "metadata": {
            "source_file": pdf_path.name,
            "source_path": str(pdf_path),
            "language": language,
            "page_count": len(doc),
            "document_type": document_type,
        },
    }


def infer_title(pdf_path: Path, raw_pages: list[list[str]]) -> str:
    for page in raw_pages[:3]:
        for line in page[:8]:
            if 8 <= len(line) <= 180 and not PAGE_NUMBER_RE.match(line):
                return line
    return pdf_path.stem


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    return value.strip("-")


def iter_pdfs(input_paths: Iterable[Path]) -> Iterable[Path]:
    for path in input_paths:
        if path.is_dir():
            yield from sorted(path.rglob("*.pdf"))
        elif path.suffix.lower() == ".pdf":
            yield path


def write_jsonl(records: Iterable[dict], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert HAD/HAF-style nuclear safety PDFs into BEIR/FermiBench-style corpus.jsonl records."
    )
    parser.add_argument("--input-dir", type=Path, help="Directory containing PDF files.", default=None)
    parser.add_argument("--input-file", type=Path, action="append", default=[], help="Individual PDF file(s).")
    parser.add_argument("--output-file", type=Path, required=True, help="Destination JSONL file.")
    parser.add_argument("--lang", default="zh", help="Document language metadata.")
    parser.add_argument("--document-type", default="had", help="Document type metadata, e.g. had, haf, law.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_paths: list[Path] = list(args.input_file)
    if args.input_dir:
        input_paths.append(args.input_dir)
    if not input_paths:
        raise SystemExit("At least one of --input-dir or --input-file must be provided.")

    records = [
        extract_pdf(pdf_path=pdf, language=args.lang, document_type=args.document_type)
        for pdf in iter_pdfs(input_paths)
    ]
    write_jsonl(records, args.output_file)
    print(f"Wrote {len(records)} record(s) to {args.output_file}")


if __name__ == "__main__":
    main()

