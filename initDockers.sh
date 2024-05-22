conda deactivate
source chatboc-env/bin/activate
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker pull postgres
docker run --name chatboc-db -e POSTGRES_PASSWORD=@1Xygm352Z+chatboc -d -p 5432:5432 postgres
