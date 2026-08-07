---
name: locution-narrative-map
description: "Turn voiceover/locution audio, subtitles, or transcripts into a reliable time-based narrative map for audiovisual preproduction. Use when an agent needs to transcribe narration locally with timestamps, identify semantic beats and the global story arc, map intention/emotion/intensity over time, or prepare the timed narrative foundation for later moodboards, visual direction, storyboards, shot lists, or technical scripts. Designed for plug-and-play use in coding agents: bootstrap a free local transcription runtime automatically when needed and never invent speech when transcription is unavailable."
---

# Locution Narrative Map

Build a trustworthy time-based narrative map from voiceover while hiding technical setup from non-technical users.

## Product behavior

Treat this as a creative tool, not a developer workflow.

- Do not ask the user to install Python, FFmpeg, MLX, Whisper, virtual environments, package managers, or model files manually.
- When local transcription is needed, bootstrap the private runtime automatically with the bundled installer.
- Explain only user-relevant events: first-time setup, model download, analysis progress, or a blocker that truly requires user action.
- Keep runtime files outside the user's creative project.
- Use only free/local transcription dependencies. Do not require a paid transcription API.
- Never invent a transcript.

Read `references/runtime.md` before bootstrapping or troubleshooting.
Read `references/output-schema.md` before producing the final narrative map.

## Workflow

1. Identify the input source.
2. If audio requires transcription, ensure the local runtime is healthy.
3. Run the preparation pipeline to create transcript + acoustic timing evidence.
4. Separate acoustic phrases (`Pxx`) from semantic beats (`Bxx`).
5. Build the narrative arc and annotate each beat.
6. Validate time coverage and boundaries.
7. Return the human-readable map and stable downstream handoff.

## 1. Input routing

### Audio file: MP3, WAV, M4A, AAC, FLAC or common media container

First ensure runtime:

macOS/Linux:
```bash
bash scripts/bootstrap.sh
```

Windows PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
```

Then run the complete evidence-preparation pipeline:

macOS/Linux:
```bash
bash scripts/run.sh prepare "<audio-file>" --output "<output-directory>"
```

Windows PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 prepare "<audio-file>" --output "<output-directory>"
```

This produces a transcript, word timestamps, acoustic phrase candidates and `handoff.json`. Use those files as evidence for semantic analysis.

If setup fails, run the doctor before asking the user to troubleshoot:

```bash
bash scripts/run.sh doctor
```

or on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 doctor
```

Only surface a technical blocker if the doctor cannot repair or explain it.

### SRT / VTT / timed transcript

Use supplied timestamps as primary evidence. Do not shift timing silently. Runtime setup is unnecessary.

### Plain transcript plus matching audio

Prefer the local preparation pipeline so word timing can be aligned from the audio. Preserve wording differences as transcription evidence rather than rewriting the source.

### Plain transcript only

Perform semantic beat analysis without pretending to know exact media timings. Mark timing as untimed/estimated.

## 2. Runtime privacy and storage

Default runtime location is private user storage, not the active project. Users can choose another location, including an external SSD, by setting `LNM_HOME` before installation.

Examples:

macOS/Linux:
```bash
export LNM_HOME="/Volumes/CREATIVE_AI/locution-narrative-map-runtime"
bash scripts/bootstrap.sh
```

Windows PowerShell:
```powershell
$env:LNM_HOME="E:\CreativeAI\locution-narrative-map-runtime"
.\scripts\bootstrap.ps1
```

Do not require the user to understand this option unless they explicitly care where the runtime is stored.

## 3. Evidence layers

Keep three layers distinct:

- **Word timing**: transcription evidence produced by the local Whisper backend.
- **Acoustic phrase (`Pxx`)**: speech interval inferred from pauses/rhythm; no semantic claim.
- **Narrative beat (`Bxx`)**: coherent semantic unit defined by idea/function/intention/emotion.

A beat may contain multiple phrases. A long phrase may contain multiple beats.

## 4. Semantic beats

Create a new beat when one or more materially changes:

- central idea or proposition;
- narrative function;
- speaker intention toward the audience;
- emotional direction;
- argument/reveal/contrast state;
- action requested from the audience.

Prefer meaningful boundaries over fixed-duration slices. Assign stable IDs `B01`, `B02`, ... in timeline order.

## 5. Narrative arc

Infer the global progression first, then classify beats relative to it. Useful roles include hook, premise, context, problem, stakes, escalation, contrast, evidence, reframe, insight, reveal, solution, transformation, invitation, CTA and closing.

Do not force a three-act or advertising structure when the material uses another form.

## 6. Intention, emotion and intensity

For each beat:

- state the communicative intention;
- name the dominant emotional direction concisely;
- score intensity 1–10 relative to this piece.

Use vocal delivery as supporting evidence, but distinguish vocal energy from narrative importance.

## 7. Validation

Before answering, verify:

- every beat has textual evidence;
- timecodes do not overlap unintentionally;
- voiced sections are not omitted without explanation;
- beat boundaries have semantic reasons, not only silence boundaries;
- `Pxx` IDs are never presented as `Bxx` IDs;
- estimated timing is labeled;
- global arc agrees with beat-level functions;
- downstream handoff preserves stable IDs and time ranges.

## 8. Stop at the narrative-map layer

Do not automatically create a moodboard, storyboard, camera plan, shot list or technical script. This skill establishes the temporal/narrative foundation for those later creative stages.
