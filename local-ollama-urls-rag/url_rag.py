from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import gradio

class UrlRag:
	def __init__(self,model_name: str="gemma2",temperature: float=0,
			  	en_model_name: str="gpt-4o",encoding_name: str="cl100k_base",
				chunk_size: int=8000, chunk_overlap: int=100) -> None:
		self.model_name = model_name
		self.temperature = temperature
		self.en_model_name = en_model_name
		self.encoding_name = encoding_name
		self.chunk_size = chunk_size
		self.chunk_overlap = chunk_overlap


	def start_process(self,message: str,history: list):
		""" 
		This method manage the ask and get response process.

		Args:
			message(str): the user prompt
			history(list): message and answer history
		"""
		if "::" not in message:
			return "Incorrect prompt, here's an exmaple:\nWhen was Gustav born::https://en.wikipedia.org/wiki/Gustave_Eiffel"
		else:
			try:
				splitted_message = message.split("::")
				question = splitted_message[0]
				urls = [url for url in splitted_message[1].split(",")if url]
				self.set_question(question=question)
				self.set_urls_list(urls=urls)
				self.set_ollama_model(model=self.model_name, temperature=self.temperature)
				self.documents_loader()
				self.set_text_splitter(en_model_name=self.en_model_name, encoding_name=self.encoding_name,
									chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
				self.split_documents()
				self.set_vectorstore()
				self.set_retiever()
				self.set_chat_prompt_template()
				return self.get_response()
			except Exception:
				# Kinda lazy exception, this can be improved :)
				return "There was error, check your prompt format, urls and internet connection."

	def set_question(self, question :str):
		"""
		This method is used to set the question to ask the modle.

		Args:
			question(str): the question
		"""
		self.question = question
	
	

	def set_urls_list(self, urls: list):
		"""
		This method is used to set the urls list

		Args:
			urls(list): a list of urls

		"""
		self.urls = urls
	
	def set_ollama_model(self, model: str,temperature: float):
		"""
		This method is used to set which ollama model to use.

		Args:
			model(str): the model name to use
			temperature(float): set the temperature rate

		Note: this method assume that you have the model installed on your system
		"""
		self.chat_ollama_obj = ChatOllama(model=model, temperature=temperature)
	
	def documents_loader(self):
		"""
		This method create a document list from the urls list.
		"""
		documents_objects_list = []
		for url in self.urls:
			documents_objects_list.append(WebBaseLoader(url).load())
		self.documents_list = []
		for documents_items in documents_objects_list:
			for item in documents_items:
				self.documents_list.append(item)
	
	def set_text_splitter(self, en_model_name: str,encoding_name,
					   chunk_size: int, chunk_overlap: int):
		"""
		This create the character spliiter object

		Args:
			model_name(str): the model to use 
			encoding_name(str): which encoding to use
			chunk_size(int): the chunk size
			chunk_overlay(int): chunk_overlap size
		"""
		self.character_text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
			model_name=en_model_name,
			encoding_name=encoding_name,
			chunk_size=chunk_size,
			chunk_overlap=chunk_overlap)
	
	def split_documents(self):
		"""
		This method continue to format the documents by splitting them.
		"""
		self.splitted_documents = self.character_text_splitter.split_documents(documents=self.documents_list)

	def set_vectorstore(self,ollama_embedding_model: str="nomic-embed-text"):
		"""
		This method set the vectorstore.

		Args:
			ollama_embeding_model(str): the embedding model to use 
		"""
		self.vectorstore = Chroma.from_documents(
			documents=self.splitted_documents,
			embedding=OllamaEmbeddings(model=ollama_embedding_model)
		)
	def set_retiever(self):
		"""
		This method set the retriever.
		"""    
		self.vectorstore_retriever = self.vectorstore.as_retriever()


	def set_chat_prompt_template(self):
		"""
		This method create the chat template for the current question 
		and invoke the question and save's the response.
		"""
		template = """Use only the context provided to address the question:
		{context},Question: {question}
		""" 
		prompt = ChatPromptTemplate.from_template(template)
		chain = (
			{"context": self.vectorstore_retriever, "question": RunnablePassthrough()}
			| prompt
			| self.chat_ollama_obj
			| StrOutputParser()
		)

		self.response = chain.invoke(self.question)

	def get_response(self):
		"""
		This method is used to get the response

		Returns:
			self.response(str): the response
		"""
		return self.response

	
if __name__ == "__main__":	
	model_name = "gemma2"
	temperature = 0
	en_model_name = "gpt-4o"
	encoding_name = "cl100k_base"
	chunk_size  = 8000
	chunk_overlap = 100

	url_rag = UrlRag(model_name=model_name,temperature=0)

	app=gradio.ChatInterface(
		fn=url_rag.start_process,
		chatbot=gradio.Chatbot(height=500),
		
		textbox=gradio.Textbox(placeholder="Enter your prompt in the correct format => Question::url,url,url", container=False, scale=7),

		title="Answer Questions based on urls",
		description="""This is a web app that will alow you to ask questions based on urls that you proived.
		Make sure to use the correct format => Question::url,url,url
		""",
		theme="soft" ,
		examples=["When was Gustav born?::https://en.wikipedia.org/wiki/Gustave_Eiffel",
				"When the storming took place and what intersting things there is to tell about that building?::https://en.wikipedia.org/wiki/Storming_of_the_Bastille,https://en.wikipedia.org/wiki/Bastille"],
		cache_examples=False,
		retry_btn=None,
		undo_btn="Delete Previous",
		clear_btn="Clear",
	)

	app.launch(inbrowser=True)
