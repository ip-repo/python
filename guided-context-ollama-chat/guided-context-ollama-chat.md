# Ollama local models with guided context from text files and a streamlit ui

This app allow the user to upload text files and to ask question about them.<br>
In this process no indexing or retrivers are used but just plain text guidance.<br>
In order to use this app you need to have ollama installed on your system with at least one model.

## How to use:
Create a folder and inside create a venv and install dependencies:
```
mkdir ogc
cd ogc
python3 -m venv ollama-guided-context
source ollama-guided-contex\bin\activate
pip install langchain-community                 #0.2.6
pip install langchain-core                      #0.2.11
pip install streamlit                           #1.36.0
```
Download or copy the script  <a href="https://github.com/ip-repo/python/blob/main/guided-context-ollama-chat/ollama_text_guided.py">`ollama_text_guided.py`</a> and place it inside the folder you created (`ogc` on this exmaple).

```console
streamlit ollama_text_guided.py
```

Notes:
* The app do not save chat history, the idea is that the models will responde only based on the uploaded text files and the current question.
* The streamlit ui get some css code that might not work well on every browser if that is the case just comment or remove the variable `page_css (line 66)` and also the line `st.markdown(page_css, unsafe_allow_html=True) (line 157)`.
