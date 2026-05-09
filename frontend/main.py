import streamlit as st
from collections import defaultdict
import requests
import whisper
import tempfile
import uuid

st.set_page_config(
    page_title="Law Buddy AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

placeholder = "Ask me about law..."

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini_2_5_flash"

if 'messages' not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "audio_text" not in st.session_state:
    st.session_state.audio_text = ""

if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""

if "type_text" not in st.session_state:
    st.session_state.type_text = None

if "original_prompt" not in st.session_state:
    st.session_state.original_prompt = None

if "previous_prompt" not in st.session_state:
    st.session_state.previous_prompt = None

if "original_score" not in st.session_state:
    st.session_state.original_score = 0

if "previous_score" not in st.session_state:
    st.session_state.previous_score = 0

if "current_score" not in st.session_state:
    st.session_state.current_score = 0

if "prompt_state" not in st.session_state:
    st.session_state.prompt_state = "normal"
    
if "predicted_goal" not in st.session_state:
    st.session_state.predicted_goal = None

if "score_reason" not in st.session_state:
    st.session_state.score_reason = None

if "missing_areas" not in st.session_state:
    st.session_state.missing_areas = None

if "questions" not in st.session_state:
    st.session_state.questions = None

if "suggestions" not in st.session_state:
    st.session_state.suggestions = None

if "is_ready" not in st.session_state:
    st.session_state.is_ready = None

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

if "suggestion" not in st.session_state:
    st.session_state.suggestion = None

if "prompt_builder" not in st.session_state:
    st.session_state.prompt_builder = None

if "user_input" not in st.session_state:
    st.session_state.user_input = None

## chat url
chat_url = "http://localhost:8000/chat"
chat_conversations_url = "http://localhost:8000/chat/conversations"
chat_messages_url = "http://localhost:8000/chat/messages/{chat_id}"
chat_delete_url = "http://localhost:8000/chat/conversations/{chat_id}"

## prompt url
copilot_url = "http://localhost:8000/prompt/copilot"

def chat_api(promt):
    response = requests.post("http://localhost:8000/chat", json={"prompt": promt, "model": st.session_state.selected_model, "chat_id": st.session_state.chat_id})
    data = response.json()
    st.session_state.messages = data["history"]
    st.session_state.chat_id = data["chat_id"]

def copilot_api():
    response = requests.post(copilot_url, json={
        "model": st.session_state.selected_model,
        "original_prompt": st.session_state.original_prompt,
        "previous_prompt": st.session_state.previous_prompt ,
        "current_prompt": st.session_state.type_text ,
        "original_score": st.session_state.original_score ,
        "previous_score": st.session_state.previous_score ,
        "history": st.session_state.prompt_history ,
    })
    data = response.json()
    return data

with st.sidebar:
    st.write("law buddy")
    col1, col2 = st.columns([3, 2])
    st.session_state.selected_model = col1.selectbox("@", options=["gemini_2_5_flash", "gemini_2_5_pro", "llama_3_1_8b_instant", "llama_3_3_70b_versatile", "gpt_oss_120b", "gpt_oss_20b"], index=["gemini_2_5_flash", "gemini_2_5_pro", "llama_3_1_8b_instant", "llama_3_3_70b_versatile", "gpt_oss_120b", "gpt_oss_20b"].index(st.session_state.selected_model), label_visibility="collapsed")
    new_chat_button = col2.button("New Chat")
    if new_chat_button:
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.rerun()
    
    st.divider()
    
    with st.expander("features"):
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        if st.button("🚀Live Co-pilot"):
            st.session_state.prompt_state = "copilot"
        if st.button("🫧3 suggestions"):
            st.session_state.prompt_state = "suggestion"
        if st.button("✨Prompt builder"):
            st.session_state.prompt_state = "prompt_builder"
    
    st.divider()

    with st.expander("History"):
        conversations = requests.get(chat_conversations_url)
        data = conversations.json()
        if not data["chat_history"]:
            st.write("No chat history")
        else:
            st.session_state.chat_history = data["chat_history"]
            # st.session_state.chat_id = data["chat_history"][-1]["chat_id"]
            for chat in st.session_state.chat_history:
                col1, col2 = st.columns([4, 1])
                if chat["chat_id"] == st.session_state.chat_id:
                    if col1.button(chat["title"][:15] + "...", type="primary", key=chat["chat_id"]):
                        response = requests.get(chat_messages_url.format(chat_id=chat["chat_id"]))
                        data = response.json()
                        st.session_state.chat_id = chat["chat_id"]
                        st.session_state.messages = data["messages"]
                        st.rerun()
                else:
                    if col1.button(chat["title"][:15] + "...", key=chat["chat_id"]):
                        response = requests.get(chat_messages_url.format(chat_id=chat["chat_id"]))
                        data = response.json()
                        st.session_state.chat_id = chat["chat_id"]
                        st.session_state.messages = data["messages"]
                        st.rerun()
                    
                if col2.button("🗑️", key=chat["chat_id"] + "delete"):
                    requests.delete(chat_delete_url.format(chat_id=chat["chat_id"]))
                    st.session_state.messages = []
                    st.rerun()
    st.divider()

    with st.expander("setting"):
        st.button("something", key=11)
        st.button("something", key=12)
        st.button("something", key=13)

if st.session_state.prompt_state == "copilot":
    with st.container(border=True, key=f"copilot_container_{uuid.uuid4()}"):
        st.markdown(f"<h3> You write I will guide you to write a promt. </h3>", unsafe_allow_html=True)
        st.write(f"```Eg. I want to know more about gratuity```", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([20, 1, 1])
        st.session_state.prompt_text = col1.text_input("@", placeholder=placeholder, icon = "🚀", label_visibility="collapsed", key="copilot_text_search")
        if col2.button("↑", type="primary"):
            with st.spinner("Thinking..."):
                if st.session_state.prompt_text:
                    st.session_state.type_text = st.session_state.prompt_text
                    chat_api(st.session_state.type_text)
                    st.session_state.type_text = ""
                    st.session_state.prompt_state = "normal"
                    st.session_state.original_prompt = None
                    st.session_state.previous_prompt = None
                    st.session_state.original_score = 0
                    st.session_state.previous_score = 0
                    st.session_state.current_score = 0
                    st.session_state.predicted_goal = None
                    st.session_state.score_reason = None
                    st.session_state.missing_areas = None
                    st.session_state.questions = None
                    st.session_state.suggestions = None
                    st.session_state.is_ready = None
                    st.session_state.prompt_history = []
                    st.rerun()

        if col3.button("⨉", type="tertiary"):
            st.session_state.prompt_state = "normal"
            st.rerun()
        col1, col2, col3 = st.columns([2, 14, 1])
        col1.metric("percent", f"{st.session_state.current_score - st.session_state.original_score}%", f"{st.session_state.current_score - st.session_state.previous_score}%", border=True)
        with col2.container(border=True, height="stretch"):
            col1, col2 = st.columns([16, 1])
            if st.session_state.predicted_goal:
                st.progress(st.session_state.current_score / 100)
                st.info(f"🎯 {st.session_state.predicted_goal}")

                if st.session_state.is_ready:
                    st.success("✅ Prompt Ready")
                else:
                    st.warning("⚠ Needs Improvement")

                with st.expander("📊 Score Analysis"):
                    st.write(st.session_state.score_reason)

                with st.expander("🧩 Missing Areas"):
                    for area in st.session_state.missing_areas:
                        st.write(f"• {area}")

                with st.expander("❓ Clarifying Questions"):
                    for question in st.session_state.questions:
                        st.write(f"• {question}")

                with st.expander("💡 Suggestions"):
                    for suggestion in st.session_state.suggestions:
                        st.write(f"• {suggestion}")
        st.write(st.session_state.prompt_history)
        if col3.button("⫸"):
            with st.spinner("Thinking..."):
                if st.session_state.prompt_text:
                    if not st.session_state.original_prompt:
                        st.session_state.original_prompt = st.session_state.prompt_text
                    st.session_state.type_text = st.session_state.prompt_text
                    copilot_output = copilot_api()
                    print(copilot_output)
                    st.session_state.previous_prompt = st.session_state.prompt_text
                    if not st.session_state.original_score:
                        st.session_state.original_score = st.session_state.current_score
                    st.session_state.previous_score = st.session_state.current_score
                    st.session_state.current_score = copilot_output["prompt_quality_score"]
                    st.session_state.predicted_goal = copilot_output["predicted_goal"]
                    st.session_state.score_reason = copilot_output["score_reason"]
                    st.session_state.missing_areas = copilot_output["missing_areas"]
                    st.session_state.questions = copilot_output["questions"]
                    st.session_state.suggestions = copilot_output["suggestions"]
                    st.session_state.is_ready = copilot_output["is_ready"]
                    st.session_state.prompt_history.append({
                        "prompt": st.session_state.prompt_text,
                        "score": copilot_output["prompt_quality_score"]
                    })
                    st.rerun()

elif st.session_state.prompt_state == "suggestion":
    with st.container(border=True, key=f"suggestion_container_{uuid.uuid4()}"):
        st.markdown(f"<h3> Write a Prompt and get 3 relavent Prompts. </h3>", unsafe_allow_html=True)
        st.write(f"```Eg. I want to do research on astrology.```", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([18, 1, 1])
        st.session_state.prompt_text = col1.text_input("@", placeholder=placeholder, icon = "🫧", label_visibility="collapsed", key="suggestion_text_search")
        if col2.button("⫸", type="primary"):
            pass
        if col3.button("⨉", type="tertiary"):
            st.session_state.prompt_state = "normal"
            st.rerun()
        if st.session_state.prompt_text:
            st.markdown("""<style>.prompt-card { padding: 8px 14px; border-radius: 12px; background-color: #1e1e1e; margin-bottom: 14px;}</style> """, unsafe_allow_html=True)
            for i, prompt in enumerate(range(3)):
                col1, col2 = st.columns([22, 1])
                col1.write(f"<div class='prompt-card'> {i} prompt </div>", unsafe_allow_html=True)
                if col2.button("↑", key=f"send_button_{uuid.uuid4()}"):
                    with st.spinner("Thinking..."):
                        if st.session_state.prompt_text:
                            st.session_state.type_text = st.session_state.prompt_text
                            chat_api(st.session_state.type_text)
                            st.session_state.type_text = ""
                            st.session_state.prompt_state = "normal"
                            st.rerun()

elif st.session_state.prompt_state == "prompt_builder":
    with st.container(border=True, key=f"prompt_builder_container_{uuid.uuid4()}"):
        st.markdown(f"<h3> Give a basic context. </h3>", unsafe_allow_html=True)
        st.write(f"```Eg. I want to understand AI```", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([20, 1, 1])
        st.session_state.prompt_text = col1.text_input("@", placeholder=placeholder, icon = "✨", label_visibility="collapsed", key="prompt_builder_text_search")
        if col2.button("↑", type="primary"):
            with st.spinner("Thinking..."):
                if st.session_state.prompt_text:
                    st.session_state.type_text = st.session_state.prompt_text
                    chat_api(st.session_state.type_text)
                    st.session_state.type_text = ""
                    st.session_state.prompt_state = "normal"
                    st.rerun()
        if col3.button("⨉", type="tertiary"):
            st.session_state.prompt_state = "normal"
            st.rerun()
        with st.container(horizontal=True, width="content"):
            # col1, col2, col3 = st.columns([1,2])
            st.button("add some spice", key=1)
            st.button("add some spice", key=2)
            st.button("add some spice", key=3)
            st.button("add some spice", key=4)
            st.button("add some spice", key=5)
            st.button("add some spice", key=6)
            st.button("add some spice", key=7)
            st.button("add some spice", key=8)
            st.button("add some spice", key=9)

else:

    st.session_state.user_input = st.chat_input(placeholder, accept_audio=True, accept_file= True, key=1)

    if st.session_state.messages:
        qna_id = None
        grouped = defaultdict(dict)

        for msg in st.session_state.messages:
            grouped[msg["qna_id"]][msg["role"]] = msg["content"]

        for qna_id, pair in grouped.items():
            col1, col2 = st.columns([1, 3])
            if "user" in pair:
                with col2.chat_message("user"):
                    st.markdown(pair["user"])

            if "assistant" in pair:
                with st.chat_message("assistant"):
                    st.markdown(pair["assistant"])
    else:
        col1, col2, col3 = st.columns([1, 3, 1])
        col2.markdown("### Welcome to Law Buddy AI")
        col2.markdown("I'm here to help you with your legal queries. Ask me anything about law...")
        col2.markdown("You can select a model from the dropdown menu above.")
        col2.markdown("You can select a language from the dropdown menu above.")


    if st.session_state.audio_text  != "":
        with st.container(border=True):
            st.write(f"🎤 Audio Prompt: {st.session_state.audio_text}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("↑", type="primary"):
                    st.session_state.type_text = st.session_state.audio_text
                    chat_api(st.session_state.type_text)
                    st.session_state.audio_text = ""
                    st.rerun()
            with col2:
                if st.button("✕"):
                    st.session_state.audio_text = ""
                    st.rerun()

    if st.session_state.user_input:
        with st.spinner("Thinking..."):

            if st.session_state.user_input["text"]:
                st.session_state.type_text = st.session_state.user_input["text"]
                chat_api(st.session_state.type_text)
                st.session_state.type_text = ""
                st.rerun()

            if st.session_state.user_input["audio"]:
                audio = st.session_state.user_input["audio"]
                model = whisper.load_model("base")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio.read())
                    temp_audio_path = tmp_file.name

                result = model.transcribe(temp_audio_path)
                st.session_state.audio_text = st.session_state.audio_text + str(result["text"])
                st.rerun()

            if st.session_state.user_input["files"]:
                st.write(st.session_state.user_input["files"])
                st.rerun()
