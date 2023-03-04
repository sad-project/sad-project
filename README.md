# sad-project
[![Django CI](https://github.com/sad-project/sad-project/actions/workflows/django.yml/badge.svg)](https://github.com/sad-project/sad-project/actions/workflows/django.yml)

## Install Dependencies
```bash
pip install -r sad/requirements.txt
```

## Run Project
First you should run an MinIO instance. Using Docker is recommended. So you can use the command bellow.
```bash
sudo docker run \
  -d -p 9000:9000 -p 9001:9001 -v ~/minio-data:/mnt/data \
  minio/minio server /mnt/data --console-address ":9001"
```
Then config the MinIO variables in `sad/sad/settings.py` and run the Django project.
```bash
python sad/manage.py migrate
python sad/manage.py runserver
```

