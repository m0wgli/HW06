import os
import sys
import shutil
from pathlib import Path

unknown_extension = []

folders_to_del = []

extensions = {'images': ['.jpeg', '.png', '.jpg', '.svg'],
              'video': ['.avi', '.mp4', '.mov', '.mkv'],
              'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
              'audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'archives': ['.zip', '.gz', '.tar']

              }


def move(target_path: Path, file: Path):
    file.replace(target_path / file.name)


def normalize(text: str):
    result = ''
    for i in text:
        if 128 <= ord(i) >= 255:
            result += '_'
        else:
            result += i
    return result


def sort():
    path = Path(sys.argv[1])
    try:
        os.mkdir((path / 'images'))
        os.mkdir((path / 'documents'))
        os.mkdir((path / 'audio'))
        os.mkdir((path / 'video'))
        os.mkdir((path / 'archives'))
    except FileExistsError as f:
        print(f)

    for item in path.glob('**/*.*'):
        # shutil.move()
        move(path, item)
    for item in path.glob('**'):
        folders_to_del.append(item)

    for item in folders_to_del[::-1]:
        if item.name not in ('images', 'documents', 'audio', 'video', 'archives'):
            try:
                item.rmdir()
            except OSError as e:
                print(e)

    for item in path.glob('**/*.*'):
        s = normalize(item.name)
        os.rename(str(item), str(item.parent / s))

    for item in path.glob('**/*.*'):
        if item.suffix in extensions['images']:
            move(path / 'images', item)
        elif item.suffix in extensions['documents']:
            move(path / 'documents', item)
        elif item.suffix in extensions['audio']:
            move(path / 'audio', item)
        elif item.suffix in extensions['video']:
            move(path / 'video', item)
        elif item.suffix in extensions['archives']:
            shutil.unpack_archive(str(item), str(path / 'archives' / item.stem))
            os.remove(item)
        else:
            unknown_extension.append(item)


sort()