docker run -d --gpus=all -v ollama:/root/.ollama -p 11439:11434 --name ollamamgpu ollama/ollama
docker run -d --gpus=all -v ollama_data:/root/.ollama -
p 11430:11434 --name ollamalarge ollama/ollama

nvidia-smi -L

--env CUDA_VISIBLE_DEVICES=GPU-d,GPU-

docker run -d --gpus=all -v _data:/root/.ollama -p 11430:11434 --name ollama4gpu  --env CUDA_VISIBLE_DEVICES=GPU-3ad0a1d,GPU-7665daf,GPU-ba8ff74,GPU-01173 ollama/ollama
docker run -d --gpus=all -v llama_data:/root/.ollama -p 11430:11434 --name ollama4gpu  --env CUDA_VISIBLE_DEVICES=GPU-34da1d,GPU-28af,GPU-bcf74,GPU-01653 --env OLLAMA_DEBUG=1 --env OLLAMA_SCHED_SPREAD=true ollama/ollama

