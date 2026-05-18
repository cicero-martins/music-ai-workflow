"""
scripts/utils.py
Funções auxiliares compartilhadas entre todos os notebooks do projeto.
"""

from pathlib import Path
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

def carregar_audio(caminho: str | Path) -> tuple[np.ndarray, int]:
    """Carrega um arquivo WAV. Retorna (array, sample_rate)."""
    audio, sr = sf.read(str(caminho))
    print(f"✓ carregado: {Path(caminho).name}  |  {sr} Hz  |  {audio.shape}  |  {len(audio)/sr:.1f}s")
    return audio, sr


def salvar_audio(audio: np.ndarray, sr: int, caminho: str | Path) -> Path:
    """Salva array de áudio como WAV."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(caminho), audio, sr)
    tamanho_mb = caminho.stat().st_size / 1e6
    print(f"✓ salvo: {caminho.name}  |  {tamanho_mb:.1f} MB")
    return caminho


def listar_audio(pasta: str | Path = None) -> list[Path]:
    """Lista arquivos de áudio WAV/MP3 em uma pasta."""
    pasta = Path(pasta) if pasta else AUDIO_RAW
    arquivos = sorted(pasta.glob("*.wav")) + sorted(pasta.glob("*.mp3"))
    if not arquivos:
        print(f"  (nenhum arquivo encontrado em {pasta})")
    for a in arquivos:
        audio, sr = sf.read(str(a))
        print(f"  {a.name:40s}  {sr} Hz  {len(audio)/sr:.1f}s")
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
