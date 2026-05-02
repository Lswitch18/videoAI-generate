# Guia de Instalação - HunyuanVideo-1.5 no Linux (Sem GPU)

## 1. Instalar Python e pip

```bash
# Atualizar repositórios
sudo apt update

# Instalar Python 3
sudo apt install python3

# Instalar pip
sudo apt install python3-pip

# Verificar versão
python3 --version
pip3 --version
```

### Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Agora todo pip install será instalado no ambiente virtual
```

---

## Especificações do HunyuanVideo-1.5

| Recurso | Valor |
|--------|-------|
| Parâmetros | 8.3B |
| VRAM Mínima | **14GB** (com offloading) |
| Recomendado | 16GB+ |
| Resoluções | 480p, 720p |

---

## Configuração do Ambiente Atual

```bash
# Verificar ambiente
python3 --version
which python3
```

### Problema: Sem GPU Disponível

O ambiente atual **não possui GPU NVIDIA**. Para rodar HunyuanVideo-1.5:

**Opções:**
1. ✅ Usar serviço online (Gradio/Replicate)
2. ⏳ Provisionar GPU cloud
3. 🔧 Executar apenas preprocessing (sem inferência)

---

## Instalação (Preparado para quando tiver GPU)

### 1. Clonar Repositório

```bash
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5.git
cd HunyuanVideo-1.5
```

### 2.Instalar Dependências

```bash
# Python 3.10+
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install PyTorch (CUDA 12.4)
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# Install Flash Attention (opcional, para aceleração)
pip install ninja
pip install flash-attn --no-build-isolation

# Install SageAttention (opcional)
pip install sage-attn

# Install sgl-kernel (para FP8)
pip install sgl-kernel==0.3.18
```

### 3. Baixar Modelo

```bash
# Método 1: HuggingFace CLI
huggingface-cli download tencent/HunyuanVideo-1.5 \
    --include "transformer/480p_t2v/*" \
    --local-dir ./ckpts

# Método 2: Python
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='tencent/HunyuanVideo-1.5', local_dir='./ckpts', allow_patterns=['transformer/480p_t2v/*'])"
```

---

## Gerar Vídeo

### Text-to-Video

```bash
torchrun --nproc_per_node=1 generate.py \
    --prompt "A cat walks on the grass, realistic style" \
    --resolution 480p \
    --aspect_ratio 16:9 \
    --num_inference_steps 5 \
    --model_path ./ckpts \
    --output_path ./output.mp4 \
    --offloading false
```

### Image-to-Video

```bash
torchrun --nproc_per_node=1 generate.py \
    --prompt "The image comes alive with motion" \
    --image_path /path/to/image.png \
    --resolution 480p \
    --aspect_ratio 16:9 \
    --num_inference_steps 50 \
    --model_path ./ckpts \
    --output_path ./output.mp4
```

### Configurações Otimizadas

| Parâmetro | Para VRAM Baixa | Para Melhor Qualidade |
|----------|----------------|---------------------|
| `--resolution` | 480p | 720p |
| `--num_inference_steps` | 20-30 | 50 |
| `--offloading` | true | false |
| `--cfg_distilled` | true | false |
| `--sr` | false | true |

### Modelo Step-Distilled (Mais Rápido)

```bash
# 480p I2V com 8 steps (até 75% mais rápido)
torchrun --nproc_per_node=1 generate.py \
    --prompt "A hummingbird flying around flowers" \
    --image_path /path/to/image.png \
    --resolution 480p \
    --enable_step_distill \
    --num_inference_steps 8 \
    --cfg_distilled true \
    --model_path ./ckpts \
    --output_path ./output.mp4
```

---

## Opções sem GPU Local

### Opção 1: API Online (Recomendado)

Acesse [hunyuan.tencent.com/video](https://hunyuan.tencent.com/video) para usar online.

### Opção 2: Replicate

```python
# Install replicate
pip install replicate

# Executar via API
import replicate
output = replicate.run(
    "zsxkib/hunyuan-video-1.5:480p_t2v",
    input={"prompt": "A cat walks on the grass"}
)
```

### Opção 3: Cloud GPU

| Serviço | GPU | Preço/hr |
|---------|-----|---------|
| RunPod | A100 40GB | ~$0.40 |
| Lambda | A100 40GB | ~$0.50 |
| Vast.ai | A100 | ~$2-3 |
| Colab Pro | T4 16GB | ~$10/mês |

---

## Solução de Problemas

### CUDA Out of Memory
```bash
# Ativar offloading
python generate.py --offloading true

# Reduzir resolução
python generate.py --resolution 480p

# Reduzir steps
python generate.py --num_inference_steps 30
```

### Flash Attention Error
```bash
# Instalar sem flash attention
pip uninstall flash-attn -y
python generate.py --use_sageattn true
```

### FP8 Inference
```bash
# Baixar modelo FP8 (se disponível)
huggingface-cli download tencent/HunyuanVideo-1.5 \
    --include "*fp8*" \
    --local-dir ./ckpts

# Executar com FP8
python generate.py --use_fp8 true
```

---

## Referências

- [GitHub HunyuanVideo-1.5](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)
- [HuggingFace](https://huggingface.co/tencent/HunyuanVideo-1.5)
- [Diffusers](https://huggingface.co/collections/hunyuanvideo-community/hunyuanvideo-15)
- [Demo Online](https://hunyuan.tencent.com/video)