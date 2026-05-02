# Agent - HunyuanVideo-1.5

## Como usar o brain

Para ver as informações do projeto, execute:

```bash
python3 brain.py
```

O brain contém:
- Requisitos do projeto
- Dependências necessárias
- Modelos disponíveis
- Comandos para gerar vídeo
- Problemas conhecidos

## Comandos úteis

### Ver brain
```bash
python3 /home/lswitch/videoAI/brain.py
```

### Rodar script de instalação
```bash
bash /home/lswitch/videoAI/install_hunyuan.sh
```

### Gerar vídeo (Text-to-Video)
```bash
cd /content/HunyuanVideo-1.5
torchrun --nproc_per_node=1 generate.py \
    --prompt "A cat walking on grass" \
    --resolution 480p \
    --num_inference_steps 20 \
    --model_path ./ckpts \
    --output_path ./output.mp4 \
    --offloading true
```

### Gerar vídeo (Image-to-Video)
```bash
torchrun --nproc_per_node=1 generate.py \
    --prompt "The image comes alive with motion" \
    --image_path ./imagem.jpg \
    --resolution 480p \
    --num_inference_steps 20 \
    --model_path ./ckpts \
    --output_path ./output.mp4 \
    --offloading true
```

## Problema atual

VRAM insuficiente (Tesla T4 15GB < 14GB necessário)
- GPU não consegue rodar o modelo
- Necessário usar cloud com GPU melhor (A100 40GB)