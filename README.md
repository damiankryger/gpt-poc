# How to run?

1. Activate venv:

```shell
source venv/bin/activate
```

2. Install dependencies

```shell
pip install -r requirements.txt
```

3. Launch Weaviate

```shell
docker-compose up -d
```

4. Launch project to feed the database

```shell
python main.py
```