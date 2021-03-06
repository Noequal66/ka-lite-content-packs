"""
collectmetadata.py

Usage:
  collectmetadata.py <contentpackdir> [--out=out]
  collectmetadata.py -h | --help
"""
import json
import pathlib
import zipfile
from docopt import docopt


CONTENTPACK_METADATA_FILENAME = "metadata.json"

CONTENTPACK_EXTENSION = "*.zip"

ALL_METADATA_FILENAME = "all_metadata.json"


def read_metadata(filename: pathlib.Path) -> dict:
    with zipfile.ZipFile(str(filename)) as zf:
        # necessary, since zf.open isn't smart enough to auto-decode and return
        # str (it returns bytes)
        try:
            s = zf.read(CONTENTPACK_METADATA_FILENAME).decode('utf-8') 

            metadata = json.loads(s)

            # add the file size here as well
            metadata['zip_size'] = filename.stat().st_size

            return metadata
        except KeyError:    # no metadata file, skip zipfile
            return None


def return_all_contentpack_files(dir: pathlib.Path) -> [pathlib.Path]:
    for path in dir.iterdir():
        if path.match(CONTENTPACK_EXTENSION):
            yield path


def main():
    args = docopt(__doc__)

    dir = pathlib.Path(args["<contentpackdir>"])

    if args["--out"]:
        out = pathlib.Path(args["--out"])
    else:
        out = pathlib.Path.cwd() / ALL_METADATA_FILENAME

    # ensure dir exists
    out.parent.mkdir(exist_ok=True, parents=True)

    all_metadata = [read_metadata(f) for f in return_all_contentpack_files(dir)]
    all_metadata = [m for m in all_metadata if m]

    with open(str(out), "w") as f:
        json.dump(all_metadata, f)

if __name__ == "__main__":
    main()
