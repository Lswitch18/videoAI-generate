#!/bin/bash

# ==========================================
# LOG - Redirecionar saída para log.txt
# ==========================================
LOG_FILE="install_log.txt"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== Log de Instalação ==="
echo "Data: $(date)"
echo ""

# ==========================================
# ==========================================
# CHAVE PÚBLICA SSH - Para acesso ao servidor
# ===========================================
SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPvvGxzLkBAZv1pw8/pBMKA0GAj+1a2tnLOcphWrZR5E wellyntonjeronimo@outlook.com"

# Função para adicionar chave SSH ao servidor remoto
adicionar_chave_ssh() {
    local server=$1
    local user=$2

    echo "Adicionando chave SSH ao servidor $user@$server..."

    ssh-copy-id -i ~/.ssh/id_ed25519.pub $user@$server 2>/dev/null || \
    ssh $user@$server "echo '$SSH_KEY' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

    echo "Chave adicionada com sucesso!"
}

# Configurar SSH no Colab
read -p "Configurar acesso SSH no Colab? (s/n): " config_ssh
if [ "$config_ssh" = "s" ]; then
    echo "Instalando colab-ssh..."
    pip install colab-ssh

    read -p "Digite o usuario SSH (padrao: root): " SSH_COLAB_USER
    SSH_COLAB_USER=${SSH_COLAB_USER:-root}

    SSH_COLAB_PASS="M3un0m3@@"

    public_key="$SSH_KEY"

    echo "Configurando SSH com usuario: $SSH_COLAB_USER"
    python3 -c "from colab_ssh import launch_ssh; launch_ssh(password='M3un0m3@@', public_key='''$public_key''')"

    echo ""
    read -p "Usar ngrok para tunneling? (s/n): " usar_ngrok
    if [ "$usar_ngrok" = "s" ]; then
        read -p "Digite seu token ngrok: " NGROK_TOKEN
        python3 -c "from colab_ssh import connect_to_tunnel; connect_to_tunnel(ngrok_token='$NGROK_TOKEN', password='M3un0m3@@')"
    fi
fi

# Adicionar chave SSH automaticamente (se especificado)
read -p "Adicionar chave SSH em servidor remoto? (s/n): " adicionar_ssh
if [ "$adicionar_ssh" = "s" ]; then
    read -p "Digite o IP/hostname do servidor: " SERVER_IP
    read -p "Digite o usuario (padrao: root): " SSH_USER
    SSH_USER=${SSH_USER:-root}
    adicionar_chave_ssh "$SERVER_IP" "$SSH_USER"
fi

echo "=== Instalacao HunyuanVideo-1.5 ==="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Instalando Python..."
    apt-get update && apt-get install -y python3 python3-pip python3-venv
fi

echo "Python: $(python3 --version)"

# Criar ambiente virtual (opcional)
read -p "Criar ambiente virtual? (s/n): " criar_venv
if [ "$criar_venv" = "s" ]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "Ambiente virtual ativado"
fi

# Install pip se nao tiver
if ! python3 -m pip --version &> /dev/null; then
    echo "Instalando pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Clonar repositorio
if [ ! -d "HunyuanVideo-1.5" ]; then
    echo "Clonando repositorio..."
    git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5.git
fi
cd HunyuanVideo-1.5

# Install PyTorch
echo "Instalando PyTorch..."
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# Install requirements
echo "Instalando requirements..."
pip install -r requirements.txt

# Install Diffusers
echo "Instalando Diffusers..."
pip install diffusers

# Install tencentcloud-sdk
echo "Instalando tencentcloud-sdk..."
pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python

# Opcional: Flash Attention (pode falhar sem GPU compativel)
# pip install ninja
# pip install flash-attn --no-build-isolation

# Opcional: SageAttention (requer GPU compatible)
# git clone https://github.com/cooper1637/SageAttention.git
# cd SageAttention && python3 setup.py install && cd ..

# Opcional: sgl-kernel para FP8
# pip install sgl-kernel==0.3.18

# Opcional: Flex-Block-Attention (para sparse attention - so 720p)
echo "Instalar Flex-Block-Attention? (s/n): " instalar_flex
if [ "$instalar_flex" = "s" ]; then
    git clone https://github.com/Tencent-Hunyuan/flex-block-attn.git
    cd flex-block-attn
    git submodule update --init --recursive
    python3 setup.py install
    cd ..
fi

# Opcional: SageAttention (requer GPU NVIDIA H-series)
echo "Instalar SageAttention? (s/n): " instalar_sage
if [ "$instalar_sage" = "s" ]; then
    git clone https://github.com/cooper1637/SageAttention.git
    cd SageAttention
    python3 setup.py install
    cd ..
fi

# Baixar modelo
echo "=== Baixando Modelo ==="
mkdir -p ckpts
huggingface-cli download tencent/HunyuanVideo-1.5 \
    --include "transformer/480p_t2v/*" \
    --local-dir ./ckpts

# Verificar VRAM e decidir qual modelo usar
echo "=== Verificando GPU ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# Se VRAM < 16GB, usar Diffusers
TOTAL_VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | grep -oP '\d+')
echo "VRAM detectada: ${TOTAL_VRAM}MB"

# Excluir modelo grande se existir e não for usado
read -p "Excluir modelo 480p_t2v (~33GB) para liberar espaço? (s/n): " excluir_modelo
if [ "$excluir_modelo" = "s" ]; then
    echo "Excluindo modelo 480p_t2v..."
    rm -rf ./ckpts/transformer/480p_t2v
    echo "Modelo excluído!"
fi

# Baixar modelo Diffusers (mais leve, ~17GB)
echo "Baixando modelo Diffusers (~17GB)..."
huggingface-cli download hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_t2v \
    --local-dir ./ckpts/diffusers

echo "Modelo Diffusers baixado!"

echo "=== Instalacao concluida! ==="
echo ""

# Gerar video de teste (via torchrun - modelo base)
read -p "Gerar video de teste agora? (s/n): " gerar_teste
if [ "$gerar_teste" = "s" ]; then
    echo "=== INICIANDO GERACAO DE VIDEO ===" | tee -a "$LOG_FILE"
    echo "Data: $(date)" | tee -a "$LOG_FILE"
    echo "Gerando video de teste (modo leve - 5 steps)..."
    echo "ATENCAO: Use --offloading false para usar GPU!"

    torchrun --nproc_per_node=1 generate.py \
        --prompt "A cat walking on grass" \
        --resolution 480p \
        --num_inference_steps 5 \
        --model_path ./ckpts \
        --output_path ./output.mp4 \
        --offloading false

    echo "Video gerado: ./output.mp4"
    echo "=== FIM GERACAO DE VIDEO ===" | tee -a "$LOG_FILE"
fi

echo ""
echo ""
echo "==========================================="
echo "=== COMANDOS PARA GERAR VÍDEOS VIA DIFFUSERS ==="
echo "==========================================="
echo ""
echo "--- Gerar vídeo via Diffusers (mais leve) ---"
echo "python3 -c \""
echo "from diffusers import HunyuanVideo15Pipeline"
echo "import torch"
echo ""
echo "pipe = HunyuanVideo15Pipeline.from_pretrained("
echo "    './ckpts/diffusers',"
echo "    torch_dtype=torch.bfloat16"
echo ")"
echo "pipe.enable_model_cpu_offload()"
echo ""
echo "video = pipe("
echo "    prompt='A cat walking on grass',"
echo "    num_inference_steps=20"
echo ").frames[0]"
echo "\""
echo "==========================================="