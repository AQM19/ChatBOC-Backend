docker compose down -v

docker stop ollama
docker rm ollama

rm -rf ./postgres/
rm -fr ./.venv
rm -fr ./.env