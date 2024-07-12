import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class HandleOllama:
	def __init__(self, model="gemma2", temperature=0.1) -> None:
		"""
		Craete a ChatOllama object to handle requests and responses to ollama

		Args:
			model(str): name of the ollama model to use(you should have it installed before using)
			temperature(float): set model temperature
		"""
		self.chat_ollama = ChatOllama(model=model, temperature=temperature)
	
	def chat_messages_from_messages(self, messages: list)-> None:
		"""
		Create a chat prmopt for messages template.

		Args:
			messages(list): list of messages
		"""
		self.prompt = ChatPromptTemplate.from_messages(messages=messages)

	def create_chain(self):
		self.chain = self.prompt | self.chat_ollama | StrOutputParser()
	
	def set_args(self, args: dict)->None:
		"""
		Set values to send to model while invoking it.

		Args:
			args(dict): a key-value pair that fit the template.
		"""
		self.args = args
	
	def invoke(self):
		"""
		Returns
			str : model response as string
		"""
		return self.chain.invoke(self.args)

	def invoke_stream(self):
		"""
		Yield(str): model response in strings chunks.
		"""
		self.latest_response = ""
		for chunk in self.chain.stream(self.args):
			self.latest_response +=chunk
			yield chunk

if __name__ == "__main__":
	# Create ollama handle object
	handle_ollama = HandleOllama(model="gemma2")

	# Define text context guiding message to use as chat templates
	messages = [("system" , "Answer the questions only based on the context: '{context}'"),
				("human","{question}")]
	
	# Set chat template
	handle_ollama.chat_messages_from_messages(messages=messages)
	
	# CSS styling
	page_css = """
	<style>
	[data-testid="stAppViewContainer"] {
	background-color : white;
	}
	
	h1 {
		color:gray;
		background-color:white;
	}

	[data-testid="stSidebar"] p {
	color: white;
	}

	p {
	color: gray;
	}

	[data-testid="stChatMessage"] {
	background-color:gray;
	}

	[data-testid="stMarkdownContainer"] p{
	color:white;}
	[data-testid="stSidebar"]  {
	
	background-color: gray;
	}

	[data-testid="stSidebar"] h1 {
	color:white;
	background-color: gray;
	}

	[class="st-emotion-cache-7oyrr6 e1bju1570"] {
		color:gray;
	}

	[data-testid="baseButton-secondary"] {
	color:white;
	background-color: gray;
	}

	[data-testid="baseButton-secondary"]:hover {
	border-color: red;
	color:white;

	}

	placeholder {
	color:white;
	}
	
	[data-testid="stFileUploaderDropzone"] {
	background-color:white;color:gray;
	}

	[data-testid="ScrollToBottomContainer"] {
	background-color: white;
	}

	[data-testid="stBottomBlockContainer"]{
	padding-top : 40px;
	background-color:white;
	}

	[class="st-emotion-cache-vj1c9o ea3mdgi6"] {
	background-color: white;
	}

	[class="st-emotion-cache-qcqlej ea3mdgi1"] {
	background-color:white;
	}

	[data-testid="stChatInputTextArea"] {
	background-color:gray; color:white;
	}

	[data-testid="stChatInputTextArea"]::placeholder {
	color:white;
	}

	[data-testid="stHeader"] {
	background-color: rgba(0, 0, 0, 0);
	color:gray;
	}
	</style>
	"""
	
	st.markdown(page_css, unsafe_allow_html=True)
	# Side bar title
	st.sidebar.title("Upload Text Files")

	# Define upload files object
	uploaded_files = st.sidebar.file_uploader("choose files",label_visibility='hidden'	, type=["txt"],accept_multiple_files=True)
	
	# Define clear chat button (chat will be cleared only after clicking it)
	
	if st.sidebar.button("Clear chat"):
		st.session_state.messages = []

	# Chat section title
	st.title("Chatbot with context from Textfiles.")
	
	# File uploaded logic
	if uploaded_files:
		file_contents = []
		for file in uploaded_files:
			file_contents.append(file.read().decode("utf-8"))
		context = [f"{file_content}" for _, file_content in enumerate(file_contents)]
		with st.chat_message("ai"):
				st.markdown("You can now ask questions based on the files uploaded: " + ", ".join([file.name  for file in uploaded_files]))
	# Define user input
	user_input = st.chat_input("Ask a question: ")

	# No files uploaded message or user try to enter a prompt while no files were uploaded
	if not uploaded_files or (not uploaded_files and user_input):
		st.session_state.messages = []
		with st.chat_message("ai"):
			st.markdown("No files uploaded, upload files in order to ask questions about them !")
			
	# Write chat history
	if  "messages" not in  st.session_state:
		st.session_state.messages = []
	for message in st.session_state.messages:
			with st.chat_message(name=message["role"], avatar=message["avatar"]):
				st.markdown(message["content"])
	
	# User input logic
	if user_input:
		if uploaded_files:
			# Save user input to chat history
			st.session_state.messages.append({"role":"human","content":user_input,"avatar":"🦁"}) 
			with st.chat_message("human", avatar="🦁"):
				st.markdown(user_input)
			# Args dict to set in the model
			args = {"question": f"{user_input}", "context": "".join(context)}
			# Set args
			handle_ollama.set_args(args=args)

			# Create model chain
			handle_ollama.create_chain()  
			with st.chat_message("ai", avatar="🐻‍❄️"):
				# Get and write model response as a stream
				st.write_stream(handle_ollama.invoke_stream())
			
			# Save model response to chat history
			st.session_state.messages.append({"role":"ai","content":handle_ollama.latest_response, "avatar":"🐻‍❄️"})       
	
	

	

	
