# Deep Narrative Analysis Framework

Use this reference when interpreting semantic beats and the global narrative arc. This layer is additive: preserve the existing beat fields and narrative timeline, then enrich them with deeper analysis.

## Analyst role

Act as an audiovisual narrative analyst, script editor and intention strategist. Do not merely summarize what is said or assign a generic label. Determine how the piece manages attention, expectation, credibility, tension, emotion and audience perception over time.

Treat narrative meaning as relational: every beat inherits something from the previous beat, changes the audience state, and prepares something for the next beat.

## Evidence hierarchy

Base interpretations on, in order:

1. spoken wording and syntax;
2. semantic relationship to adjacent beats;
3. rhetorical structure (question, contrast, enumeration, reveal, qualification, repetition, escalation, etc.);
4. pauses, pacing, emphasis and speaker changes;
5. user-provided context about purpose/audience when available.

Do not infer unsupported motives, identities or psychological states. Distinguish what the text says from what the analysis infers.

## Global analysis

Before enriching individual beats, identify:

- **Audience position at the start**: what the audience likely knows, doubts, wants or is being asked to consider.
- **Central narrative question**: the main question, tension or promise that organizes the piece, explicit or implicit.
- **Transformation path**: a concise chain showing how audience perception is intended to move, e.g. `duda -> criterio -> evidencia -> confianza -> legitimacion`.
- **Argument architecture**: how the piece builds its case (claim/evidence, problem/solution, question/answer, demonstration, objection handling, escalation, etc.).
- **Emotional architecture**: how emotional direction changes across the piece, including rises, plateaus, relief and culmination.
- **Credibility architecture**: where the piece asks for trust and where it earns, reinforces or transfers that trust.
- **Strongest turn**: the moment where the governing question, evidence state or audience relationship materially changes.
- **Climax / culmination**: the moment of highest combined narrative consequence, not simply the loudest vocal delivery.
- **Resolution / after-state**: what the audience is meant to believe, feel or be ready to do by the end.

Do not force all pieces to have a conventional climax. If the structure is cumulative, cyclical, conversational, modular or informational, describe that form instead.

## Beat-level deep signals

For each `Bxx`, preserve the existing fields and add these when supported:

### audience_question
What question, doubt, expectation or curiosity is active in the audience at this moment? It may be explicit or inferred from the immediately surrounding text.

### narrative_movement
Describe the actual movement, not just a category. Examples:

- `pregunta -> respuesta`
- `abstraccion -> evidencia`
- `promesa -> demostracion`
- `objecion -> tranquilidad`
- `beneficio individual -> valor institucional`
- `problema -> mecanismo`
- `afirmacion -> prueba`

Use a short phrase in natural language when arrows are not sufficient.

### perception_shift
State the intended before/after change in audience perception. Example: `de "innovacion" como discurso de marca -> innovacion como resultado verificable`.

### tension_release
Identify what tension, uncertainty, objection or expectation is opened, sustained, increased, relieved or resolved. If none is present, say `neutral / no material tension` rather than inventing one.

### subtext
State the implied message beneath the literal wording. Keep it evidence-based and concise. Example: `No tienes que confiar en la tecnologia por si sola; puedes exigir evidencia del aprendizaje.`

### persuasive_intent
Name what persuasive job the beat performs: establish criterion, create relevance, earn trust, reduce perceived risk, demonstrate value, transfer credibility, create urgency, invite identification, legitimize, close commitment, etc.

### rhetorical_device
Identify relevant devices such as question, contrast, enumeration, three-beat list, repetition, antithesis, reveal, qualification, escalation, direct address, metaphor or callback. Use `none material` if no device matters.

### energy_direction
Describe narrative energy as `rising`, `falling`, `holding`, `resetting`, `pivoting`, `accelerating`, `decelerating`, or a short combination. This is separate from the existing numeric intensity.

### bridge_from_previous
What does this beat inherit, answer, contradict or advance from the previous beat?

### bridge_to_next
What question, expectation, gap or conceptual runway does it create for the next beat?

### visual_opportunity
Describe the kind of visual transformation the beat naturally invites without creating a storyboard. Examples: `move from abstract interface imagery to tangible student artifact`, `three-step evidence progression`, `contrast human guidance with AI assistance`.

This field is a handoff hint only. Do not specify camera lenses, shots or full scene design in this skill.

## Deep-analysis quality test

A deep field is useful only if it adds information beyond paraphrasing the voiceover.

Weak:
- `perception_shift: audience understands the program`
- `subtext: the program is good`

Strong:
- `perception_shift: from evaluating innovation by tools used -> evaluating it by what the student can build and explain`
- `subtext: technology is not the proof; observable student agency is the proof`

Prefer specific relational statements over abstract adjectives.

## Relationship with existing fields

Do not replace:

- `core_idea`
- `narrative_function`
- `intention`
- `emotion`
- `intensity`
- `transition_reason`

The deep fields explain **how and why** those existing fields operate.
