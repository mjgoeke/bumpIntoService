# Setup
```sh
git clone https://github.com/mjgoeke/bumpIntoService.git /var/www/bumpIntoService
cd /var/www/bumpIntoService

./setup_server.sh
```

# Redeploy
```sh
cd /var/www/bumpIntoService

git pull origin main

docker-compose down
docker-compose up --build -d

sudo nginx -t
sudo systemctl reload nginx
```