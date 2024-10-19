from json import load, JSONDecodeError


def load_config():
    try:
        with open('config/config.json', 'r', encoding='utf-8') as file:
            return load(file)
    except FileNotFoundError:
        raise FileNotFoundError('config/config.json not found')
    except JSONDecodeError:
        raise JSONDecodeError('config/config.json is not a valid JSON file')
    except Exception as e:
        raise Exception(f'Error loading config: {e}')
