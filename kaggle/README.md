# Workflow Kaggle

Notebooks adaptados para rodar em **Kaggle Notebooks** (GPU T4 16 GB grátis, 30h/semana).
Use quando a GPU local for insuficiente — especialmente para LoRA training e gerações longas.

## Notebooks disponíveis

| Arquivo | Equivalente local | Status |
|---|---|---|
| [02_vocal2bgm_kaggle.ipynb](02_vocal2bgm_kaggle.ipynb) | [notebooks/02_vocal2bgm.ipynb](../notebooks/02_vocal2bgm.ipynb) | ✅ Pronto |
| `05_lora_finetune_kaggle.ipynb` | (a criar) | ⏳ Em breve |

## Como usar

### Pré-requisitos (apenas 1ª vez)

1. **Conta Kaggle** com **telefone verificado** (necessário pra liberar GPU)
   - https://www.kaggle.com/settings → Phone verification
2. **Dataset privado no Kaggle** com seu áudio de entrada
   - https://www.kaggle.com/datasets → "+ New Dataset"
   - Sugestão de nome: `music-ai-workflow-audio`
   - **Visibility: Private**
   - Upload do `vocals.wav` gerado pelo notebook 01 local

### Rodar um notebook

1. No Kaggle, clique em "+ Create" → **New Notebook**
2. Copie e cole o conteúdo do `.ipynb` deste diretório (ou faça upload do arquivo)
3. No painel direito da UI Kaggle:
   - **Settings**:
     - Accelerator: `GPU T4 x2` ou `GPU T4`
     - Internet: `On`
   - **Add data**: anexar seu dataset privado (`music-ai-workflow-audio`)
4. **Run All** ou execute célula a célula

### Primeira execução

- Setup (clone repos + pip install): ~3 min
- Download dos modelos ACE-Step (~14 GB): ~10–15 min
- Geração propriamente dita: 1–3 min (T4 16 GB sem offload)
- **Total: ~15–20 min na 1ª execução**, ~3–5 min nas seguintes (modelos persistem em cache do Kaggle)

### Saída

Arquivos vão para `/kaggle/working/output/` — aparecem no painel direito da UI em **Output**. Baixe individualmente.

## Limitações do Kaggle (vs sessão local ou VM dedicada)

- Sessão expira em **9h ativa ou 12h ociosa**
- Cap de **30 horas de GPU por semana** por conta
- File system `/kaggle/working/` **não persiste** entre sessões — outputs precisam ser baixados ou commitados como dataset
- Datasets privados persistem (até 100 GB no plano grátis)
- Sem `VS Code Remote-SSH` direto (existe hack via ngrok mas é frágil)

## Por que Kaggle e não Colab/GCP

- **Kaggle T4 grátis**, sem cartão, sem prazo de validade da promoção
- **GCP exigiu €45 pré-pagamento** na Itália (categorização da conta) — ver memória `project_gcp_blocked_kaggle.md`
- **Colab Pro+** (~$50/mês) seria opção se Kaggle se mostrar limitante — não foi necessário até agora

## Variações que valem testar

| Variação | Mudar | Por quê |
|---|---|---|
| **Qualidade máxima** | `INFERENCE_STEPS=50`, `DURATION_SEC=60` | T4 aguenta — só leva mais minutos |
| **Iterar rápido** | `INFERENCE_STEPS=8`, `DURATION_SEC=15` | Geração em ~30s, bom pra testar caption |
| **Reproduzir resultado** | Anotar e fixar `SEED` | Mesma seed + mesmo TOML = mesmo output |
| **Outro gênero** | Editar `CAPTION` (em inglês) | Modelo treinado predominantemente em EN |
| **Tracks diferentes** | `COMPLETE_TRACKS='drums,bass'` ou `'drums,keyboard,strings'` | Cada combinação dá um arranjo diferente |
