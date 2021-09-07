from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


def image_analyzer(x):
    filename = x
    parser = createParser(filename)
    metadata = extractMetadata(parser)
    data = metadata.exportPlaintext()

    result = [{}]
    for item in data:
        key, val = item.split(":", 1)
        if key in result[-1]:
            result.append({})
        result[-1][key] = val

    return result
