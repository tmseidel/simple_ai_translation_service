#!/usr/bin/env python3
import torch
import platform
import subprocess
import shutil
import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def check_nvidia_smi():
    print_header("Checking NVIDIA GPU (nvidia-smi)")
    if shutil.which("nvidia-smi") is None:
        print("❌ nvidia-smi not found — GPU driver may not be installed")
        return
    try:
        output = subprocess.check_output(["nvidia-smi"], text=True)
        print("✔ nvidia-smi found and working")
        print(output)
    except Exception as e:
        print("❌ Error running nvidia-smi:", e)

def check_torch_cuda():
    print_header("Checking PyTorch CUDA Support")
    print(f"PyTorch version: {torch.__version__}")

    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("CUDA device count:", torch.cuda.device_count())
        print("CUDA device name:", torch.cuda.get_device_name(0))
        print("CUDA version (PyTorch):", torch.version.cuda)
        print("cuDNN version:", torch.backends.cudnn.version())
    else:
        print("❌ CUDA not available in PyTorch")

def check_fp16_support():
    print_header("Checking FP16 / Half Precision Support")
    if not torch.cuda.is_available():
        print("❌ No GPU available — skipping FP16 test")
        return

    try:
        x = torch.randn(1000, 1000, device="cuda").half()
        y = torch.matmul(x, x)
        print("✔ FP16 matrix multiplication works on GPU")
    except Exception as e:
        print("❌ FP16 test failed:", e)

def check_transformers_inference():
    print_header("Checking Transformers GPU Inference")

    model_name = "t5-small"

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            model = model.to("cuda")

        text = "Translate English to German: The house is wonderful."
        inputs = tokenizer(text, return_tensors="pt")

        if torch.cuda.is_available():
            inputs = inputs.to("cuda")

        with torch.no_grad():
            output = model.generate(**inputs)

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        print("✔ Transformers inference successful")
        print("Output:", decoded)

    except Exception as e:
        print("❌ Transformers inference failed:", e)

def check_python_environment():
    print_header("Python & System Environment")
    print("Python version:", sys.version)
    print("Platform:", platform.platform())
    print("Processor:", platform.processor())

def main():
    print_header("AI SYSTEM CHECK — GPU & ENVIRONMENT VALIDATION")

    check_python_environment()
    check_nvidia_smi()
    check_torch_cuda()
    check_fp16_support