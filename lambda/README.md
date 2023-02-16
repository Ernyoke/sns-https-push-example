# lambda

## Development

### Create a venv

```
python3 -m venv venv
```

### Activate venv

```
.\venv\Scripts\Activate.sh
```

## Build and Deploy

### Generate requirements.txt

```
pip3 install pipreqs
pip3 install pip-tools

pipreqs --savepath=requirements.in && pip-compile
```
