from __future__ import annotations

from flask import Flask, jsonify, request

from src.port_manifest import build_port_manifest
from src.query_engine import QueryEnginePort

app = Flask(__name__)


@app.get("/")
def home():
    """Vercel health endpoint with quick usage hints."""
    return jsonify(
        {
            "name": "claw-code",
            "status": "ok",
            "endpoints": {
                "/": "health + endpoint listing",
                "/api/summary": "render workspace summary",
                "/api/manifest": "render workspace manifest",
            },
        }
    )


@app.get("/api/summary")
def summary():
    summary_text = QueryEnginePort.from_workspace().render_summary()
    return jsonify({"summary": summary_text})


@app.get("/api/manifest")
def manifest():
    manifest = build_port_manifest()
    fmt = request.args.get("format", "json").lower()

    if fmt == "markdown":
        return jsonify({"manifest": manifest.to_markdown(), "format": "markdown"})

    return jsonify(
        {
            "format": "json",
            "modules": [
                {
                    "name": module.name,
                    "file_count": module.file_count,
                    "notes": module.notes,
                }
                for module in manifest.top_level_modules
            ],
            "backlog": manifest.backlog,
        }
    )
