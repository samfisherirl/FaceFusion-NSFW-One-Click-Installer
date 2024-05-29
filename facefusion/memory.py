from facefusion.common_helper import is_macos, is_windows

if is_windows():
	import ctypes
else:
	import resource


def limit_system_memory(system_memory_limit : int = 1) -> bool:
	if is_macos():
		system_memory_limit = system_memory_limit * (1024 ** 6)
	else:
		system_memory_limit = system_memory_limit * (1024 ** 3)
	try:
		if is_windows():
			ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, ctypes.c_size_t(system_memory_limit), ctypes.c_size_t(system_memory_limit)) #type:ignore[attr-defined]
		else:
			resource.setrlimit(resource.RLIMIT_DATA, (system_memory_limit, system_memory_limit))
		return True
	except Exception:
		return False
