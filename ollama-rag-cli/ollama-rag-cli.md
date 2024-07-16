#  A simple RAG cli that use local ollama models

* The code reads PDF and/or text files from a specified directory.
* An Ollama embedding model is used to generate embeddings (numerical representations) for each text chunk.
* The Ollama embedding model generates an embedding for the query.
* The retrieved chunks are combined to form a context.
* The `ollama.chat` function uses the Ollama model to generate a response based on the provided context and the user's query.

## User positional arguments:
These are arguments the most be passed from the command line in order for the program to run.
* directory path: a directory that contain pdf or text files or both types.
* model: a ollama model that is installed the system.
* embedding model: a ollama model that is installed on the system.

## User optional arugments
* `-cs` or `--chunksize` (int): chunk size to use when text spliting.
* `-co` or `--chunkoverlap` (int): chunk overlap size to use when text splitting
* `-nr` or `--nresults` (int): the collection.query will return the n_results closest matches to each

  
## How to use:

```consloe
mkdir ollama-rag-cli
cd ollama-rag-cli
python3 -m venv orc
source orc/bin/activate
pip install ollama chormadb langchain PyMuPDF

```
Copy or download the script <a href="https://github.com/ip-repo/python/blob/main/ollama-rag-cli/ollama-rag-cli.py">`ollama-rag-cli.py`</a> and place in the directory you created.
Now you can run the script. 
**reminder: you must specify directory path, model to use and embedding model to use (they most be installed on your system)**.
```console
python3 ollama-rag-cli.py path/to/directory/ gemma2 nomic-embed-text
````
### More examples:
```console
python3 ollama-rag-cli.py path/to/directory/ gemma2 nomic-embed-text -co 100
python3 ollama-rag-cli.py path/to/directory/ gemma2 nomic-embed-text --chunksize 600 -nr 3

```

