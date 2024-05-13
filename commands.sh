ssh -i "postercokeypair.pem" ubuntu@43.207.52.193

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx