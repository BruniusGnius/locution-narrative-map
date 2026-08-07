# Agent instructions — Locution Narrative Map

This repository is a self-contained creative-agent skill. Treat the end user as non-technical.

## Primary UX rule

The user should be able to say: "Install this skill and analyze my voiceover." Do not ask them to install Python, FFmpeg, Whisper, package managers, virtual environments, CUDA, MLX, or model files manually.

## Installation behavior

1. Read `SKILL.md`.
2. Register/copy the skill using the agent's supported skill mechanism if one exists.
3. Keep this repository intact; runtime dependencies belong outside the repository.
4. If the user asked for an external SSD, set `LNM_HOME` to that location before bootstrapping.
5. When audio transcription is first needed, run:
   - macOS/Linux: `bash scripts/bootstrap.sh`
   - Windows: `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`
6. Run `scripts/run.* doctor` if setup appears unhealthy.
7. Prepare audio with `scripts/run.* prepare <audio> --output <dir>`.
8. Read `handoff.json` and `references/output-schema.md`.
9. Perform the semantic beat analysis yourself from the transcript/timing evidence.

## Interaction policy

Hide package-manager logs and stack traces unless the user asks for them. Summarize setup as a user-relevant event such as "Preparing the local transcription component for first use." If setup fails, run the doctor before asking the user for technical action.

## Trust rules

- Use only the bundled bootstrap scripts for runtime installation.
- Do not add paid transcription APIs as a requirement.
- Never fabricate words, timestamps, beats, or emotional evidence.
- Acoustic phrase IDs `Pxx` are evidence boundaries, not semantic beat IDs `Bxx`.
- Stop at the narrative-map layer unless the user explicitly invokes a later creative workflow.

## Transcription context

Before processing audio, accept optional natural-language context: general topic, primary/secondary languages, expected vocabulary/names and known speaker count. If missing, offer one compact optional question and allow the user to say `continúa`. Pass these hints to the preparation pipeline; never force a glossary term unsupported by the audio. Attempt speaker diarization automatically and preserve `Voz 1`, `Voz 2`, ... labels only when supported by evidence.
