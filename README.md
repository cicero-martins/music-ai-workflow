# music-ai-workflow

Pipeline local para criação musical com voz própria usando **ACE-Step 1.5** + **Demucs**.  
Organizado como notebooks Jupyter reprodutíveis no VS Code.

## Estrutura do projeto

```
music-ai-workflow/
│
├── notebooks/
│   ├── 00_setup.ipynb              # ambiente, GPU, instalação
│   ├── 01_separar_stems.ipynb      # Demucs: gravação → vocals + no_vocals
│   ├── 02_vocal2bgm.ipynb          # ACE-Step: voz isolada → arranjo completo
│   ├── 03_cover_audio2audio.ipynb  # (planejado) ACE-Step: cover em novo estilo
│   ├── 04_stemgen.ipynb            # (planejado) ACE-Step: stem de instrumento
│   └── 05_lora_finetune.ipynb      # (planejado, cloud) treino LoRA com suas músicas
│
├── audio/
│   ├── raw/          # suas gravações originais (voz + violão)
│   ├── stems/        # stems separados pelo Demucs
│   └── output/       # músicas geradas pelo ACE-Step
│
├── models/
│   └── lora/         # checkpoints LoRA treinados (em cloud)
│
├── scripts/
│   ├── utils.py      # funções auxiliares compartilhadas
│   └── check_env.py  # verificação rápida do ambiente
│
├── docs/
│   └── sessoes.md    # log manual de sessões e resultados (gerado pelos notebooks)
│
├── ACE-Step-1.5/     # clonado pelo notebook 00 (não commitado)
├── .gitignore
├── requirements.txt
└── README.md
```

## Pré-requisitos

- **Python 3.11 ou 3.12** (ACE-Step 1.5 não suporta 3.13+)
- **GPU NVIDIA com CUDA ≥ 12.8** — ideal ≥ 8 GB VRAM (com `offload_to_cpu`); LoRA training pede ≥ 12 GB
- VS Code com extensões Python + Jupyter
- Git

## Instalação rápida (Windows)

```powershell
# 1. Clonar este repositório
git clone https://github.com/SEU_USUARIO/music-ai-workflow.git
cd music-ai-workflow

# 2. Criar conda env com Python 3.11
conda create -n music-ai python=3.11 pip -y
conda activate music-ai

# 3. Abrir VS Code apontando para a pasta
code .
```

Depois disso, abra `notebooks/00_setup.ipynb` no VS Code (com o kernel do env `music-ai`) e execute célula a célula. O notebook 00 instala PyTorch + CUDA 12.8, demais dependências, e clona o ACE-Step.

## Onde rodar cada notebook

| Notebook | Local | Motivo |
|---|---|---|
| 00–04 | Este PC (4 GB VRAM com offload) | Demucs e inferência ACE-Step rodam, embora lentos |
| 05 (LoRA) | **Cloud (Colab/RunPod)** | Treino exige ≥ 12 GB VRAM |

Os checkpoints LoRA treinados em cloud voltam para `models/lora/` via download manual.

## Uso

Abra o VS Code na pasta do projeto e execute os notebooks em ordem.  
Cada notebook é independente e documentado — você pode retomar de qualquer ponto.  
Cada sessão é registrada em `docs/sessoes.md` via `scripts/utils.log_sessao(...)`.

## Portabilidade

Para transferir para outro computador:
1. `git push` deste repositório (sem áudios — ver `.gitignore`)
2. No novo computador: `git clone` + `conda create -n music-ai python=3.11` + abrir `00_setup.ipynb`
3. Copie a pasta `audio/raw/` manualmente (ou via pendrive/nuvem)
4. Os modelos LoRA em `models/lora/` também precisam ser copiados manualmente

## Notas sobre autoria

Os arquivos de áudio originais e gerados **não são commitados no Git** por padrão
(ver `.gitignore`). Mantenha backups separados em nuvem (Google Drive, Dropbox etc.)
ou num disco externo.
