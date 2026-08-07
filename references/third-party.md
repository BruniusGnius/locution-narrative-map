# Third-party runtime components

The skill repository does not bundle large model files. First-use setup installs/downloads components locally.

- uv — cross-platform Python/runtime bootstrapper. Project: https://github.com/astral-sh/uv
- imageio-ffmpeg — Python wrapper whose common-platform wheels include an FFmpeg executable. Project: https://github.com/imageio/imageio-ffmpeg
- mlx-whisper — Whisper implementation for Apple Silicon via MLX. Project: https://github.com/ml-explore/mlx-examples/tree/main/whisper
- faster-whisper — CTranslate2-based Whisper implementation used as the cross-platform CPU-first fallback. Project: https://github.com/SYSTRAN/faster-whisper
- Whisper model family — speech-recognition models originally released by OpenAI. Project: https://github.com/openai/whisper

Before public distribution, the repository maintainer should preserve applicable license notices and review dependency/model licenses for the chosen pinned versions.
