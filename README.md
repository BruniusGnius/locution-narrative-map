# Locution Narrative Map

Skill plug-and-play para convertir una locución en un **mapa narrativo temporal** listo para alimentar dirección visual, moodboard, storyboard y guion técnico.

## Para el creativo

No necesitas instalar Python, FFmpeg, Whisper ni configurar un entorno.

Dale este repositorio a Codex o Claude Code y dile:

> Instala esta skill y déjala lista para usar. Después analiza mi locución con Locution Narrative Map. No me pidas instalar dependencias manualmente.

Después comparte o indica tu archivo MP3, WAV, M4A, AAC o FLAC.

La primera ejecución puede descargar un runtime local gratuito y un modelo de transcripción. Las siguientes reutilizan esa instalación.

## Usar dentro de Obsidian

Si trabajas con un Vault de Obsidian, puedes usarlo como workspace creativo: deja la locucion dentro del Vault, abre Codex o Claude Code sobre esa carpeta y pide el analisis. Los resultados pueden guardarse como Markdown dentro del propio Vault, mientras el runtime y los modelos permanecen fuera.

Consulta **[OBSIDIAN.md](OBSIDIAN.md)** para la guia paso a paso de Claude Code y Codex.

## Qué entrega

- transcripción con timestamps por palabra cuando el backend lo soporta;
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

La skill nunca debe inventar una transcripción si la capa de speech-to-text no está disponible.
