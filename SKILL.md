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
Read `references/narrative-analysis.md` before interpreting the global arc or semantic beats.

## Workflow

1. Identify the input source.
2. Collect optional transcription context without blocking the user.
3. If audio requires transcription, ensure the local runtime is healthy.
4. Run the preparation pipeline to create transcript + acoustic timing + speaker evidence.
5. Build the human-reviewable timed phrase reading (`Pxx`) from the transcript and acoustic evidence.
6. Separate acoustic phrases (`Pxx`) from semantic beats (`Bxx`).
7. Build the narrative arc and annotate each beat.
8. Enrich the same beats with the deep narrative-analysis layer; do not replace the existing beat analysis.
9. Validate time coverage, semantic relationships and boundaries.
10. Return the human-readable map and stable downstream handoff.

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

This produces `context.json`, a transcript, word timestamps, `speaker-map.json`, acoustic phrase candidates, `phrase-map.json` and `handoff.json`. `phrase-map.json` attaches readable transcript text to each `Pxx` time range so a human can verify the transcription against the audio before relying on the narrative analysis. Use those files as evidence for semantic analysis.

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


## 2. Optional transcription context

Before transcribing an audio file, use context as a quality hint when the user provides it. Do not require technical metadata. If useful context is missing, ask at most one compact optional intake message covering:

- general topic or subject of the audio;
- primary language and any secondary languages/foreign terms;
- names, brands, acronyms or technical vocabulary likely to appear;
- expected number of speakers, when the user knows it.

Make it easy to skip: the user may answer in one line or say `continúa` / `no sé`. Never block transcription because these details are absent.

Example user context:

```text
Es un podcast sobre técnicas de prompting e ingeniería de contexto.
Está principalmente en español, pero usa términos en inglés.
Pueden aparecer: prompting, context engineering, system prompt, RAG y few-shot.
Hablan 2 personas.
```

Use this context only as a hypothesis. Never force glossary terms that are not supported by the audio. Preserve foreign terms, names and acronyms in their original form when the acoustic evidence supports them. Save the context used as `context.json` and include it in `handoff.json`.

### Speaker detection

Attempt local speaker diarization when audio is available. If the user provides the expected speaker count, use it as a clustering hint, not as permission to invent identities. If the user does not know the count, attempt automatic detection.

- Label unknown voices as `Voz 1`, `Voz 2`, ... and keep stable speaker IDs `S01`, `S02`, ... .
- Do not infer real names, jobs, gender, age or identity from voice alone.
- If the user later provides identities or roles, map those labels explicitly.
- If diarization is unavailable or unreliable, mark speaker data as unavailable/unknown and continue the rest of the narrative map.
- Save diarization evidence as `speaker-map.json`.

## 3. Runtime privacy and storage

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

## 4. Evidence layers

Keep three layers distinct:

- **Word timing**: transcription evidence produced by the local Whisper backend.
- **Acoustic phrase (`Pxx`)**: speech interval inferred from pauses/rhythm; no semantic claim.
- **Narrative beat (`Bxx`)**: coherent semantic unit defined by idea/function/intention/emotion.

A beat may contain multiple phrases. A long phrase may contain multiple beats.

## 5. Timed phrase reading

Before the narrative table, always include a human-readable **Lectura temporizada de la locución** when timed speech evidence exists. Preserve all existing narrative outputs; this is an additional review layer.

For each `Pxx`, show:

- phrase ID;
- start time;
- end time;
- duration;
- exact or minimally cleaned transcript text;
- speaker label when diarization evidence is available.

Use one phrase block per `Pxx` rather than a dense table so a human can read it like a timed script while listening. Apply this exact information hierarchy in the human-readable Markdown:

```markdown
#### P03 — Voz 1

- **Inicio** `00:00:11.026` **Final** `00:00:15.136`
- **Duración** `4.110 s`

> #### *“Que no solo aprendieran tecnología, sino que aprendieran a crear con ella.”*

---
```

Keep start and final timecodes on the same bullet, duration on its own bullet, and the spoken phrase in a blockquote with level-4 heading emphasis plus italics. Separate every phrase block with `---`. Preserve millisecond precision in this review layer; the visual hierarchy, not information removal, is what makes it readable.

Do not treat `Pxx` as narrative meaning. Its purpose is transcript verification, timing review and traceability. If a phrase has no reliably aligned words, preserve the time range and mark its text as unavailable rather than guessing.

## 6. Semantic beats

Create a new beat when one or more materially changes:

- central idea or proposition;
- narrative function;
- speaker intention toward the audience;
- emotional direction;
- argument/reveal/contrast state;
- action requested from the audience.

Prefer meaningful boundaries over fixed-duration slices. Assign stable IDs `B01`, `B02`, ... in timeline order.

## 7. Narrative arc

Infer the global progression first, then classify beats relative to it. Useful roles include hook, premise, context, problem, stakes, escalation, contrast, evidence, reframe, insight, reveal, solution, transformation, invitation, CTA and closing.

Do not force a three-act or advertising structure when the material uses another form.

Also produce a deeper global reading using `references/narrative-analysis.md`. Preserve the existing arc summary, strongest turn and climax; add, rather than substitute:

- audience starting position;
- central narrative question or governing tension;
- transformation path;
- argument architecture;
- emotional architecture;
- credibility architecture when relevant;
- intended audience after-state / resolution.

## 8. Deep narrative reading

Preserve every existing `Bxx` field. Then enrich each beat using the deep-analysis framework in `references/narrative-analysis.md`. Adopt the senior audiovisual narrative analyst / script editor / rhetoric and intention strategist role defined there. Analyze the actual narrative form rather than forcing an advertising or three-act template.

Before writing the enriched fields, distinguish four things: literal content, relational change from adjacent beats, audience-state change, and structural purpose. Then write only supported conclusions.

Look for relational signals such as:

- active audience question or expectation;
- narrative movement from one state to another;
- intended perception shift;
- tension opened, sustained or released;
- subtext;
- persuasive job;
- rhetorical device;
- energy direction;
- bridge from the previous beat;
- bridge to the next beat;
- visual opportunity for downstream creative work.

Keep the enriched fields non-redundant: `audience_question` is the unresolved mental question; `narrative_movement` is the structural transition; `perception_shift` is the audience belief/frame change; `tension_release` tracks unresolved pressure; `subtext` captures implication; `persuasive_intent` names the strategic job; `rhetorical_device` names the mechanism; `energy_direction` tracks momentum; bridges explain adjacency; and `visual_opportunity` is only a narrative handoff clue. If two fields say essentially the same thing, rewrite or omit the weaker one.

Use the controlled energy vocabulary from `references/narrative-analysis.md`. Treat audio pauses, pacing and speaker changes as supporting evidence rather than automatic meaning. When evidence is ambiguous, qualify the interpretation instead of inventing certainty.

Do not fill these mechanically. Use `null`, `none material`, or omit an optional field when the source does not support a meaningful interpretation. Prefer specific before/after relationships over generic labels.

## 9. Intention, emotion and intensity

For each beat:

- state the communicative intention;
- name the dominant emotional direction concisely;
- score intensity 1–10 relative to this piece.

Use vocal delivery as supporting evidence, but distinguish vocal energy from narrative importance.

## 10. Validation

Before answering, verify:

- the timed phrase reading appears before the narrative beat table when timing evidence exists;
- each `Pxx` preserves start, end, duration and transcript text when available;
- speaker labels are shown only when diarization evidence supports them;
- context/glossary terms are treated as hints rather than corrections without acoustic support;
- every beat has textual evidence;
- timecodes do not overlap unintentionally;
- voiced sections are not omitted without explanation;
- beat boundaries have semantic reasons, not only silence boundaries;
- `Pxx` IDs are never presented as `Bxx` IDs;
- estimated timing is labeled;
- global arc agrees with beat-level functions;
- deep-analysis fields add relational insight rather than paraphrasing the voiceover;
- audience-question, perception-shift, tension and subtext claims remain evidence-based;
- visual-opportunity hints stop before storyboard/shot design;
- downstream handoff preserves stable IDs, time ranges and all original beat fields alongside enriched fields.

## 11. Stop at the narrative-map layer

Do not automatically create a moodboard, storyboard, camera plan, shot list or technical script. This skill establishes the temporal/narrative foundation for those later creative stages.
