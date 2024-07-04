# A RAG app built with gradio that use local ollama models to answer question based on urls


![url-rag](https://github.com/ip-repo/python/assets/123945379/4fd0cbfb-372c-4229-8a48-ad16bac5b19b)

This app is a simple gradio chatbot that allow a user to send a prompt with a question and urls and to receive answers based on the urls.
The app use the local ollama model installed on the user system, i have tested this app with gemma2 and it worked nicely.

## How to use: 

First you need to have installed ollama on your system and install at least one llm and one embding model.
```console
ollama pull nomic-embed-text
ollama pull gemma2
```
Create a venv
```console
python -m venv rag-venv
```
Then install the python libraries.
```console
pip install langchain #0.2.6
pip install langchain-community #0.2.6
pip install langchain-core #0.2.11
pip install gradio #4.37.2
pip install tiktoken #0.7.0
pip install beautifulsoup4 #4.12.3
```
Download or copy the script `url_rag.py`.

Then in the file you can change the local model to use and other settings.
```python
model_name = "gemma2"
temperature = 0
en_model_name = "gpt-4o"
encoding_name = "cl100k_base"
chunk_size  = 8000
chunk_overlap = 100
```
Now you can run the file and it should open the app in a new tab.

Note: make sure to prompt with the following format:  **Question::url,url,url**.

### Limitations 
* No memory, if you want to ask more questions and urls you already have asked before you will need to resend the urls.
* each prompt will have to a question and at least once url.
* A general exception if something go wrong, can be a bad prompt, no internet connection or invalid url.
* Performance may change from browser to browser due gradio limitations.
