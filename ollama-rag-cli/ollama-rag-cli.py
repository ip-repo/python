import argparse
import os
import ollama
import fitz
import chromadb
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction

class OllamaEmbedding:
    def __init__(self, url: str="http://localhost:11434/api/embeddings", model_name: str="nomic-embed-text") -> None:
        """
        Set ollama embedding function.

        Args:
            url(str): the url for http request to ollama API.
            model_name(str): embedding model name.
        """
        self.ollama_embedding_function = OllamaEmbeddingFunction(
        url=url,
        model_name=model_name
        )

    def get_embedded_chunks(self, text_chunks: list) -> list: 
        """
        Get embedded text chunks.

        Args:
            text_chunks(list): text chunks to embedd.
        
        Returns:
            list of embedded text chunks.
        """
        return self.ollama_embedding_function(text_chunks)
    
    def get_embedd_query(self, query: str) -> str:
        """
        Get embedded string.

        Args:
            query(str): string to embedd.
        
        Returns:
            a embedded string.
        """
        return self.ollama_embedding_function(query)
     
class SplitTextIntoChunks:
    def __init__(self, text: str, text_name: str, chunk_size: int=800, chunk_overlap: int = 100, separators=[". ","\n\n","\n",""," "]) -> None:
        """
        Split text into chunks.

        Args:
            text(str): text to split.
            text_name(str): the text name.
            chunk_size(int): chunk size
            chunk_overlap: chunk overlap
            separator(list): a list to separate by.
        """
        self.text = text
        self.text_name = text_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators
        self.text_as_chunks = None
    
    def text_to_chunks(self) -> None:
        """
        Split text into chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.text_as_chunks = text_splitter.split_text(text=self.text)
    
    def get_chunks(self) -> list:
        """
        Get chunks.
        """
        return self.text_as_chunks
    
    def get_chunks_ids(self) -> list:
        """
        Get chunks ids as list.

        Returns:
            A list of string represting text chunks id.
        """
        if self.text_as_chunks:
            ids = []
            for i in range(len(self.text_as_chunks)):
                ids.append(self.text_name + "-part" + str(i + 1))

            return ids
        return []		

class PDFTextExtractor:
    def __init__(self, pdf_path: str) -> None:
        """
        Initialize a PDF file path and store as 
        document object for later user.

        Args:
            pdf_path(str): the path to the PDF.
        
        """
        self.pdf_path = pdf_path
        self.fitz_doc = fitz.open(pdf_path)

    def __del__(self) -> None:
        """
        Ensure that the PDF is closed properley when 
        PDFTextExtractor instance is deleted.
        """
        self.fitz_doc.close()

    def extract_text(self) -> str:
        """
        Extracts all the text from the PDF.

        Returns:
            text(str): The text from the PDF.
        """
        text = ""
        for page_number in range(self.fitz_doc.page_count):
            current_page = self.fitz_doc.load_page(page_number)
            text += current_page.get_text()
        return text

class ProgramManager:
    def __init__(self, args_dict: dict) -> None:
        """
        __init__ method of the class that handle the program.

        Args:
            args_dict(dict): user arguments dict.
        """
        self.args_dict = args_dict
        self.ready_chunks = []
        self.ready_ids = []
        self.chroma_client = chromadb.Client()
        self.ollama_embedding = OllamaEmbedding()
        self.parse_pdf()
        self.prase_text()
        self.create_collection()
        self.populate_collection()
          
    def parse_pdf(self) -> None:
        """
        Split text in pdfs files into cunks and prepare chunks ids.
        """
        if self.args_dict["pdfs"]:
            for pdf in self.args_dict["pdfs"]:
                temp_text_exctractor = PDFTextExtractor(pdf_path=pdf)
                pdf_text = temp_text_exctractor.extract_text()
                temp_text_splitter = SplitTextIntoChunks(
                     text=pdf_text,
                     text_name=pdf,
                     chunk_size=self.args_dict["chunk-size"],
                     chunk_overlap=self.args_dict["chunk-overlap"]
                )
                temp_text_splitter.text_to_chunks()
                for chunk in temp_text_splitter.get_chunks():
                    self.ready_chunks.append(chunk)
                for id in temp_text_splitter.get_chunks_ids():
                     self.ready_ids.append(id)
                   
    def prase_text(self) -> None:
        """
        Split text in text files into cunks and prepate chunks ids.
        """
        if self.args_dict["text"]:
            for text in self.args_dict["text"]: 
                with open(text, "r") as text_file:
                    text_text = text_file.read()
                    temp_text_splitter = SplitTextIntoChunks(
                     text=text_text,
                     text_name=text,
                     chunk_size=self.args_dict["chunk-size"],
                     chunk_overlap=self.args_dict["chunk-overlap"]
                )
                temp_text_splitter.text_to_chunks()
                for chunk in temp_text_splitter.get_chunks():
                    self.ready_chunks.append(chunk)
                for id in temp_text_splitter.get_chunks_ids():
                     self.ready_ids.append(id)
                
    def create_collection(self) -> None:
        """
        Create chromdb to store embedding.
        """
        self.collection = self.chroma_client.create_collection(name="rag-collection",
                                    embedding_function=self.ollama_embedding.ollama_embedding_function,
                                    metadata={"hnsw:space":"cosine"}
        )
         
    def populate_collection(self) -> None: 
        """
        Add data prased earlier to the database.
        Start the program loop.
        """
        self.collection.add(
            ids=self.ready_ids,
            documents=self.ready_chunks   
        )
        self.start_program_loop()
          
    def start_program_loop(self) -> None:
        """
        This method ask for user query and look for similarity context in the database
        and give back a response.It does that in a loop so that the user can ask as much questions 
        as he want until '/bye' is the input.
        """
        print(LINE)
        query = input("Enter your query:").strip()
        while query.lower().strip() != "/bye":
            try:
                results = self.collection.query(
                query_embeddings=self.ollama_embedding.ollama_embedding_function(query)
                ,n_results=self.args_dict["nresults"]
                )
                context = "|||".join(results["documents"][0])
                messages = [{"role":"system","content":"You an ai assitant that responde only based on the context provided with the question. if you cant find an answer in the context Say: 'No answer in the context'"},
                        {"role":"user","content":f"Answer the question only based on this context:{context}, the question is: {query}"}]
                response = ollama.chat(model="gemma2", messages=messages, stream=True)
                for chunk in response:
                    print(chunk['message']['content'] ,end='', flush=True)
                print(LINE)
                print("Files used as context :",", ".join(results["ids"][0]))
                print("Distances values:", ", ".join([str(dis) for dis in results["distances"][0]]))
                print(LINE)
                
                query = input("Enter your query:").strip()
            except ValueError:
                 continue
            except KeyboardInterrupt:
                 break

class ParseArgs:
    def __init__(self, args: argparse.Namespace) -> None:
        """
        __init__ method of ParseArgs.

        Args:
            args(argparse.Namespace): arguments passed by the user.
        """
        print(LINE)
        self.args = args
        ollama_models = [model["name"] for model in ollama.list()["models"]]
        self.args_dict = {
                    "pdfs": [], "text": [],
                    "chunk-size":600,
                    "chunk-overlap":0,
                    "ollama-models-installed": ollama_models,
                    "ollama-model" : "gemma2",
                    "ollam-embed-model" : None,
                    "nresults" : 3,
                    "procced" : True
                    }
        self.set_args_dict()
           
    def set_args_dict(self) -> None:
        """
        This method class a calls series of methods to test user aguments.
        """
        self.test_directory_positional_argument()
        if not (self.args_dict["pdfs"] or self.args_dict["text"]):
            self.args_dict["procced"] = False         
            print("Make sure to enter a correct path to a directory with pdf and/or text files.")
        else:
            self.set_chunk_size()
            self.set_chunk_overlap()
            self.set_ollama_model()
            self.set_ollama_embeding_model()
            self.set_nresults()

    def test_directory_positional_argument(self) -> None:
        """
        This method check if the files directory exists and if its contain pdf or text files.
        """
        if os.path.exists(self.args.directory):
            if not os.listdir(self.args.directory):
                self.args_dict["procced"] = False
                print("Found the directory but its empty.")
            else:
                for file_name in os.listdir(self.args.directory):
                    if file_name.lower().endswith(".pdf"):
                        self.args_dict["pdfs"].append(self.args.directory + "/" + file_name)
                    elif file_name.lower().endswith(".txt"):
                        self.args_dict["text"].append(self.args.directory + "/" +  file_name)
                    else:
                        continue                
        else:
            self.args_dict["procced"] = False
            print("Could not locate the directory, please check the path again.")

    def set_chunk_size(self)-> None:
        """
        Set chunk size fot text splitting.
        """
        if args.chunksize and args.chunksize > 0:
            self.args_dict["chunk-size"] = args.chunksize
            print("Chunk size:", self.args_dict["chunk-size"])
        else:
            print("Default chunk size:", self.args_dict["chunk-size"])
    
    def set_chunk_overlap(self)-> None:
        """
        Set chunk overlap for text splitting.
        """
        if args.chunkoverlap and args.chunkoverlap >0:
            self.args_dict["chunk-overlap"] = args.chunkoverlap
            print("Chunk overlap:", self.args_dict["chunk-overlap"])
        else:
            print("Default chunk overlap:", self.args_dict["chunk-overlap"])

    def set_ollama_model(self)-> None:
        """
        Set the ollama model to use to generate responses.
        """
        if args.ollamamodel:
            if (args.ollamamodel in self.args_dict["ollama-models-installed"]) or (args.ollamamodel in [model.split(":")[0] for  model in self.args_dict["ollama-models-installed"]]):
                self.args_dict["ollama-model"] = args.ollamamodel
                print("Ollama model set:",self.args_dict["ollama-model"])
            else:
                 self.args_dict["procced"] = False
                 print("Could not locate ollama model", args.ollamamodel)
        else:
            self.args_dict["procced"] = False
            print("You must specify a ollama model to use.")

    def set_ollama_embeding_model(self) ->None:
        """
        Set embedding model.
        """
        if args.embeddingmodel:
            if (args.embeddingmodel in self.args_dict["ollama-models-installed"]) or (args.embeddingmodel in [model.split(":")[0] for  model in self.args_dict["ollama-models-installed"]]):
                self.args_dict["ollama-embed-model"] = args.embeddingmodel
                print("Ollama embedding model:",self.args_dict["ollama-embed-model"])
            else:
                self.args_dict["procced"] = False
                print("Could not locate", args.embeddingmodel, "Please enter a valid embedding model")  
        else:
            self.args_dict["procced"] = False
            print("Please enter a valid embedding model")              

    def set_nresults(self):
        """
        Set nresults parameter.
        """
        if args.nresults and (args.nresults > 0):
            self.args_dict["nresults"] = args.nresults
        else:
            if args.nresults == None:
                print("Default n_results:",self.args_dict["nresults"])
            else:
                print("Wrong value for --nresults: value must be greater then 0")
                print("Default number of query results:",self.args_dict["nresults"])
    

if __name__ == "__main__":
    CURRENT_TERMINAL_WIDTH = os.get_terminal_size()[0]
    LINE = CURRENT_TERMINAL_WIDTH * "*"

    parser = argparse.ArgumentParser(description="RAG cli that allow to user to choose a directory with pds and text files and ask question about them to ollama installed models.")
    parser.add_argument("directory", help="A directory with pdf's or text files or both.")
    parser.add_argument("ollamamodel", help="The ollama model to use (you need to have it installed on your system.)", type=str)
    parser.add_argument("embeddingmodel", help="The embedding model to use.", type=str)
    parser.add_argument("-cs","--chunksize", help="Set chunk size.", type=int)
    parser.add_argument("-co","--chunkoverlap", help="Set chunk overlap size.", type=int)
    parser.add_argument("-nr", "--nresults", help="Number of closest matches to the query.", type=int)

    args = parser.parse_args()
    parse_args = ParseArgs(args=args)
    if parse_args.args_dict["procced"]:
        pm = ProgramManager(parse_args.args_dict)
    else:
        print(LINE)
        print("Wrong usage, make sure you have at least one ollama chat model and one ollama embedding model")
        print("A command should look like this: [python][filename][directorypath][modelname][embeddingmodelname]")
        print("Examples:python python_file.py path/to/directory/ gemma2 nomic-embed-text")
        print("Examples:python python_file.py path/to/directory/ gemma2 nomic-embed-text --chunksize 1000 -nr 1")
