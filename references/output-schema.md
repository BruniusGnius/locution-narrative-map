# Locution Narrative Map — Output Schema

## Core distinction

Keep these layers separate:

- **Transcription context**: optional user-provided hints about topic, language, vocabulary and expected speakers.
- **Speaker evidence (`Sxx`)**: diarization segments that estimate who speaks when; identity is not inferred.
- **Acoustic phrase (`Pxx`)**: a speech interval inferred from pauses or rhythm. It has no semantic claim.
- **Narrative beat (`Bxx`)**: the smallest meaningful unit whose idea, narrative function, intention, or emotional direction is coherent.
- A beat may contain several acoustic phrases, and a long acoustic phrase may contain more than one beat.

## Timecode

Use `HH:MM:SS.mmm` for all precise outputs. Start from the actual media timeline. Do not fabricate millisecond precision when timing is estimated; mark `timing_quality` as `estimated`.

## Context fields

When context is provided or inferred reliably, preserve:

- `general_topic`
- `content_type`
- `primary_language`
- `secondary_languages`
- `glossary`
- `expected_speakers`
- `preserve_foreign_terms`

Context is a transcription aid, not evidence that a term was actually spoken.

## Speaker fields

Speaker diarization output should preserve:

- `status`: `detected`, `unavailable`, or `disabled`
- `count`
- `count_source`: e.g. `diarization`, `user_hint+diarization`, `user_hint`, `unknown`
- `speaker_id`: stable `S01`, `S02`, ...
- `speaker_label`: human label `Voz 1`, `Voz 2`, ...
- timed speaker segments with `start` and `end`

Never assign names, gender, age, profession or identity from voice alone.

## Phrase fields

Each timed acoustic phrase should carry:

- `phrase_id`: sequential `P01`, `P02`, ...
- `tc_in`, `tc_out`
- `duration`
- `text`: exact or minimally cleaned transcript wording aligned to that phrase
- `word_count` when word-level timestamps are available
- `speaker_id` and `speaker_label` when diarization evidence is available
- `timing_quality`: `source`, `aligned`, or `estimated` when relevant

This phrase layer is additive. It does not replace the beat layer.

## Beat fields

Each beat should carry:

- `beat_id`: sequential `B01`, `B02`, ...
- `tc_in`, `tc_out`
- `duration`
- `voiceover`: exact or minimally cleaned source wording
- `speaker_ids` when speaker evidence materially matters
- `core_idea`: one-sentence semantic summary
- `narrative_function`: best-fit role in the local/global arc
- `intention`: what the locution is trying to make the audience understand, feel, or do
- `emotion`: dominant emotional direction, not a diagnosis of the speaker
- `intensity`: integer 1–10, relative within this specific piece
- `transition_reason`: why the next beat deserves a new boundary
- `timing_quality`: `source`, `aligned`, or `estimated`

## Narrative function vocabulary

Use the smallest useful vocabulary and adapt when needed:

`hook`, `premise`, `context`, `problem`, `stakes`, `escalation`, `question`, `contrast`, `evidence`, `reframe`, `insight`, `reveal`, `solution`, `transformation`, `invitation`, `cta`, `closing`.

Do not force every piece into all categories.

## Required human-readable output

### 1. Piece summary and transcription context

Give the basic review context: media duration, detected/declared language, phrase count, beat count, speaker count/status and timing quality. Then show the context used for transcription when any was supplied, for example:

```markdown
## Contexto de transcripción

- Tipo: Podcast
- Tema general: Técnicas de prompting e ingeniería de contexto
- Idioma principal: Español
- Otros idiomas/términos: Inglés
- Hablantes esperados: 2
- Vocabulario esperado: prompting, context engineering, RAG, few-shot
```

Do not imply that glossary terms definitely occur in the recording.

### 2. Timed phrase reading

Place this section **before the narrative analysis table** whenever timed speech evidence exists. It is a human QA layer for listening and transcript verification.

Render each phrase as a readable block, not as a dense table:

```markdown
## Lectura temporizada de la locución

### P01 · Voz 1 · 00:00:00.000 → 00:00:04.056 · 4.06 s
Bienvenidos a una nueva forma de aprender.

### P02 · Voz 2 · 00:00:04.849 → 00:00:10.216 · 5.37 s
Imagina que tus alumnos pudieran convertir una idea en algo real.
```

If speaker evidence is unavailable, omit the voice label rather than guessing.

Requirements:

- preserve `Pxx` order;
- show start, end and duration;
- show speaker only when supported by diarization/user mapping;
- preserve exact or minimally cleaned wording;
- do not add semantic labels here;
- if transcription confidence is insufficient, flag the phrase instead of inventing text.

### 3. Arc summary

Give 3–6 bullets describing the overall progression and identify the strongest turn/climax when one exists.

### 4. Narrative timeline

| Beat | Timecode | Speaker | Voiceover | Core idea | Function | Intention / emotion | Intensity | Boundary reason |
|---|---|---|---|---|---|---|---:|---|

### 5. Rhythm and timing notes

Call out meaningful pauses, acceleration, compression, breathing room, speaker changes, and any mismatch between acoustic phrasing and semantic beats.

### 6. Downstream handoff

End with a compact machine-readable block or table preserving at least `beat_id`, `tc_in`, `tc_out`, `core_idea`, `narrative_function`, `emotion`, and `intensity`. Preserve the context, speaker layer and phrase layer separately so later visual-direction/storyboard skills can trace beats back to exact spoken phrases and speaker changes. This is the contract for later visual-direction/storyboard skills.
