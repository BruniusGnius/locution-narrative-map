# Locution Narrative Map

Skill plug-and-play para convertir una locución en un **mapa narrativo temporal** listo para alimentar dirección visual, moodboard, storyboard y guion técnico.

## Para el creativo

No necesitas instalar Python, FFmpeg, Whisper ni configurar un entorno.

Dale este repositorio a Codex o Claude Code y dile:

> Instala esta skill y déjala lista para usar. Después analiza mi locución con Locution Narrative Map. No me pidas instalar dependencias manualmente.

Después comparte o indica tu archivo MP3, WAV, M4A, AAC o FLAC.

Para mejorar la precisión puedes darle contexto en lenguaje natural, por ejemplo:

> Es un podcast sobre técnicas de prompting e ingeniería de contexto. Está principalmente en español, usa algunos términos en inglés y hablan 2 personas. Pueden aparecer palabras como prompting, context engineering, RAG y few-shot.

No es obligatorio llenar un formulario: si no sabes esos datos, dile `continúa` y la Skill intentará detectarlos.

La primera ejecución puede descargar un runtime local gratuito y un modelo de transcripción. Las siguientes reutilizan esa instalación.

## Usar dentro de Obsidian

Si trabajas con un Vault de Obsidian, puedes usarlo como workspace creativo: deja la locucion dentro del Vault, abre Codex o Claude Code sobre esa carpeta y pide el analisis. Los resultados pueden guardarse como Markdown dentro del propio Vault, mientras el runtime y los modelos permanecen fuera.

Consulta **[OBSIDIAN.md](OBSIDIAN.md)** para la guia paso a paso de Claude Code y Codex.

## Qué entrega

- contexto de transcripción guardado para saber qué pistas se utilizaron;
- transcripción con timestamps por palabra cuando el backend lo soporta;
- detección local de cantidad de voces y cambios de hablante cuando la diarización está disponible;
- una **lectura temporizada de la locución** con `P01`, `P02`, ... mostrando voz, inicio, fin, duración y texto para revisar fácilmente la transcripción mientras escuchas;
- frases acústicas `P01`, `P02`, ... basadas en pausas y ritmo;
- beats narrativos `B01`, `B02`, ... definidos por significado;
- arco narrativo global;
- intención, emoción e intensidad relativa por beat;
- un `handoff.json` estable para futuras skills de moodboard, storyboard y guion técnico.

## Privacidad y costo

La transcripción se ejecuta localmente con herramientas gratuitas. No requiere una API de transcripción de pago.

Los modelos y dependencias pesadas **no viven en este repositorio**: se descargan al equipo del usuario en el primer uso.

## Guardar el runtime en un SSD externo

El agente puede establecer `LNM_HOME` antes de la primera instalación. Por ejemplo:

```bash
export LNM_HOME="/Volumes/CREATIVE_AI/locution-narrative-map-runtime"
```

El creativo no necesita hacer esto manualmente: basta con decirle al agente dónde quiere guardar los archivos pesados.

## Para agentes

- Codex / agentes compatibles: leer primero `AGENTS.md` y `SKILL.md`.
- Claude Code: leer primero `CLAUDE.md` y `SKILL.md`.
- Procedimiento genérico: `INSTALL.md`.

El runtime se prepara automáticamente con:

- macOS/Linux: `bash scripts/bootstrap.sh`
- Windows: `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`

Luego el agente debe usar `scripts/run.* prepare` y convertir la evidencia generada en el mapa narrativo siguiendo `references/output-schema.md`.

## Estado

Esta versión prioriza una experiencia sin setup manual. El backend se selecciona automáticamente:

- Apple Silicon: MLX Whisper.
- Otros sistemas compatibles: faster-whisper en CPU como fallback conservador.

La skill nunca debe inventar una transcripción ni una identidad de hablante. Si la diarización no está disponible, el resto del análisis continúa y el dato de voces se marca como desconocido.
