import torch
print(f"CUDA is available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.current_device()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")

print(f"PyTorch CUDA version: {torch.version.cuda}")


x = torch.rand(5, 3)
print(x.device)  # Should be 'cpu'
if torch.cuda.is_available():
    x = x.cuda()
    print(x.device)  # Should be smething like 'cuda:0'