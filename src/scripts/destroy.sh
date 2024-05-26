docker compose down -v

docker stop ollama
docker rm ollama

sudo rm -rf ./postgres/
sudo rm -fr ./.venv
sudo rm -fr ./.env