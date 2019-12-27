def get(data, keys=None, default_value=None):
    if data is None:
        return default_value

    if keys is None:
        return data

    if not isinstance(keys, list):
        return data

    current = data
    for key in keys:
        if isinstance(current, list):
            try:
                current = current[key]
            except Exception:
                return default_value
        else:
            current = current.get(key, None)
        if current is None:
            return default_value

    return current
