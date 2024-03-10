from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchDriverException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions
from time import sleep
import os

API_KEY = os.environ.get("API_KEY")

url = ("https://quillbot.com/?utm_medium=cpc&utm_source=google&utm_campaign=FA+-+HY+|+PERF+-+Search+|+Product+-+Ext"
       "+-+Chrome+-+Brand+|+DEVP+|+CPA&utm_term=quillbot&utm_content=664002325919&campaign_type=extension-19193089128"
       "&click_id=Cj0KCQiA5-uuBhDzARIsAAa21T-Hc-pjkeHPV2t_cfR1rKVLngrF75WDQ2dkaMjCO9DFilSTNzHoYSAaAqp7EALw_wcB"
       "&campaign_id=19193089128&adgroup_id=149512431012&ad_id=664002325919&keyword=quillbot&placement=&target"
       "=&network=g&extension=23083258234&gad_source=1&gclid=Cj0KCQiA5-uuBhDzARIsAAa21T-Hc"
       "-pjkeHPV2t_cfR1rKVLngrF75WDQ2dkaMjCO9DFilSTNzHoYSAaAqp7EALw_wcB")

client = OpenAI(
    api_key=API_KEY,
)

chat_log = []

while True:

    user_message = input("Ask me something? ")

    if user_message.lower() == "quit":
        break
    else:
        chat_log.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        feedback = response.choices[0].message.content.strip("\n").strip()

        print(f"Olivia: \n{feedback}")
        with open("original.txt", "a") as file:
            file.write(f"{feedback} \n")
        engine = webdriver.Chrome()

        engine.get(url)
        ignored = (NoSuchDriverException, StaleElementReferenceException, TimeoutException)

        sleep(5)
        text_area = WebDriverWait(engine, 10, ignored_exceptions=ignored) \
            .until(expected_conditions.presence_of_element_located((By.ID, "paraphraser-input-box")))

        text_area.send_keys(feedback)

        button = WebDriverWait(engine, 10, ignored_exceptions=ignored) \
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "css-1fz2g01")))

        sleep(2)
        button.click()

        sleep(10)
        paraphrased = WebDriverWait(engine, 10, ignored_exceptions=ignored) \
            .until(expected_conditions.presence_of_element_located((By.ID, "paraphraser-output-box"))).text

        # print(paraphrased)
        with open("paraphrased.txt", "a") as file:
            file.write(f"{paraphrased} \n")
        engine.quit()

        chat_log.append({"role": "assistant", "content": feedback.strip("\n").strip()})
