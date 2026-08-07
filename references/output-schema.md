# Locution Narrative Map — Output Schema

## Core distinction

Keep these layers separate:

- **Acoustic phrase (`Pxx`)**: a speech interval inferred from pauses or rhythm. It has no semantic claim.
- **Narrative beat (`Bxx`)**: the smallest meaningful unit whose idea, narrative function, intention, or emotional direction is coherent.
- A beat may contain several acoustic phrases, and a long acoustic phrase may contain more than one beat.

## Timecode

Use `HH:MM:SS.mmm` for all precise outputs. Start from the actual media timeline. Do not fabricate millisecond precision when timing is estimated; mark `timing_quality` as `estimated`.

## Beat fields

Each beat should carry:

- `beat_id`: sequential `B01`, `B02`, ...
- `tc_in`, `tc_out`
- `duration`
- `voiceover`: exact or minimally cleaned source wording
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

### 1. Arc summary

Give 3–6 bullets describing the overall progression and identify the strongest turn/climax when one exists.

### 2. Narrative timeline

| Beat | Timecode | Voiceover | Core idea | Function | Intention / emotion | Intensity | Boundary reason |
|---|---|---|---|---|---|---:|---|

### 3. Rhythm and timing notes

Call out meaningful pauses, acceleration, compression, breathing room, and any mismatch between acoustic phrasing and semantic beats.

### 4. Downstream handoff

End with a compact machine-readable block or table preserving at least `beat_id`, `tc_in`, `tc_out`, `core_idea`, `narrative_function`, `emotion`, and `intensity`. This is the contract for later visual-direction/storyboard skills.
