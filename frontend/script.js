document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const tokenBtn = document.getElementById('token-btn');

    // Optional token handling: user can set one if desired, but it is not mandatory
    if (tokenBtn) {
        tokenBtn.addEventListener('click', () => {
            const current = sessionStorage.getItem('agent_api_token') || '';
            const updated = prompt('Optional Agent API Token (press Cancel to skip):', current);
            if (updated !== null) {
                const trimmed = updated.trim();
                if (trimmed) {
                    sessionStorage.setItem('agent_api_token', trimmed);
                    appendMessage('API Token saved in session.', 'system');
                } else {
                    sessionStorage.removeItem('agent_api_token');
                    appendMessage('API Token cleared. Direct access active.', 'system');
                }
            }
        });
    }

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

        // Optional token if configured, otherwise direct access
        const token = sessionStorage.getItem('agent_api_token');
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: headers,
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
