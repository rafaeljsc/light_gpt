import time
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .start_browser import start_browser
from .selenium_running import selenium_running

driver = None

def light_gpt(input_text: str, answer_style: str = "moderado", keep_context: bool = False) -> str:

    """Envia o texto para a IA e retorna a resposta.

    Args:
        driver (uc.Chrome): WebDriver do Chrome
        input_text (str): Texto a ser enviado
        answer_style (str): Estilo da resposta. Valores aceitáveis: `compacto`, `moderado` (padrão), `abrangente`. 
        keep_context (bool): `True`: Mantém o contexto da conversa. `False` (padrão): Novo contexto a cada envio
    """

    global driver

    # Verifica se o Selenium já está em execução
    if not selenium_running():
        driver = start_browser(headless=False)
    
    # Verifica tag de contexto
    if not keep_context:
        driver.refresh()

    # Captura a caixa de texto onde o prompt é digitado.
    prompt_box = driver.find_element(By.XPATH, '//div[@id="prompt-textarea"]') 
    
    # Retorna a quantidade de respostas registradas na sessão.
    answer_count = len(driver.find_elements(By.XPATH, '//button[@aria-label="Copiar resposta"]')) 

    # Configura instruções adicionais com base no estilo de resposta definido.
    if answer_style == "compacto":
        temp_instructions = "Responda de forma curta e precisa, em apenas uma única linha."
        temp = "0"
    elif answer_style == "moderado":
        temp_instructions = "Responda de forma moderada e direta."
        temp = "0.5"
    else:
        temp_instructions = "Responda de forma completa, detalhada e abrangente."
        temp = "0.8"

    # Formata input para envio
    final_prompt = f"""
    TEXTO DE ENTRADA: 
    {input_text}

    ---
    INSTRUÇÕES DE FORMATAÇÃO:
    - Não adicione emojis.
    - Não use negrito, listas ou Markdown. Use APENAS parágrafos.
    - Tamanho da resposta: {temp_instructions}
    - Parâmetro de criatividade (Temperature): {temp}
    """
    
    # Envia prompt para IA
    for txt in final_prompt.split('\n'):
        if txt:
            prompt_box.send_keys(txt)
            prompt_box.send_keys(Keys.SHIFT + Keys.ENTER)

    prompt_box.send_keys(Keys.ENTER)

    # Ignora login, caso solicitado
    try:
        driver.find_element(By.XPATH, '//a[text()="Permanecer desconectado"]').click()
    except:
        pass

    # Aguarda IA retornar a resposta completa    
    while len(driver.find_elements(By.XPATH, '//button[@aria-label="Copiar resposta"]')) == answer_count:
        time.sleep(1)

    # Retorna reposta da IA
    answer = driver.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]')[-1].text
    return unicodedata.normalize("NFKC", answer)
