"""Shared GUI binary; the installed executable name selects the product edition."""
import sys
from pathlib import Path
from ide_launcher import main as ide_main
from desktop_launcher import main as desktop_main


if __name__=='__main__':
    try:
        (ide_main if 'IDE' in Path(sys.executable).stem.upper() else desktop_main)()
    except Exception as error:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0,f'Не удалось запустить DevForge.\n{error}\nПодробности сохранены в журнале приложения.','DevForge',16)
        raise
