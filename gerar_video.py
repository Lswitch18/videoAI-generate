#!/usr/bin/env python3
"""
Script para gerar videos usando Diffusers
HunyuanVideo-1.5
"""
import torch
import argparse
from diffusers import HunyuanVideo15Pipeline
from diffusers.utils import export_to_video

def gerar_video(
    prompt: str,
    output_path: str = "output.mp4",
    num_frames: int = 121,
    num_inference_steps: int = 20,
    model_name: str = "hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_t2v",
    image_path: str = None,
    seed: int = None
):
    print(f"Carregando modelo: {model_name}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16

    pipe = HunyuanVideo15Pipeline.from_pretrained(
        model_name,
        torch_dtype=dtype
    )

    pipe.enable_model_cpu_offload()
    pipe.vae.enable_tiling()

    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)
        print(f"Usando seed: {seed}")

    print(f"Gerando video...")
    print(f"  Prompt: {prompt}")
    print(f"  Frames: {num_frames}")
    print(f"  Steps: {num_inference_steps}")

    if image_path:
        print(f"  Imagem: {image_path}")
        video = pipe(
            prompt=prompt,
            image_path=image_path,
            generator=generator,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps
        ).frames[0]
    else:
        video = pipe(
            prompt=prompt,
            generator=generator,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps
        ).frames[0]

    export_to_video(video, output_path, fps=24)
    print(f"Video salvo em: {output_path}")

    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerar video com HunyuanVideo-1.5")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt para gerar o video")
    parser.add_argument("--output", type=str, default="output.mp4", help="Caminho de saida")
    parser.add_argument("--frames", type=int, default=121, help="Numero de frames (121 = ~5s, 1440 = ~60s)")
    parser.add_argument("--steps", type=int, default=20, help="Numero de inference steps")
    parser.add_argument("--model", type=str, default="hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_t2v", help="Modelo no HuggingFace")
    parser.add_argument("--image", type=str, default=None, help="Caminho da imagem (para I2V)")
    parser.add_argument("--seed", type=int, default=None, help="Seed para reproducibilidade")

    args = parser.parse_args()

    gerar_video(
        prompt=args.prompt,
        output_path=args.output,
        num_frames=args.frames,
        num_inference_steps=args.steps,
        model_name=args.model,
        image_path=args.image,
        seed=args.seed
    )