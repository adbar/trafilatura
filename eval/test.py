import trafilatura

with open('benchmark/dataset_original/11.html', 'rb') as f:
    content = trafilatura.extract(f.read())
    print(content)
