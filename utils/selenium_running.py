import psutil

def selenium_running() -> list[psutil.Process] | bool:
    """Verifica se Selenium/Chrome está em execução"""
    
    procs = []
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'] == 'chrome.exe' and 'selenium' in " ".join(proc.info['cmdline']):
            procs.append(proc)
    
    return procs