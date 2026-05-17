# music-ai-workflow

Pipeline local para criação musical com voz própria usando ACE-Step 1.5 + Demucs.  
Organizado como notebooks Jupyter reprodutíveis no VS Code.

## Estrutura do projeto

```
music-ai-workflow/
│
├── notebooks/
│   ├── 00_setup.ipynb          # instalação do ambiente, verificação de GPU
│   ├── 01_separar_stems.ipynb  # Demucs: voz → voz isolada + instrumental
│   ├── 02_vocal2bgm.ipynb      # ACE-Step: voz isolada → música completa
│   ├── 03_cover_audio2audio.ipynb  # ACE-Step: gravação → cover em novo estilo
│   ├── 04_stemgen.ipynb        # ACE-Step: gerar stem de instrumento específico
│   └── 05_lora_finetune.ipynb  # ACE-Step: treinar LoRA com suas músicas
│
├── audio/
│   ├── raw/          # suas gravações originais (voz + violão)
│   ├── stems/        # stems separados pelo Demucs
│   └── output/       # músicas geradas pelo ACE-Step
│
├── models/
│   └── lora/         # checkpoints LoRA treinados
│
├── scripts/
│   ├── utils.py      # funções auxiliares compartilhadas
│   └── check_env.py  # verificação rápida do ambiente
│
├── docs/
│   └── sessoes.md    # log manual de sessões e resultados
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.11
- GPU NVIDIA com CUDA 12.x (mínimo 4 GB VRAM para geração; 12 GB para LoRA)
- VS Code com extensões: Python, Jupyter
- Git

## Instalação rápida

```bash
# 1. Clonar este repositório
git clone https://github.com/SEU_USUARIO/music-ai-workflow.git
cd music-ai-workflow

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# ou: .venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Clonar o ACE-Step 1.5 (na pasta raiz do projeto)
git clone https://github.com/ace-step/ACE-Step-1.5.git

# 5. Verificar ambiente
python scripts/check_env.py
```

## Uso

Abra o VS Code na pasta do projeto e execute os notebooks em ordem.  
Cada notebook é independente e documentado — você pode retomar de qualquer ponto.

## Portabilidade

Para transferir para outro computador:
1. `git push` deste repositório (sem os arquivos de áudio — ver `.gitignore`)
2. No novo computador: `git clone` + `pip install -r requirements.txt`
3. Copie a pasta `audio/raw/` manualmente (ou via pendrive/nuvem)
4. Os modelos LoRA em `models/lora/` também precisam ser copiados manualmente

## Notas sobre autoria

Os arquivos de áudio originais e gerados **não são commitados no Git** por padrão
(ver `.gitignore`). Mantenha backups separados em nuvem (Google Drive, Dropbox etc.)
ou num disco externo.
