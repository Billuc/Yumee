import shutil
import uuid
from pathlib import Path


class FileTest:
    def __init__(self, path: Path) -> None:
        self.id = uuid.uuid4()
        self.path = path.resolve()
        self.temp_path = self.path.with_name(str(self.id) + self.path.suffix)

    def __enter__(self) -> Path:
        return shutil.copy(self.path, self.temp_path)

    def __exit__(self, type, value, tb) -> None:
        self.temp_path.unlink(True)


def temp_file(path: Path) -> FileTest:
    return FileTest(path)
