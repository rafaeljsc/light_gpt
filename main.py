from utils.light_gpt import light_gpt
from utils.selenium_running import selenium_running

try:    
    answer = light_gpt(
        input_text="qual a população da china?",
        answer_style="abrangente",
        keep_context=False
    )

    print(answer)
finally:
    for process in selenium_running():
        process.terminate()
