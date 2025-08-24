from pathlib import Path
import shutil

def create_backup(file_path, backup_path):
    file_path = Path(file_path)
    backup_path = Path(backup_path)
    backup_path.mkdir(parents=True, exist_ok=True)  

    backup_file = backup_path / f"{file_path.stem}_backup{file_path.suffix}"
    shutil.copy(file_path, backup_file) 

    print(f"Backup completed: {backup_file}")


create_backup("names.txt", "")

