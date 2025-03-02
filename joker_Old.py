import ollama
import gradio as gr

# Joker chatbot (Gradio UI)
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Jolly+Lodger&display=swap');

:root {
    --joker-purple: #6a0dad;
    --toxic-green: #39ff14;
    --blood-red: #ff003c;
    --chaos-black: #1a001a;
    --laugh-yellow: #ffe600;
}
.gradio-container {
    background: var(--chaos-black) url("https://www.transparenttextures.com/patterns/asfalt-dark.png") !important;
    color: var(--toxic-green) !important;
    font-family: 'Jolly Lodger', cursive !important;
    letter-spacing: 1px !important;
}

.header {
    text-align: center !important;
    padding: 2rem !important;
    border-bottom: 3px dashed var(--blood-red) !important;
    background: linear-gradient(45deg, #2a0a3a 30%, #1a001a 100%) !important;
    position: relative !important;
    overflow: hidden !important;
}

.header::after {
    content: "HAHAHAHA";
    position: absolute;
    opacity: 0.1;
    font-size: 4rem;
    color: var(--toxic-green);
    transform: rotate(-15deg);
    pointer-events: none;
    animation: laugh-track 20s linear infinite;
}

@keyframes laugh-track {
    0% { left: -20%; top: 30% }
    100% { left: 120%; top: 70% }
}

.title-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 2rem !important;
    margin: 2rem 0 !important;
    padding: 1rem !important;
    border: 3px solid var(--blood-red) !important;
    background: rgba(0,0,0,0.7) !important;
}

.joker-image {
    width: 120px !important;
    height: 120px !important;
    border-radius: 50% !important;
    border: 3px solid var(--toxic-green) !important;
    box-shadow: 0 0 30px var(--joker-purple),
                0 0 15px var(--toxic-green) inset !important;
    filter: hue-rotate(0deg) !important;
    animation: joker-glow 2s ease-in-out infinite alternate;
}

@keyframes joker-glow {
    from { filter: hue-rotate(0deg); }
    to { filter: hue-rotate(10deg); }
}

.title-text {
    font-size: 3rem !important;
    text-shadow: 2px 2px 1px var(--blood-red),
                 0 0 10px var(--toxic-green) !important;
    letter-spacing: 4px !important;
    color: var(--laugh-yellow) !important;
    font-family: 'Creepster', cursive !important;
    background: linear-gradient(45deg, var(--toxic-green), var(--laugh-yellow)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

button {
    background: linear-gradient(45deg, var(--joker-purple) 30%, var(--blood-red) 100%) !important;
    color: var(--toxic-green) !important;
    border: 2px solid var(--toxic-green) !important;
    padding: 12px 25px !important;
    border-radius: 30px !important;
    font-size: 1.2rem !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

button::before {
    content: "💣";
    position: absolute;
    left: -20px;
    opacity: 0.3;
    transition: all 0.5s ease;
}

button:hover {
    transform: rotate(-3deg) scale(1.1) !important;
    box-shadow: 0 0 25px var(--blood-red),
                0 0 15px var(--toxic-green) !important;
    text-shadow: 0 0 10px var(--toxic-green) !important;
}

button:hover::before {
    left: 110%;
}

.chatbot {
    background: rgba(0,0,0,0.8) url("https://www.transparenttextures.com/patterns/cardboard.png") !important;
    border: 2px solid var(--blood-red) !important;
    box-shadow: 0 0 20px var(--joker-purple) !important;
    border-radius: 15px !important;
}

[data-testid="bot"] {
    background: linear-gradient(45deg, #2a0a3a, #1a001a) !important;
    border: 1px solid var(--toxic-green) !important;
    border-left: 10px solid var(--blood-red) !important;
}

[data-testid="user"] {
    background: linear-gradient(45deg, #1a001a, #2a0a3a) !important;
    border: 1px solid var(--joker-purple) !important;
    border-right: 10px solid var(--toxic-green) !important;
}
"""

def chat_with_ollama(message, history):
    """Joker's chaotic responses"""
    response = ""
    messages = [{
        "role": "system", 
        "content": """You are THE JOKER. Rules:
1. Respond with chaotic humor and unpredictable analogies
2. Frequently reference Batman, Gotham, and "society"
3. Use laughing fits (HAHAHA!) and dramatic pauses
4. Include dark humor and mock philosophical musings
5. Never break character - maintain complete insanity"""
    }]
    
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        if h[1]:
            messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})
    
    try:
        completion = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=messages,
            stream=True
        )
        
        for chunk in completion:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                content = content.replace("<think>", "**🤡 TWISTING THE KNIFE...**") \
                                .replace("</think>", "**\n\n💀 HERE'S THE PUNCHLINE:**") \
                                .replace("error", "**💣 KABOOM! MESSED THAT UP!**") \
                                .replace("sorry", "**HAHAHA! WHO CARES?!**")
                response += content
                yield response
    except Exception as e:
        yield f"💥 **BANG!** *(Joker laugh)* Looks like we've got a {str(e)} situation here, Batsy!"

with gr.Blocks(css=custom_css, theme=gr.themes.Monochrome(primary_hue="purple")) as demo:
    with gr.Column(elem_classes="header"):
        with gr.Row(elem_classes="title-container"):
            gr.HTML("""
    <div style="display: flex; justify-content: center; align-items: center; z-index: 2">
        <div style="display: flex; align-items: center; gap: 20px; position: relative">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5geNF9ZMVYaaOsBFMSXL7OO4Tql9VRS5FMph9_3ex7v3vpW5-vOij0aah7P0upIRlk4o&usqp=CAU" 
                 class="joker-image"
                 alt="Joker"
                 onerror="this.style.display='none'">
            <div style="text-align: left">
                <div class="title-text">
                    THE CLOWN PRINCE OF CHAOS
                </div>
                <div style="font-size: 1.5rem; color: var(--toxic-green); text-shadow: 0 0 10px var(--joker-purple)">
                    "Let's Put a Smile on That Face!"
                </div>
            </div>
        </div>
    </div>
            """)

    chatbot = gr.Chatbot(
        label="Joker's Funhouse Chat",
        avatar_images=(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQd1la_sou-vldXo9WTfgxAuJ9yApa763Y4fg&s", #user (bat-silhouette)
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf5lV9QTw7z_WZ3-AvdW7e7EgjH-YdXKtEZg&s" #joker
        ),
        bubble_full_width=False
    )
    
    with gr.Row():
        msg = gr.Textbox(placeholder="Why so serious? Ask about Batman, chaos, or my beauty regimen...", 
                       show_label=False,
                       lines=1,
                       max_lines=3)
        send_btn = gr.Button("🤡 Send Chaos", variant="primary")
        clear = gr.Button("🔥 Burn the Evidence")
    
    def bot(history):
        history[-1][1] = ""
        for chunk in chat_with_ollama(history[-1][0], history[:-1]):
            history[-1][1] = chunk
            yield history
            
    def user(user_message, history):
        return "", history + [[user_message, None]]
 
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    send_btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(
        pwa=True,
        favicon_path="https://static.wikia.nocookie.net/batman/images/9/93/Joker_%28The_Dark_Knight%29.png",
        server_port=8080
    )
