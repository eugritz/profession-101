def paginate(source, page, max):
    start = page * max
    return source[start:start + max]
