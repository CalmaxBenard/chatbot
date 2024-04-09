from openai import OpenAI
import streamlit as st
import warnings
import os
warnings.filterwarnings("ignore")

st.set_page_config(page_title="happy-assistant", page_icon=":movie_camera:")
st.title("🧑🏽‍💻 Supergal Olivia")
st.markdown("<style>div.block-container{padding-top:1.3rem}</style>", unsafe_allow_html=True)

st.write("Hi there! Olivia here. How may I help you?")

url = ("https://quillbot.com/?utm_medium=cpc&utm_source=google&utm_campaign=FA+-+HY+|+PERF+-+Search+|+Product+-+Ext"
       "+-+Chrome+-+Brand+|+DEVP+|+CPA&utm_term=quillbot&utm_content=664002325919&campaign_type=extension-19193089128"
       "&click_id=Cj0KCQiA5-uuBhDzARIsAAa21T-Hc-pjkeHPV2t_cfR1rKVLngrF75WDQ2dkaMjCO9DFilSTNzHoYSAaAqp7EALw_wcB"
       "&campaign_id=19193089128&adgroup_id=149512431012&ad_id=664002325919&keyword=quillbot&placement=&target"
       "=&network=g&extension=23083258234&gad_source=1&gclid=Cj0KCQiA5-uuBhDzARIsAAa21T-Hc"
       "-pjkeHPV2t_cfR1rKVLngrF75WDQ2dkaMjCO9DFilSTNzHoYSAaAqp7EALw_wcB")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = str(OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

chat_logs = []
max_iter = 100
user_key = 0
while user_key < max_iter:
    user_message = st.text_input("Type your question here...", key=user_key)

    if user_message != "":
        if user_message.lower() == "quit":
            break
        else:
            chat_logs.append({"role": "user", "content": user_message})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_logs,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            feedback = response.choices[0].message.content.strip("\n").strip()

            st.write(f"Olivia:  \n{feedback}")
            chat_logs.append({"role": "assistant", "content": feedback.strip("\n").strip()})

        user_key += 1

