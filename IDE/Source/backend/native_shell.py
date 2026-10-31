"""Windows application identity and a per-user, per-edition instance lock."""
def claim_instance(edition: str) -> bool:
    import ctypes
    import os
    from ctypes import wintypes
    shell = ctypes.WinDLL('shell32')
    shell.SetCurrentProcessExplicitAppUserModelID.argtypes = [wintypes.LPCWSTR]
    shell.SetCurrentProcessExplicitAppUserModelID(f'DevForge.{edition}')
    if os.environ.get('DEVFORGE_TEST_HIDDEN'):
        return True
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    handle = kernel.CreateMutexW(None, False, f'Local\\DevForge.{edition}')
    if not handle:raise ctypes.WinError(ctypes.get_last_error())
    if ctypes.get_last_error() == 183:
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(handle)
        ctypes.windll.user32.MessageBoxW(0, 'Приложение уже запущено. Откройте его окно на панели задач.', f'DevForge {edition}', 64)
        return False
    return True
