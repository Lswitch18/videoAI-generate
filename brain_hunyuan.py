#!/usr/bin/env python3
"""
Brain - Caso HunyuanVideo-1.5
===============================
Documentação completa do caso de instalação do HunyuanVideo-1.5 no Google Colab.

Data: 2026-04-29
Autor: lswitch
"""

# =============================================================================
# RESUMO DO PROJETO
# =============================================================================
PROJETO = {
    "nome": "HunyuanVideo-1.5",
    "origem": "Tencent",
    "tipo": "Geração de vídeo por IA (Text-to-Video / Image-to-Video)",
    "parametros": "8.3B",
    "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5",
    "huggingface": "https://huggingface.co/tencent/HunyuanVideo-1.5"
}

# =============================================================================
# HARDWARE E AMBIENTE
# =============================================================================
AMBIENTE = {
    "plataforma": "Google Colab",
    "gpu": {
        "nome": "Tesla T4",
        "vram": "15GB",
        "compute_capability": "7.5",
        "disponivel": True
    },
    "problema_vram": "8GB insuficientes - necessário 14GB mínimo",
    "sistema": "Linux (Ubuntu 24.04)",
    "python": "3.12"
}

# =============================================================================
# DEPENDÊNCIAS INSTALADAS
# =============================================================================
DEPENDENCIAS = {
    "obrigatorias": [
        "python3",
        "pip",
        "torch==2.4.0 (ou 2.6.0)",
        "torchvision==0.19.0",
        "-r requirements.txt",
        "tencentcloud-sdk-python"
    ],
    "opcionais": [
        "flash-attn (falhou - compute capability baixa)",
        "sage-attn (falhou - GPU incompatível)",
        "flex-block-attn (não testado)",
        "sgl-kernel==0.3.18 (FP8)"
    ],
    "instalacao_basica": """
# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# PyTorch CUDA 12.4
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# Requirements
pip install -r requirements.txt
pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
""",
    "instalacao_opcional": """
# Flash Attention
pip install ninja
pip install flash-attn --no-build-isolation

# SageAttention (requer GPU H-series)
git clone https://github.com/cooper1637/SageAttention.git
cd SageAttention && python3 setup.py install

# Flex-Block-Attention
git clone https://github.com/Tencent-Hunyuan/flex-block-attn.git
cd flex-block-attn && git submodule update --init --recursive
python3 setup.py install

# sgl-kernel (FP8)
pip install sgl-kernel==0.3.18
"""
}

# =============================================================================
# PROBLEMAS ENCONTRADOS
# =============================================================================
PROBLEMAS = {
    "venv_nao_funciona": {
        "descricao": "Python no Colab não tem ensurepip",
        "solucao": "Instalar pip manualmente: curl https://bootstrap.pypa.io/get-pip.py",
        "alternativa": "Usar pip diretamente sem venv"
    },
    "modelo_distilled_nao_cabe": {
        "descricao": "Modelo cfg_distilled precisa de 33GB + 17GB = 50GB total",
        "problema": "Só tem 15GB VRAM + ~15GB disco livre",
        "solucao": "Usar modelo base 480p_t2v (17GB)"
    },
    "espaco_disco": {
        "descricao": "Apenas 15GB livres",
        "solucao": "Baixar apenas modelo 480p_t2v"
    },
    "travamento_inferencia": {
        "descricao": "Geração trava com VRAM 0%",
        "possible_causa": "Compatibilidade Tesla T4 (compute 7.5) é muito antiga",
        "solucoes_tentadas": [
            "Usar offloading=true",
            "Reduzir num_inference_steps para 5-10",
            "Usar cfg_distilled=false (modelo base)"
        ]
    },
    "sageattention_nao_suporta": {
        "descricao": "SageAttention requer compute capability 8.0+",
        "gpu_t4": "compute 7.5 - não suportado"
    }
}

# =============================================================================
# MODELOS DISPONÍVEIS
# =============================================================================
MODELOS = {
    "480p_t2v": {
        "tamanho": "~17GB",
        "descricao": "Text-to-Video 480p",
        "download": "huggingface-cli download tencent/HunyuanVideo-1.5 --include 'transformer/480p_t2v/*' --local-dir ./ckpts"
    },
    "480p_i2v": {
        "tamanho": "~17GB",
        "descricao": "Image-to-Video 480p",
        "download": "huggingface-cli download tencent/HunyuanVideo-1.5 --include 'transformer/480p_i2v/*' --local-dir ./ckpts"
    },
    "480p_t2v_distilled": {
        "tamanho": "~33GB",
        "descricao": "Text-to-Video distilled (mais rápido)",
        "problema": "não cabe no disco"
    },
    "720p_t2v": {
        "tamanho": "~50GB+",
        "descricao": "Text-to-Video 720p",
        "problema": "não cabe"
    }
}

# =============================================================================
# COMANDOS PARA GERAR VÍDEO
# =============================================================================
COMANDOS = {
    "text_to_video": """
torchrun --nproc_per_node=1 generate.py \\
    --prompt "A cat walking on grass" \\
    --resolution 480p \\
    --num_inference_steps 20 \\
    --model_path ./ckpts \\
    --output_path ./output.mp4 \\
    --offloading true
""",
    "image_to_video": """
torchrun --nproc_per_node=1 generate.py \\
    --prompt "The image comes alive with motion" \\
    --image_path ./sua_imagem.jpg \\
    --resolution 480p \\
    --num_inference_steps 20 \\
    --model_path ./ckpts \\
    --output_path ./output.mp4 \\
    --offloading true
""",
    "sem_offloading": """
# Para GPUs com 16GB+ VRAM
torchrun --nproc_per_node=1 generate.py \\
    --prompt "A cat walking" \\
    --resolution 480p \\
    --num_inference_steps 20 \\
    --model_path ./ckpts \\
    --output_path ./output.mp4 \\
    --offloading false
""",
    "diffusers": """
# Usar via Diffusers (mais estável)
from diffusers import HunyuanVideo15Pipeline
from diffusers.utils import export_to_video

pipe = HunyuanVideo15Pipeline.from_pretrained(
    "hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_t2v",
    torch_dtype=torch.bfloat16
)
pipe.enable_model_cpu_offload()

video = pipe(
    prompt="A cat walking",
    num_inference_steps=20
).frames[0]

export_to_video(video, "output.mp4")
"""
}

# =============================================================================
# ACESSO SSH
# =============================================================================
SSH = {
    "chave_publica": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPvvGxzLkBAZv1pw8/pBMKA0GAj+1a2tnLOcphWrZR5E wellyntonjeronimo@outlook.com",
    "ip_colab": "172.28.0.12 (interno)",
    "problema": "IP interno - precisa de tunnel (ngrok)",
    "solucao_colab_ssh": """
# No Colab
pip install colab-ssh
from colab_ssh import launch_ssh
launch_ssh(password='sua_senha', public_key='CHAVE_PUBLICA')

# Ou com ngrok
from colab_ssh import connect_to_tunnel
connect_to_tunnel(ngrok_token='SEU_TOKEN', password='senha')
"""
}

# =============================================================================
# SCRIPT DE INSTALAÇÃO
# =============================================================================
SCRIPT_INSTALACAO = "/home/lswitch/videoAI/install_hunyuan.sh"

# =============================================================================
# PRÓXIMOS PASSOS
# =============================================================================
PROXIMOS_PASSOS = [
    "1. Usar cloud com GPU melhor (A100 40GB) - RunPod/Lambda",
    "2. Testar via Diffusers",
    "3. Testar API alternativa (Replicate, RunPod)",
    "4. Considerar modelos menores (Lumen, ModelScope)",
    "5. Esperar modelo mais leve do HunyuanVideo"
]

# =============================================================================
# LINKS ÚTEIS
# =============================================================================
LINKS = {
    "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5",
    "huggingface": "https://huggingface.co/tencent/HunyuanVideo-1.5",
    "demo_online": "https://hunyuan.tencent.com/video",
    "diffusers": "https://huggingface.co/collections/hunyuanvideo-community/hunyuanvideo-15",
    "prompt_handbook": "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md",
    "runpod": "https://runpod.io",
    "lambda": "https://lambda.ai",
    "replicate": "https://replicate.com"
}

# =============================================================================
# IMPRIMIR RESUMO
# =============================================================================
def print_brain():
    print("=" * 60)
    print("BRAIN - CASO HUNYUANVIDEO-1.5")
    print("=" * 60)
    print(f"\nGPU: {AMBIENTE['gpu']['nome']} ({AMBIENTE['gpu']['vram']})")
    print(f"Problema: VRAM insuficiente (8GB vs 14GB necessário)")
    print("\n--- Modelos ---")
    for nome, info in MODELOS.items():
        status = "✓" if "problema" not in info else "✗"
        print(f"  {status} {nome}: {info.get('tamanho', '?')} - {info['descricao']}")
    print("\n--- Próximos Passos ---")
    for passo in PROXIMOS_PASSOS:
        print(f"  {passo}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print_brain()