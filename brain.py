#!/usr/bin/env python3
"""
Brain - HunyuanVideo-1.5
=========================
Documentação do projeto de geração de vídeo por IA.

Data: 2026-04-29
"""

# =============================================================================
# PROJETO
# =============================================================================
PROJETO = {
    "nome": "HunyuanVideo-1.5",
    "origem": "Tencent",
    "tipo": "Text-to-Video / Image-to-Video",
    "parametros": "8.3B",
    "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5",
    "huggingface": "https://huggingface.co/tencent/HunyuanVideo-1.5"
}

# =============================================================================
# REQUISITOS
# =============================================================================
REQUISITOS = {
    "gpu": {
        "minimo": "14GB VRAM (com offloading)",
        "recomendado": "16GB+",
        "gpus_compativeis": ["RTX 3090", "RTX 4090", "A100", "H100"]
    },
    "sistema": "Linux",
    "python": "3.10+",
    "cuda": "12.4"
}

# =============================================================================
# DEPENDÊNCIAS
# =============================================================================
DEPENDENCIAS = {
    "obrigatorias": [
        "python3",
        "pip",
        "torch>=2.4.0",
        "torchvision>=0.19.0",
        "requirements.txt",
        "tencentcloud-sdk-python"
    ],
    "opcionais": [
        "flash-attn (GPU compute 8.0+)",
        "sage-attn (GPU H-series)",
        "flex-block-attn (720p sparse)",
        "sgl-kernel==0.3.18 (FP8)"
    ],
    "install": """
# pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# PyTorch CUDA 12.4
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# Requirements
pip install -r requirements.txt
pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
"""
}

# =============================================================================
# MODELOS
# =============================================================================
MODELOS = {
    "480p_t2v": {
        "tamanho": "~17GB",
        "tipo": "Text-to-Video",
        "resolucao": "480p",
        "status": "ok"
    },
    "480p_i2v": {
        "tamanho": "~17GB",
        "tipo": "Image-to-Video",
        "resolucao": "480p",
        "status": "ok"
    },
    "480p_t2v_distilled": {
        "tamanho": "~33GB",
        "tipo": "Text-to-Video (mais rápido)",
        "status": "espaco_insuficiente"
    },
    "720p_t2v": {
        "tamanho": "~50GB+",
        "tipo": "Text-to-Video",
        "status": "espaco_insuficiente"
    }
}

# =============================================================================
# COMANDOS
# =============================================================================
COMANDOS = {
    "download_modelo": """
mkdir -p ckpts
huggingface-cli download tencent/HunyuanVideo-1.5 \\
    --include "transformer/480p_t2v/*" \\
    --local-dir ./ckpts
""",
    "text_to_video": """
torchrun --nproc_per_node=1 generate.py \\
    --prompt "A cat walking on grass" \\
    --resolution 480p \\
    --num_inference_steps 5 \\
    --model_path ./ckpts \\
    --output_path ./output.mp4 \\
    --offloading false
""",
    "image_to_video": """
torchrun --nproc_per_node=1 generate.py \\
    --prompt "The image comes alive with motion" \\
    --image_path ./imagem.jpg \\
    --resolution 480p \\
    --num_inference_steps 5 \\
    --model_path ./ckpts \\
    --output_path ./output.mp4 \\
    --offloading false
""",
    "diffusers": """
from diffusers import HunyuanVideo15Pipeline
pipe = HunyuanVideo15Pipeline.from_pretrained(
    "hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_t2v",
    torch_dtype=torch.bfloat16
)
pipe.enable_model_cpu_offload()
video = pipe(prompt="A cat walking", num_inference_steps=20).frames[0]
"""
}

# =============================================================================
# PROBLEMAS
# =============================================================================
PROBLEMAS = [
    "VRAM insuficiente (Tesla T4 15GB < 14GB mínimo)",
    "Espaço em disco insuficiente para modelos maiores",
    "sage-attn não suporta compute capability < 8.0"
]

# =============================================================================
# LINKS
# =============================================================================
LINKS = {
    "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5",
    "huggingface": "https://huggingface.co/tencent/HunyuanVideo-1.5",
    "demo": "https://hunyuan.tencent.com/video",
    "diffusers": "https://huggingface.co/collections/hunyuanvideo-community/hunyuanvideo-15"
}

def print_brain():
    print("=" * 50)
    print("BRAIN - HUNYUANVIDEO-1.5")
    print("=" * 50)
    print(f"\nRequisito GPU: {REQUISITOS['gpu']['minimo']}")
    print(f"VRAM atual: 15GB (insuficiente)")
    print("\n--- Modelos ---")
    for nome, info in MODELOS.items():
        print(f"  {nome}: {info['tamanho']} [{info['status']}]")
    print("\n--- Problemas ---")
    for p in PROBLEMAS:
        print(f"  - {p}")
    print("=" * 50)

if __name__ == "__main__":
    print_brain()