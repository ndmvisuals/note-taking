def filter_hidden_directories(dirs):
    return [d for d in dirs if not d.startswith('.')]
