import undetected_chromedriver as uc
from webdriver_manager.core.os_manager import OperationSystemManager
from pathlib import Path

def start_browser(headless: bool = True) -> uc.Chrome:
    """Inicializa ChromeDriver
    
    Args:
        headless (bool): `True` (padrão): Inicializa em background. `False`: Inicializa em primeiro plano.
    """

    # Configura perfil Selenium
    profile_path = Path(__file__).parent / "selenium"
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    
    # Configurações adicionais para melhor experiência
    args = [
        "--window-size=1920,1080",
        "--disable-dev-shm-usage",
        "--disable-extensions",
    ]
    
    # Configurações adicionais para o modo headless
    if headless:
        for arg in args:
            options.add_argument(arg)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')

    conf = {"options": options, "headless": headless, "use_subprocess": True}
    chrome_version = int(OperationSystemManager().get_browser_version_from_os("google-chrome").split('.')[0])
    
    driver = uc.Chrome(version_main=chrome_version, **conf)
    driver.maximize_window()

    # Padrão de wait para localizar elementos
    driver.implicitly_wait(5)
    driver.get("https://chatgpt.com")
    return driver