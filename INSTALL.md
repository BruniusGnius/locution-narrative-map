# Agent-first installation

This repository is designed to be installed and operated by a coding agent, not manually by a creative user.

## Suggested user prompt

```text
Install Locution Narrative Map from this repository and make it ready to use.
Do not ask me to install Python, FFmpeg, package managers, Whisper or model files manually.
Use only free local transcription tools. If something fails, run the built-in doctor before asking me to troubleshoot.
```

If the user wants large files on an external SSD, set `LNM_HOME` to that location before bootstrapping.

## Agent procedure

1. Read `SKILL.md` and the relevant agent instruction file (`AGENTS.md` or `CLAUDE.md`).
2. Register/copy the skill using the coding agent's supported skill mechanism when available.
3. Keep runtime dependencies outside the repository.
4. Do not bootstrap transcription dependencies until audio transcription is needed, unless the user explicitly asks to make everything ready now.
5. First audio use:
   - macOS/Linux: `bash scripts/bootstrap.sh`
   - Windows: `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`
6. Verify with `scripts/run.* doctor`.
7. Prepare audio:
   - macOS/Linux: `bash scripts/run.sh prepare "<audio>" --output "<output-dir>"`
   - Windows: `powershell -ExecutionPolicy Bypass -File scripts/run.ps1 prepare "<audio>" --output "<output-dir>"`
8. Read `handoff.json` plus `references/output-schema.md`.
9. Create semantic narrative beats from the evidence. Do not equate acoustic phrases with beats.

## Expected creative-user interaction

```text
Preparing the local transcription component for first use...
Ready. Analyzing the voiceover...
```

Do not expose package-manager output or stack traces unless the user requests technical details.


## Obsidian vaults

When the user wants to work from an Obsidian Vault, treat the Vault as the creative workspace and keep heavy runtime dependencies outside it. Read `OBSIDIAN.md` for the recommended folder structure and user-facing flow.

Prefer generating the human-readable `narrative-map.md` inside the Vault and keeping model caches, Python runtimes and transcription dependencies under `LNM_HOME` outside the Vault.

## Transcription context

Before processing audio, accept optional natural-language context: general topic, primary/secondary languages, expected vocabulary/names and known speaker count. If missing, offer one compact optional question and allow the user to say `continúa`. Pass these hints to the preparation pipeline; never force a glossary term unsupported by the audio. Attempt speaker diarization automatically and preserve `Voz 1`, `Voz 2`, ... labels only when supported by evidence.
