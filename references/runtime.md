# Runtime and plug-and-play behavior

## Goal

The end user should be able to give an agent an audio file and ask for a narrative map without manually preparing a development environment.

## Runtime layout

The runtime is stored outside the creative project.

Default:
- macOS/Linux: `~/.local/share/locution-narrative-map`
- Windows: `%LOCALAPPDATA%\locution-narrative-map`

Override with `LNM_HOME`, including a path on an external SSD.

Expected contents:

```text
<LNM_HOME>/
  uv/             # private uv binary
  python/         # uv-managed Python
  cache/          # package/model caches
  venv/           # isolated Python environment
  bin/            # private ffmpeg shim/binary
  runtime.json    # detected backend and paths
```

## Dependency strategy

The bootstrapper uses `uv` because it has standalone installers for macOS/Linux/Windows and can download a managed Python when the machine does not already have one.

Base package:
- `imageio-ffmpeg==0.6.0` to provide a local FFmpeg executable without Homebrew/system installation.

Transcription backend:
- macOS + Apple Silicon: `mlx-whisper==0.4.3`, backend `mlx`, model profile optimized for Apple Silicon.
- other supported machines: `faster-whisper==1.2.1`, backend `faster-whisper`, CPU-first for reliability.

Do not install CUDA drivers, Homebrew, system Python, or global pip packages.

## Model policy

Models are downloaded on first transcription and cached locally. Do not commit models to the skill repository.

Default profile: `balanced`.

Suggested mapping:
- MLX `fast`: `mlx-community/whisper-small-mlx`
- MLX `balanced`: `mlx-community/whisper-turbo`
- MLX `quality`: `mlx-community/whisper-large-v3-mlx`
- faster-whisper `fast`: `small`
- faster-whisper `balanced`: `medium`
- faster-whisper `quality`: `large-v3`

If a configured MLX model is unavailable, prefer the package's supported Whisper Turbo model rather than failing permanently; record the actual model in output metadata.

## User experience rules

On first use, it is acceptable to tell the user that a free local transcription component/model is being prepared. Avoid exposing dependency names unless requested.

On subsequent uses, run silently unless there is a meaningful blocker.

If a command fails:
1. run `doctor`;
2. retry once when doctor identifies a repairable runtime issue;
3. report a concise blocker only if still unresolved.

Never instruct a non-technical user to interpret stack traces.

## Network behavior

Network access is needed during first-time runtime/package/model download. Once dependencies and a model are cached, transcription is local. The coding agent itself may still require network access according to its own product.

## Safety / trust

- Never execute arbitrary remote scripts except the official `uv` installer used by the bootstrapper.
- Pin Python package versions in the bootstrap script.
- Keep runtime modifications scoped to `LNM_HOME`.
- Do not modify shell profile files.
- Do not require administrator/sudo privileges.
