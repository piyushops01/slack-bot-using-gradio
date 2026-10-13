import gradio as gr


def chatbot(message):
    return f"Gradio received your message: {message}"


demo = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(),
    outputs=gr.Textbox(),
    api_name="predict"
)


if __name__ == "__main__":
    print("Starting Gradio app...")
    demo.launch()