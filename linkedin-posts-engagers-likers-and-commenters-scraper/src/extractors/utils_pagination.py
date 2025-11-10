def paginate(iterations: int, start_index: int = 0):
    """Generate pagination offsets for multiple iterations."""
    for i in range(start_index, start_index + iterations):
        yield i * 10