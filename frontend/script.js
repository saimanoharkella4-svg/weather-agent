document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const API_TOKEN = 'default-dev-token'; // Updated to match dashboard tests

    function appendMessage(text, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}`;
        msgDiv.textContent = text;
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return msgDiv;
    }

    function appendLoading() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system loading';
        msgDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return msgDiv;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        userInput.value = '';
        const loadingDiv = appendLoading();

        try {
            const response = await fetch('/agent/invoke', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${API_TOKEN}`
                },
                body: JSON.stringify({ input: text })
            });

            const data = await response.json();
            chatWindow.removeChild(loadingDiv);
            
            if (response.ok) {
                appendMessage(data.output, 'system');
            } else {
                appendMessage(`Error: ${data.detail || 'Something went wrong.'}`, 'system');
            }
        } catch (error) {
            chatWindow.removeChild(loadingDiv);
            appendMessage(`Connection Error: ${error.message}`, 'system');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
