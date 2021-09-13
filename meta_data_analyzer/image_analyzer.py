from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import os


def image_analyzer(path: str) -> dict:
    if path is None:
        return None
    else:
        parser = createParser(path)
        metadata = extractMetadata(parser)
        data = metadata.exportPlaintext()
        result = {}
        for item in data:
            key, val = item.split(":", 1)
            if key in result:
                continue
            result[key] = val

    return result


