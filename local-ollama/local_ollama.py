from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit
import requests

def get_available_ollama_models(url="http://127.0.0.1:11434/api/tags"):
		"""
		This function get the models list from ollama server

		Args:
			url(str):ollama server request url
		"""
		response = requests.get(url=url)
		output= ""
		for model in response.json()["models"]:
			if "nomic" in model["name"]:
				continue
			output+= model["name"] +","     

		return output


class EasyOllama:
	def __init__(self, model:str="mistral",chat_history: list=[]) -> None:
		"""
		Set ChatOllama model and chat history
		
		Args:
			model(str): model name
			chat_history(list): chat history
		"""
		self.model = ChatOllama(model=model,verbose=True)
		self.chat_history = chat_history

	def set_system_message(self,system_message: str="You a funny pirate that always responde short funny answers.") -> None:
		"""
		Set system message
			system_message(str): define the system message
		"""
		self.chat_history.append(SystemMessage(content=system_message))

	def invoke_model(self,user_prompt: str="how are you?"):
		"""
		Send a prompt to the model and get a response back
		
		Args:
			user_prompt(str): user prompt
		
		Returns:
			response(str): model response
		"""
		self.chat_history.append(HumanMessage(content=user_prompt))    
		response = self.model.invoke(self.chat_history)
		self.chat_history.append(AIMessage(content=response.content))
		return response

	def __repr__(self) -> str:
		return self.chat_history[-1].content
	
class StreamlitUI:
	def __init__(self) -> None:
		modles_list = get_available_ollama_models().split(",")
		self.modles_list = [model  for model in modles_list if model]
		self.selected_model = "none"
		self.easy_ollama = EasyOllama()

	
	def run(self):
		"""
		Run the sreamlit front end.
		"""
		streamlit.title("EasyOllama")
		with streamlit.sidebar:
			with streamlit.form("my_form"):
				streamlit.write("Inside the form")
				self.select_model = streamlit.selectbox(label="Choose model:", options=self.modles_list)
				self.text = streamlit.text_area(label="Enter assitant role", value="a rude bike messenger", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible")
				submitted = streamlit.form_submit_button("Submit")
				
		if  "messages" not in   streamlit.session_state:
				streamlit.session_state.messages = []
		if submitted or self.selected_model == "none":
			if submitted:
				streamlit.session_state.messages = []
			del self.easy_ollama 
			self.selected_model = self.select_model.split(":")[0]
			self.easy_ollama = EasyOllama(model=self.select_model,chat_history=[])
			self.easy_ollama.set_system_message(f"You are {self.text}")
		
		with streamlit.chat_message("ai"):
			streamlit.markdown("Model: " + self.easy_ollama.model.model +"\nRole: " + self.easy_ollama.chat_history[0].content + "\n")

		for message in streamlit.session_state.messages:
		
			with streamlit.chat_message(message["role"]):
				streamlit.markdown(message["content"])
		
		if prompt := streamlit.chat_input("Prompt:"):
			streamlit.session_state.messages.append({"role": "human", "content": prompt})
			with streamlit.chat_message("user"):
				streamlit.markdown(prompt)
		
			with streamlit.chat_message("ai"):
				with streamlit.spinner("Generating response:"):
					response = self.easy_ollama.invoke_model(prompt)
					streamlit.markdown(response.content)
				
			streamlit.session_state.messages.append({"role": "ai", "content": self.easy_ollama.chat_history[-1].content})
			
				
if __name__ == "__main__":
	streamlit_app = StreamlitUI()
	streamlit_app.run()








	
	
	
		
   
