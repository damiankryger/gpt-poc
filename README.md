# How to run?

1. Create venv (if not already created)

```shell
python -m venv venv
```

2. Activate venv:

```shell
source venv/bin/activate
```

3. Install dependencies

```shell
pip install -r requirements.txt
```

4. Launch Weaviate

```shell
make up
```

5. Create schema

```shell
python create_schema.py
```

6. Feed the database

```shell
python feed_database.py
```