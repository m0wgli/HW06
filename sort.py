import shutil
import sys
from pathlib import Path

CATEGORIES = {'images': ['.jpeg', '.png', '.jpg', '.svg'],
              'video': ['.avi', '.mp4', '.mov', '.mkv'],
              'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
              'audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'archives': ['.zip', '.gz', '.tar']

              }

BAD_SYMBOLS = ('%', '*', ' ', '-')

translit_dict = {
    ord('А'): 'A',
    ord('Б'): 'B',
    ord('В'): 'V',
    ord('Г'): 'H',
    ord('Ґ'): 'G',
    ord('Д'): 'D',
    ord('Е'): 'E',
    ord('Є'): 'Ye',
    ord('Ж'): 'Zh',
    ord('З'): 'Z',
    ord('И'): 'Y',
    ord('І'): 'I',
    ord('Ї'): 'Yi',
    ord('Й'): 'Y',
    ord('К'): 'K',
    ord('Л'): 'L',
    ord('М'): 'M',
    ord('Н'): 'N',
    ord('О'): 'O',
    ord('П'): 'P',
    ord('Р'): 'R',
    ord('С'): 'S',
    ord('Т'): 'T',
    ord('У'): 'U',
    ord('Ф'): 'F',
    ord('Х'): 'Kh',
    ord('Ц'): 'Ts',
    ord('Ч'): 'Ch',
    ord('Ш'): 'Sh',
    ord('Щ'): 'Shch',
    ord('Ь'): '',
    ord('Ю'): 'Yu',
    ord('Я'): 'Ya',
    ord('а'): 'a',
    ord('б'): 'b',
    ord('в'): 'v',
    ord('г'): 'h',
    ord('ґ'): 'g',
    ord('д'): 'd',
    ord('е'): 'e',
    ord('є'): 'ye',
    ord('ж'): 'zh',
    ord('з'): 'z',
    ord('и'): 'y',
    ord('і'): 'i',
    ord('ї'): 'yi',
    ord('й'): 'y',
    ord('к'): 'k',
    ord('л'): 'l',
    ord('м'): 'm',
    ord('н'): 'n',
    ord('о'): 'o',
    ord('п'): 'p',
    ord('р'): 'r',
    ord('с'): 's',
    ord('т'): 't',
    ord('у'): 'u',
    ord('ф'): 'f',
    ord('х'): 'kh',
    ord('ц'): 'ts',
    ord('ч'): 'ch',
    ord('ш'): 'sh',
    ord('щ'): 'shch',
    ord('ь'): '',
    ord('ю'): 'yu',
    ord('я'): 'ya',
    ord('%'): '_',
    ord('*'): '_',
    ord(' '): '_',
    ord('-'): '_'
}


def normalize(name: str) -> str:
    trans_name = name.translate(translit_dict)
    return trans_name


def move_file(file: Path, root_dir: Path, category: str):
    if category == 'unknown':
        return file.replace(root_dir / normalize(file.name))
    target_dir = root_dir / category
    if category == 'archives':
        return shutil.unpack_archive(file, target_dir / normalize(file.name))
    if not target_dir.exists():
        target_dir.mkdir()
    return file.replace(target_dir / normalize(file.name))


def sort_dir(root_dir: Path, current_dir: Path):
    for item in [f for f in current_dir.glob('*') if f.name not in CATEGORIES.keys()]:
        if not item.is_dir():
            category = get_categories(item)
            move_file(item, root_dir, category)
        else:
            sort_dir(root_dir, item)
            item.rmdir()


def get_categories(file: Path):
    extension = file.suffix.lower()
    for cat, ext in CATEGORIES.items():
        if extension in ext:
            print(f'Familiar extension - {extension}')
            return cat
    print(f'Unknown extension - {extension}')
    return 'unknown'


def print_files_by_category(root_dir):
    for category in CATEGORIES.keys():
        print(f"--- {category.upper()} ---")
        for item in (root_dir / category).glob('*'):
            if item.is_dir():
                continue
            print(f"{item.name}")


def main():
    try:
        path = Path(sys.argv[1])

    except IndexError:
        return f'There no path to folder. Take as parameter'

    if not path.exists():
        return 'Sorry, folder not exist'
    sort_dir(path, path)

    print_files_by_category(path)


if __name__ == '__main__':
    main()
