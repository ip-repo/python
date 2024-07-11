# Using local ollama with a streamlit ui

![locollama](https://github.com/ip-repo/python/assets/123945379/fa29cf25-9377-425b-9ec5-dbf33fd46111)

The user can choose from the models installed on his system ollama server and define a system message for the model.

After clicking on the submit button the chat is ready and the user can start prompting.

## How to use:


* Install ollama and also install at least one model #i've used the ollama version 0.1.48
* Create a venv and install dependecies :


```console 
pip install requests                            #2.32.3
pip install langchain-community                 #0.2.6
pip install langchain-core                      #0.2.11
pip install streamlit                           #1.36.0
```
Good, now you can download or copy the script <a href="https://github.com/ip-repo/python/blob/main/local-ollama/local_ollama.py">`local_ollama.py`</a>

Make sure to activate your venv and run the script like that:

```console
streamlit run local_ollama.py
```
