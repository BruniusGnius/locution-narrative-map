# Claude Code instructions — Locution Narrative Map

Read `SKILL.md` before operating this repository.

The intended user is a creative, not a developer. Installation and troubleshooting must be agent-operated.

## When asked to install or use this skill

1. Preserve the repository structure.
2. If Claude Code has a supported reusable skill/instruction mechanism, register this repository's `SKILL.md` accordingly. Otherwise keep the repository available and follow `SKILL.md` directly.
3. Do not ask the user to manually install Python, FFmpeg, Whisper, Homebrew, pip, uv, virtual environments, MLX, CUDA, or model files.
4. If the user wants dependencies on an external SSD, set `LNM_HOME` to that path before setup.
5. On first transcription, bootstrap automatically:
   - macOS/Linux: `bash scripts/bootstrap.sh`
   - Windows: `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`
6. If setup fails, run the bundled doctor before surfacing the blocker.
7. Prepare the audio with the bundled `run` script.
8. Use generated transcript/timestamps plus `references/output-schema.md` to create semantic beats and the narrative arc.

Do not expose low-level logs by default. Never invent a transcript when transcription is unavailable.
