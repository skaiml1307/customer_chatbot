from flask import Flask, request, render_template_string
from chatbot import chatbot_response, normalize_text, match_token, keywords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

chat_history = []

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Customer Service Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ffe6f0; margin: 0; padding: 20px; }
        .chat-container { max-width: 500px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .chat-header { background: #ff99cc; color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; font-size: 18px; }
        .chat-box { padding: 15px; height: 400px; overflow-y: auto; }
        .message { margin: 10px 0; display: flex; align-items: flex-end; }
        .user { justify-content: flex-end; }
        .bot { justify-content: flex-start; }
        .bubble { padding: 10px 15px; border-radius: 20px; max-width: 70%; }
        .user .bubble { background: #ffccdd; color: #000; }
        .bot .bubble { background: #f2f2f2; color: #000; }
        .avatar { width: 40px; height: 40px; margin: 0 10px; }
        form { display: flex; padding: 10px; border-top: 1px solid #ddd; }
        input[type=text] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 20px; }
        input[type=submit] { margin-left: 10px; padding: 10px 20px; border: none; border-radius: 20px; background: #ff99cc; color: white; cursor: pointer; }
        input[type=submit]:hover { background: #ff66b2; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Customer Service Chatbot</div>
        <div class="chat-box" id="chat-box">
            {% for msg in chat_history %}
                <div class="message user">
                    <div class="bubble">{{ msg[0] }}</div>
                    <!-- Baby pink + white cartoon human avatar -->
                    <img src="https://cdn-icons-png.flaticon.com/512/921/921087.png" class="avatar" alt="User" style="background:#ffe6f0; border-radius:50%; padding:5px;">
                </div>
                <div class="message bot">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="avatar" alt="Bot">
                    <div class="bubble">{{ msg[1] }}</div>
                </div>
            {% endfor %}
        </div>
        <form method="post">
            <input type="text" name="message" placeholder="Type your message..." autofocus>
            <input type="submit" value="Send">
        </form>
    </div>

    <script>
        // Auto-scroll to bottom
        window.onload = function() {
            var chatBox = document.getElementById("chat-box");
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // Clear chat after 1 minute if Goodbye appears
        document.querySelector("form").addEventListener("submit", function() {
            setTimeout(() => {
                const bubbles = document.querySelectorAll(".bot .bubble");
                if (bubbles.length > 0) {
                    const lastMsg = bubbles[bubbles.length - 1].innerText;
                    if (lastMsg.includes("Goodbye")) {
                        setTimeout(() => {
                            document.getElementById("chat-box").innerHTML = "";
                        }, 60000); // 1 minute delay
                    }
                }
            }, 400);
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_history
    if request.method == "POST":
        user_message = request.form["message"]
        normalized = normalize_text(user_message)
        if any(match_token(t, keywords["farewell"]) for t in word_tokenize(normalized)):
            response = "Goodbye! Have a great day."
            chat_history.append((user_message, response))
            # Do NOT clear immediately; JS handles clearing after 1 minute
        else:
            response = chatbot_response(user_message)
            chat_history.append((user_message, response))
    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
