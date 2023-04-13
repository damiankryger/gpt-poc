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
python feed_database_with_mocks.py
```

Or instead of launching the commands form 4th, 5th and 6th step, you can run the following command:

```shell
make seed
```