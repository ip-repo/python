from langchain_community.llms import Ollama
import gradio as gr
import os

def create_models_list():
    """
    This function create a list froom the models that are available
    on the user Ollama.
    """
    models = os.popen("ollama list").read().split("\n")
    models_list = []
 
    for model_line in models[1:]:

        models_list.append(model_line.split(":")[0])
    return [elem for elem in models_list if elem]

def process_choice(model: str,keywords: str)-> str: 
    """
    This function get a model name(str) and keywords (str)
    and reutrn a one liner joke.
    """   
    if len(keywords) == 0:
        keywords="moon,earth,clown, car, snake, mountain, village, photo, computer, boring, lazy."
    # You can alter the prompt the get different results.
    return Ollama(model=model.strip()).invoke(f"Generate a one-liner joke, here are some keywords: {keywords}.Make sure to use at least one keyword.")

if __name__ == "__main__":
    models_list = create_models_list()
    with gr.Blocks(css=".gradio-container {background-color: lightgray}",theme=gr.themes.Soft(primary_hue="red", secondary_hue="blue")) as joker:
        dropdown = gr.Dropdown(label="Choose model",allow_custom_value=False,choices=models_list,value=models_list[0])
        keyword = gr.Textbox(label = "Add keywords")
        output = gr.Textbox(label="Output Box")
        greet_btn = gr.Button("Make me laugh",)
        greet_btn.click(fn=process_choice, inputs=[dropdown,keyword], outputs=output, api_name="greet")

    joker.launch()
