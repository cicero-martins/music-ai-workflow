"""
scripts/utils.py
Funções auxiliares compartilhadas entre todos os notebooks do projeto.
"""

from pathlib import Path
import io
import json
import subprocess
import soundfile as sf
import numpy as np
import datetime


# ── Caminhos padrão do projeto ────────────────────────────────────────────────

ROOT        = Path(__file__).parent.parent
AUDIO_RAW   = ROOT / "audio" / "raw"
AUDIO_STEMS = ROOT / "audio" / "stems"
AUDIO_OUT   = ROOT / "audio" / "output"
MODELS_LORA = ROOT / "models" / "lora"
DOCS        = ROOT / "docs"

for p in [AUDIO_RAW, AUDIO_STEMS, AUDIO_OUT, MODELS_LORA, DOCS]:
    p.mkdir(parents=True, exist_ok=True)


# ── Áudio ─────────────────────────────────────────────────────────────────────

_FORMATOS_NATIVOS = {".wav", ".flac", ".ogg", ".aiff", ".aif"}  # lidos por soundfile direto


def _ffmpeg_exe() -> str:
    """Caminho do binário ffmpeg empacotado pelo imageio-ffmpeg."""
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _decodificar_via_ffmpeg(caminho: Path) -> tuple[np.ndarray, int]:
    """Decodifica MP3/MP4/M4A/AAC/... para WAV em memória usando ffmpeg, depois lê com soundfile."""
    cmd = [_ffmpeg_exe(), "-loglevel", "error", "-i", str(caminho),
           "-f", "wav", "-acodec", "pcm_s16le", "-"]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    return sf.read(io.BytesIO(proc.stdout))


def _info_via_ffmpeg(caminho: Path) -> tuple[int, float]:
    """Retorna (sample_rate, duration_seconds) via ffmpeg para arquivos não-WAV."""
    cmd = [_ffmpeg_exe(), "-i", str(caminho), "-f", "null", "-"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    stderr = proc.stderr
    import re
    sr_match = re.search(r"(\d+)\s*Hz", stderr)
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", stderr)
    sr = int(sr_match.group(1)) if sr_match else 0
    if dur_match:
        h, m, s = dur_match.groups()
        dur = int(h) * 3600 + int(m) * 60 + float(s)
    else:
        dur = 0.0
    return sr, dur


def carregar_audio(caminho: str | Path) -> tuple[np.ndarray, int]:
    """Carrega áudio. WAV/FLAC/OGG via soundfile; MP3/MP4/M4A/AAC via ffmpeg em memória.

    Retorna (array, sample_rate). Array em (samples,) mono ou (samples, channels) estéreo.
    """
    caminho = Path(caminho)
    if caminho.suffix.lower() in _FORMATOS_NATIVOS:
        audio, sr = sf.read(str(caminho))
    else:
        audio, sr = _decodificar_via_ffmpeg(caminho)
    print(f"✓ carregado: {caminho.name}  |  {sr} Hz  |  {audio.shape}  |  {len(audio)/sr:.1f}s")
    return audio, sr


def garantir_wav(caminho: str | Path) -> Path:
    """Garante WAV no caminho. Se já for WAV, retorna direto. Se for MP3/MP4/M4A/AAC,
    converte para WAV ao lado (idempotente: pula se o WAV já existir).

    Útil antes de chamar ferramentas que só aceitam WAV (Demucs, torchaudio, ACE-Step CLI).
    """
    caminho = Path(caminho)
    if caminho.suffix.lower() == ".wav":
        return caminho
    wav_path = caminho.with_suffix(".wav")
    if wav_path.exists():
        print(f"  (WAV já existe: {wav_path.name})")
        return wav_path
    print(f"Convertendo {caminho.name} → {wav_path.name}...")
    cmd = [_ffmpeg_exe(), "-loglevel", "error", "-y",
           "-i", str(caminho), "-acodec", "pcm_s16le", str(wav_path)]
    subprocess.run(cmd, check=True)
    print(f"✓ Convertido: {wav_path.name}  ({wav_path.stat().st_size/1e6:.1f} MB)")
    return wav_path


def salvar_audio(audio: np.ndarray, sr: int, caminho: str | Path) -> Path:
    """Salva array de áudio como WAV."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(caminho), audio, sr)
    tamanho_mb = caminho.stat().st_size / 1e6
    print(f"✓ salvo: {caminho.name}  |  {tamanho_mb:.1f} MB")
    return caminho


def listar_audio(pasta: str | Path = None) -> list[Path]:
    """Lista arquivos de áudio em uma pasta. Suporta WAV/MP3/MP4/M4A/FLAC/OGG/AAC."""
    pasta = Path(pasta) if pasta else AUDIO_RAW
    extensoes = ("*.wav", "*.mp3", "*.mp4", "*.m4a", "*.flac", "*.ogg", "*.aac")
    arquivos = sorted({p for ext in extensoes for p in pasta.glob(ext)})
    if not arquivos:
        print(f"  (nenhum arquivo encontrado em {pasta})")
    for a in arquivos:
        if a.suffix.lower() in _FORMATOS_NATIVOS:
            info = sf.info(str(a))
            sr, dur = info.samplerate, info.duration
        else:
            sr, dur = _info_via_ffmpeg(a)
        print(f"  {a.name:40s}  {sr} Hz  {dur:.1f}s")
    return arquivos


# ── Log de sessão ─────────────────────────────────────────────────────────────

def log_sessao(titulo: str, notas: str = "", arquivo_log: str | Path = None) -> None:
    """
    Registra uma entrada no log de sessões (docs/sessoes.md).
    Chame ao final de cada notebook com um resumo do que foi feito.

    Exemplo:
        utils.log_sessao(
            titulo="Vocal2BGM — Samba 01",
            notas="Gravação original: samba_voz_violao.wav. "
                  "Guidance 7.5, prompt 'samba, pandeiro, baixo'. "
                  "Resultado bom, bateria um pouco mecânica. "
                  "Próximo teste: aumentar guidance para 8.5."
        )
    """
    arquivo_log = Path(arquivo_log) if arquivo_log else DOCS / "sessoes.md"
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    entrada = f"\n## {agora} — {titulo}\n\n{notas}\n\n---\n"

    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(entrada)

    print(f"✓ sessão registrada em {arquivo_log.name}: '{titulo}'")


# ── Verificação de GPU ────────────────────────────────────────────────────────

def verificar_gpu() -> str:
    """Verifica disponibilidade de GPU e retorna o device correto."""
    try:
        import torch
        if torch.cuda.is_available():
            nome = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✓ GPU disponível: {nome}  |  {vram:.1f} GB VRAM")
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            print("✓ GPU Apple MPS disponível")
            return "mps"
        else:
            print("⚠ Nenhuma GPU detectada — usando CPU (geração será lenta)")
            return "cpu"
    except ImportError:
        print("✗ PyTorch não instalado")
        return "cpu"


# ── Waveform simples no notebook ──────────────────────────────────────────────

def plotar_audio(audio: np.ndarray, sr: int, titulo: str = "Waveform") -> None:
    """Plota a forma de onda de um array de áudio."""
    try:
        import matplotlib.pyplot as plt
        tempo = np.linspace(0, len(audio) / sr, len(audio))
        if audio.ndim == 2:
            audio_plot = audio[:, 0]  # canal esquerdo
        else:
            audio_plot = audio
        plt.figure(figsize=(12, 2))
        plt.plot(tempo, audio_plot, linewidth=0.4, color="#534AB7")
        plt.title(titulo, fontsize=11)
        plt.xlabel("tempo (s)")
        plt.ylabel("amplitude")
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("matplotlib não instalado — instale para visualizar formas de onda")
