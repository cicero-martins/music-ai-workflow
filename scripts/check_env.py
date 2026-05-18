"""
scripts/check_env.py
Verificação rápida do ambiente antes de começar.
Execute com: python scripts/check_env.py
"""

import sys
import subprocess

print("=" * 50)
print("Verificação do ambiente — music-ai-workflow")
print("=" * 50)

# Python — ACE-Step 1.5 exige >=3.11,<3.13
print(f"\n Python: {sys.version.split()[0]}")
ok = (3, 11) <= sys.version_info < (3, 13)
print(f"  {'✓' if ok else '✗'} versão {'ok (3.11–3.12)' if ok else 'ACE-Step exige 3.11 ou 3.12'}")

# Pacotes essenciais
pacotes = {
    "torch":      "PyTorch",
    "soundfile":  "soundfile",
    "demucs":     "Demucs",
    "librosa":    "librosa",
    "numpy":      "numpy",
    "jupyter":    "Jupyter",
}

print("\n Pacotes:")
for modulo, nome in pacotes.items():
    try:
        m = __import__(modulo)
        versao = getattr(m, "__version__", "?")
        print(f"  ✓ {nome:15s} {versao}")
    except ImportError:
        print(f"  ✗ {nome:15s} NÃO INSTALADO  →  pip install {modulo}")

# GPU
print("\n GPU:")
try:
    import torch
    if torch.cuda.is_available():
        nome = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  ✓ CUDA disponível: {nome}  ({vram:.1f} GB VRAM)")
        if vram < 8:
            print("  ⚠ menos de 8 GB — use offload_to_cpu=True no ACE-Step (geração lenta)")
        elif vram < 12:
            print("  ⚠ menos de 12 GB — LoRA fine-tune não disponível (use Colab/RunPod)")
        else:
            print("  ✓ VRAM suficiente para geração e LoRA")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("  ✓ Apple MPS disponível (Mac M-series)")
    else:
        print("  ⚠ Nenhuma GPU — CPU only (geração muito lenta)")
except ImportError:
    print("  ✗ PyTorch não instalado")

# ACE-Step
print("\n ACE-Step 1.5:")
try:
    import acestep
    print(f"  ✓ instalado")
except ImportError:
    print("  ✗ não instalado")
    print("    → git clone https://github.com/ace-step/ACE-Step-1.5.git")
    print("    → pip install -e ./ACE-Step-1.5")

# Git
print("\n Git:")
try:
    r = subprocess.run(["git", "--version"], capture_output=True, text=True)
    print(f"  ✓ {r.stdout.strip()}")
except FileNotFoundError:
    print("  ✗ Git não encontrado")

print("\n" + "=" * 50)
print("Execute os notebooks em ordem, começando por 00_setup.ipynb")
print("=" * 50)
