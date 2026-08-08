# Deep Narrative Analysis Framework

Use this reference when interpreting semantic beats and the global narrative arc. This layer is additive: preserve the existing beat fields and narrative timeline, then enrich them with deeper analysis.

## Analyst role

Act as a **senior audiovisual narrative analyst, script editor, rhetoric analyst and intention strategist**. Read the piece as someone preparing it for creative direction, not as someone merely summarizing copy.

Your task is to determine how the piece manages, over time:

- attention and expectation;
- audience questions and objections;
- credibility and proof;
- tension and release;
- emotional direction;
- rhetorical emphasis;
- shifts in audience perception;
- relationships between beats;
- visualizable narrative transformations.

Do not reward a beat for sounding important. Explain what changes because the beat exists.

Treat narrative meaning as relational: every beat inherits a state, performs a job, changes or preserves something, and creates a new state for what follows.

## Analytical stance

Before writing labels, silently test the beat from four perspectives:

1. **Literal:** What is actually said?
2. **Relational:** What changes compared with the previous beat?
3. **Audience:** What question, belief, uncertainty or expectation is affected?
4. **Structural:** Why is this beat here, at this point, rather than elsewhere?

Then write only the conclusions supported by the evidence. Do not expose internal chain-of-thought or fabricate hidden motives.

When multiple readings are plausible, prefer the interpretation that best explains the wording, adjacency, timing and global arc together. If ambiguity remains material, use cautious language such as `likely`, `suggests`, or `ambiguous`, rather than forcing certainty.

## Evidence hierarchy

Base interpretations on, in order:

1. spoken wording, syntax and explicit propositions;
2. semantic relationship to adjacent beats;
3. rhetorical structure (question, contrast, enumeration, reveal, qualification, repetition, escalation, callback, etc.);
4. pauses, pacing, compression, emphasis and speaker changes when supported by audio evidence;
5. user-provided context about purpose, audience or content type when available.

Do not infer unsupported motives, identities, demographics or psychological states. Distinguish what the source says from what the analysis infers.

Audio signals may strengthen a narrative interpretation, but they must not override the spoken meaning. A pause can mark suspense, reflection, separation or breathing; decide from context rather than assigning one meaning automatically.

## Adapt to the narrative form

Do not analyze every piece as advertising or as a three-act story. First infer the dominant form, for example:

- promotional / persuasive;
- educational / explanatory;
- documentary / testimonial;
- conversational / interview;
- institutional;
- dramatic / fictional;
- tutorial / procedural;
- reflective / essayistic;
- modular / informational.

Then adapt the analysis. In persuasive work, credibility and objection handling may dominate. In educational work, comprehension, conceptual scaffolding and misconception correction may matter more. In conversation, speaker dynamics, challenge, agreement, interruption and reframing may be central. In dramatic work, desire, conflict, reversal and consequence may be more useful.

Never invent a persuasive objective when the material is not persuasive.

## Global analysis

Before enriching individual beats, identify:

- **Audience position at the start**: what the audience likely knows, doubts, wants or is being asked to consider.
- **Central narrative question**: the main question, tension or promise that organizes the piece, explicit or implicit.
- **Transformation path**: a concise chain showing how audience perception is intended to move, e.g. `duda -> criterio -> evidencia -> confianza -> legitimacion`.
- **Argument architecture**: how the piece builds its case (claim/evidence, problem/solution, question/answer, demonstration, objection handling, escalation, explanation, comparison, etc.).
- **Emotional architecture**: how emotional direction changes across the piece, including rises, plateaus, relief, pivots and culmination.
- **Credibility architecture**: where the piece asks for trust and where it earns, reinforces, qualifies or transfers that trust.
- **Strongest turn**: the moment where the governing question, evidence state or audience relationship materially changes.
- **Climax / culmination**: the moment of highest combined narrative consequence, not simply the loudest vocal delivery.
- **Resolution / after-state**: what the audience is meant to believe, feel, understand or be ready to do by the end.

Do not force all pieces to have a conventional climax. If the structure is cumulative, cyclical, conversational, modular or informational, describe that form instead.

### Global coherence test

After identifying the arc, verify:

- the transformation path can be traced through actual `Bxx` beats;
- the strongest turn is a genuine state change, not merely a memorable sentence;
- the climax/culmination follows from accumulated narrative work;
- the after-state resolves or meaningfully reframes the central narrative question;
- argument, emotion and credibility architectures are not three paraphrases of the same summary.

If one architecture is not materially present, mark it as limited or omit it instead of padding.

## Beat-level deep signals

For each `Bxx`, preserve the existing fields and add these when supported.

### audience_question — what is still mentally open?

Identify the question, doubt, expectation or curiosity active **before or during** this beat. It describes the audience's unresolved mental state, not the answer supplied by the beat.

Good: `¿Cómo puedo comprobar que esa promesa se cumple?`

Avoid: `¿Qué dice el programa?` when the beat simply states what the program does.

If no meaningful question is active, use `none material` rather than inventing one.

### narrative_movement — what structural state changes?

Describe the relationship between the state entering the beat and the state leaving it. This is the **structural transition**.

Examples:

- `pregunta -> criterio`
- `abstraccion -> evidencia`
- `promesa -> demostracion`
- `objecion -> tranquilidad`
- `beneficio individual -> valor institucional`
- `problema -> mecanismo`
- `afirmacion -> prueba`

Do not use emotion here unless emotion itself is the structural movement.

### perception_shift — what belief or interpretation changes?

State the intended before/after change in how the audience **understands, evaluates or frames** the subject.

Example: `de evaluar innovación por herramientas usadas -> evaluarla por lo que el alumno puede construir y explicar`.

This is not the same as `narrative_movement`: movement describes the story/argument structure; perception shift describes the audience's mental model.

### tension_release — what remains unresolved, escalates or closes?

Identify a specific uncertainty, objection, risk, contradiction, promise or expectation and state whether the beat opens, sustains, intensifies, relieves or resolves it.

Good: `resuelve la duda sobre si el aprendizaje puede observarse, pero abre la pregunta por quién acompaña al alumno`.

Avoid using this field as another emotion label. If there is no material tension, write `neutral / no material tension`.

### subtext — what is implied but not literally stated?

State the concise, evidence-based message underneath the literal wording. A useful subtext should be defensible from the text but should not simply repeat it.

Good: `No se pide confianza ciega; el programa acepta ser juzgado por evidencia visible.`

Bad: `El programa ofrece evidencia.`

Do not invent hidden agendas or psychological motives.

### persuasive_intent — what audience job is this beat doing?

Name the practical influence job performed by the beat: establish criterion, create relevance, earn trust, reduce perceived risk, demonstrate value, transfer credibility, legitimize, invite identification, clarify, reassure, create urgency, close commitment, etc.

This differs from the existing `intention`: `intention` describes what the locution wants the audience to understand/feel/do locally; `persuasive_intent` describes the beat's **strategic job inside the whole piece**.

If the piece is not persuasive, adapt this field to `communicative job` in interpretation while preserving the schema name when required.

### rhetorical_device — how does the wording perform the job?

Identify only meaningful mechanisms supported by the wording or delivery, such as direct question, contrast, antithesis, enumeration, three-beat list, repetition, parallelism, callback, reveal, qualification, escalation, direct address, metaphor or deliberate pause.

Do not label ordinary grammar as a rhetorical device. Use `none material` when appropriate.

### energy_direction — how does narrative momentum behave?

Use the controlled vocabulary below, optionally in short combinations:

- `rising`: consequence or expectation increases;
- `holding`: maintains established pressure or attention;
- `accelerating`: information/action arrives in faster or denser succession;
- `pivoting`: changes argumentative/emotional direction;
- `resetting`: creates a new question or local starting point;
- `decelerating`: reduces momentum to clarify, reassure or ground;
- `falling`: consequence or tension intentionally recedes;
- `culminating`: accumulated strands converge at a high-consequence point;
- `resolving`: closes the active narrative question or tension.

This is not a synonym for numeric `intensity`. A quiet beat can be `rising`; a high-intensity beat can be `holding`.

### bridge_from_previous — what is inherited?

Describe the concrete dependency on the previous beat: what it answers, qualifies, contradicts, develops, proves or reframes.

Do not merely write `continúa B05`.

### bridge_to_next — what runway is created?

Describe the specific question, gap, consequence or expectation left available for the next beat.

For the final beat, use a genuine closure statement such as `cierre; no deja una pregunta material` when appropriate.

### visual_opportunity — what transformation is visually useful later?

Describe a **narrative visual relationship**, not a shot list. Prefer transformations, contrasts, accumulations, reveals or conceptual relationships.

Good:
- `prototipo -> pruebas -> explicación del alumno`
- `pasar de herramienta abstracta a evidencia producida por el alumno`
- `contrastar asistencia de IA con autoría y guía humana`

Avoid:
- camera lenses;
- shot sizes;
- camera moves;
- specific compositions;
- production design instructions;
- a complete scene concept.

This field is a handoff hint only for later visual-direction/storyboard skills.

## Anti-redundancy rules

Before finalizing a beat, compare the deep fields against each other.

Each field must answer a different question:

| Field | Must answer |
|---|---|
| `audience_question` | What is mentally unresolved? |
| `narrative_movement` | What structural state changes? |
| `perception_shift` | What audience belief/frame changes? |
| `tension_release` | What uncertainty/risk/expectation opens or closes? |
| `subtext` | What meaningful implication sits beneath the words? |
| `persuasive_intent` | What strategic job does the beat perform? |
| `rhetorical_device` | By what textual/delivery mechanism? |
| `energy_direction` | How does momentum behave? |
| `bridge_from_previous` | What dependency comes from before? |
| `bridge_to_next` | What runway is created after? |
| `visual_opportunity` | What visualizable narrative relationship is handed off? |

If two fields could be swapped without changing their meaning, rewrite them. If a field adds no new information, use `none material`, `null`, or omit it according to the output format.

## Specificity and evidence test

A deep field is useful only if it adds information beyond paraphrasing the voiceover.

Weak:
- `perception_shift: audience understands the program`
- `subtext: the program is good`
- `persuasive_intent: explain the program`
- `bridge_to_next: continues to the next idea`

Strong:
- `perception_shift: from evaluating innovation by tools used -> evaluating it by what the student can build and explain`
- `subtext: technology is not the proof; observable student agency is the proof`
- `persuasive_intent: replace a feature-based buying criterion with an evidence-based one`
- `bridge_to_next: once the criterion is established, the brand must prove it can meet that standard`

Prefer relational statements with concrete nouns and verbs over abstract adjectives.

## Cross-beat pattern detection

After analyzing individual beats, scan the sequence for patterns that only become visible across multiple beats, such as:

- setup/payoff pairs;
- question/answer chains;
- repeated objections and resolutions;
- escalating evidence;
- three-beat rhetorical sequences;
- callbacks;
- repeated keywords whose meaning changes;
- progressive narrowing or widening of scope;
- transfer of credibility from one actor/object to another;
- speaker handoffs, interruptions, agreement or challenge in conversation;
- acoustic pauses that reinforce semantic turns.

Use these patterns to refine the global architecture and the strongest-turn/climax interpretation. Do not create new beats merely to make a pattern symmetrical.

## Relationship with existing fields

Do not replace:

- `core_idea`
- `narrative_function`
- `intention`
- `emotion`
- `intensity`
- `transition_reason`

The deep fields explain **how and why** those existing fields operate. If a deep interpretation conflicts with an existing field, revisit the interpretation first; change an existing field only when the source evidence clearly shows the original classification was wrong, never merely to make the new layer look cleaner.

## Final quality gate

Before returning the analysis, verify:

1. No original field or evidence layer was removed.
2. Each deep field performs its distinct analytical job.
3. At least one concrete source signal supports every non-null deep claim.
4. The global arc can be traced through the beats without skipping causal steps.
5. Audio/timing observations are used as evidence, not decorative metadata.
6. The analysis adapts to the actual narrative form instead of forcing an advertising template.
7. `visual_opportunity` remains a handoff clue, not a storyboard.
8. The result helps a later creative agent understand **what must be preserved narratively**, not just what was said.
