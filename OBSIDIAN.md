# Usar Locution Narrative Map con Obsidian

Puedes usar **Locution Narrative Map** dentro de un Vault de Obsidian sin convertir Obsidian en un entorno tecnico. El Vault sigue siendo tu espacio creativo; Codex o Claude Code hacen el trabajo tecnico sobre la misma carpeta.

## Experiencia recomendada

La idea es que el creativo solo necesite:

1. Abrir su Vault de Obsidian.
2. Guardar o arrastrar una locucion dentro del Vault.
3. Abrir Codex o Claude Code usando la carpeta del Vault como proyecto.
4. Pedirle al agente que instale Locution Narrative Map y analice el audio.
5. Volver a Obsidian para leer el mapa narrativo generado.

No hace falta instalar Python, FFmpeg, Whisper ni modelos manualmente.

## Estructura sugerida del Vault

```text
Mi-Vault-Creativo/
├── 01_Inbox/
│   └── mi-locucion.mp3
├── 02_Mapas-Narrativos/
├── 03_Moodboards/
├── 04_Storyboards/
├── 05_Guiones/
└── ...
```

No es obligatorio usar estos nombres. Son solo una estructura recomendada para mantener continuidad entre futuras skills creativas.

Los archivos pesados del runtime y los modelos de transcripcion deben permanecer fuera del Vault. Asi el Vault sigue siendo ligero, portable y facil de sincronizar.

## Opcion A: usar Claude Code

### 1. Abre el Vault como proyecto

En Terminal, entra a la carpeta del Vault y abre Claude Code:

```bash
cd "/ruta/a/Mi-Vault-Creativo"
claude
```

Si prefieres no escribir comandos, pide ayuda al agente o abre una terminal directamente en la carpeta del Vault desde Finder/Explorer cuando tu sistema lo permita.

### 2. Pidele instalar la skill

Puedes pegar este mensaje:

```text
Instala Locution Narrative Map desde https://github.com/BruniusGnius/locution-narrative-map y dejala lista para usarse dentro de este Vault. No me pidas instalar Python, FFmpeg, Whisper ni dependencias manualmente. Guarda los archivos pesados fuera del Vault. Cuando termines, analiza la locucion que esta en 01_Inbox y guarda el resultado legible en 02_Mapas-Narrativos.
```

Claude Code puede usar skills de proyecto ubicadas en `.claude/skills/<skill-name>/SKILL.md`. Si el agente elige esa forma de instalacion, la skill queda asociada al Vault/proyecto.

Ejemplo:

```text
Mi-Vault-Creativo/
├── .claude/
│   └── skills/
│       └── locution-narrative-map/
│           ├── SKILL.md
│           ├── scripts/
│           └── references/
├── 01_Inbox/
└── 02_Mapas-Narrativos/
```

La carpeta `.claude` puede permanecer oculta para el creativo.

### 3. Uso diario

Despues de la primera instalacion, deberia bastar con algo como:

```text
Analiza la nueva locucion de 01_Inbox con Locution Narrative Map y guarda el mapa narrativo en 02_Mapas-Narrativos.
```

## Opcion B: usar Codex

### 1. Abre Codex sobre la carpeta del Vault

Usa la carpeta del Vault como workspace/proyecto de Codex.

### 2. Pidele instalar la skill desde GitHub

Pega este mensaje:

```text
Instala esta skill desde https://github.com/BruniusGnius/locution-narrative-map y dejala lista para usar en este Vault de Obsidian. No me pidas instalar dependencias manualmente. Guarda el runtime y los modelos fuera del Vault. Despues analiza la locucion que esta en 01_Inbox y guarda el mapa narrativo en 02_Mapas-Narrativos.
```

Codex debe leer `AGENTS.md`, `SKILL.md` e `INSTALL.md` del repositorio y encargarse del runtime local.

### 3. Uso diario

```text
Analiza la locucion nueva que deje en 01_Inbox y crea su mapa narrativo en 02_Mapas-Narrativos.
```

## Que deberia aparecer en Obsidian

El resultado principal debe ser un archivo Markdown legible directamente desde Obsidian, por ejemplo:

```text
02_Mapas-Narrativos/
└── mi-locucion/
    ├── narrative-map.md
    ├── transcript.srt
    ├── transcript.json
    └── handoff.json
```

`narrative-map.md` es el archivo pensado para el creativo. Los archivos JSON y SRT sirven como evidencia y como puente hacia futuras skills de moodboard, storyboard y guion tecnico.

## Runtime y SSD externo

Si quieres que modelos y dependencias pesadas vivan en un SSD externo, dile al agente algo como:

```text
Guarda el runtime y los modelos de Locution Narrative Map en mi SSD externo llamado CREATIVE_AI. No guardes dependencias pesadas dentro del Vault.
```

El agente debe configurar `LNM_HOME` en esa ubicacion antes de instalar el runtime.

## Recomendacion para un Vault compartido

Si varias personas comparten o sincronizan el mismo Vault:

- comparte las notas, audios y resultados que realmente formen parte del proyecto;
- evita sincronizar el runtime, modelos de Whisper, caches o entornos de Python;
- cada computadora debe preparar su propio runtime local la primera vez;
- si usas `.claude/skills/` dentro del Vault, decide conscientemente si esa carpeta tambien debe sincronizarse con el equipo.

## Solucion de problemas

El creativo no deberia diagnosticar dependencias manualmente. Si algo falla, pide:

```text
Locution Narrative Map dejo de funcionar. Ejecuta su doctor, repara automaticamente lo que puedas y vuelve a intentar el analisis. Solo preguntame si necesitas una decision que no puedas resolver por tu cuenta.
```

El agente debe usar el `doctor` incluido en la skill antes de mostrar errores tecnicos o pedir acciones manuales.
