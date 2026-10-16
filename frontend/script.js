document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const tokenBtn = document.getElementById('token-btn');

    function getApiToken() {
        let token = sessionStorage.getItem('agent_api_token');
        if (!token) {
            token = prompt('Please enter your Agent API Token:');
            if (token) {
                token = token.trim();
                sessionStorage.setItem('agent_api_token', token);
            }
        }
        return token;
    }

    if (tokenBtn) {
        tokenBtn.addEventListener('click', () => {
            const current = sessionStorage.getItem('agent_api_token') || '';
            const updated = prompt('Enter Agent API Token:', current);
            if (updated !== null) {
                const trimmed = updated.trim();
                if (trimmed) {
                    sessionStorage.setItem('agent_api_token', trimmed);
                    appendMessage('API Token updated in session.', 'system');
                } else {
                    sessionStorage.removeItem('agent_api_token');
                    appendMessage('API Token cleared from session.', 'system');
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

        const token = getApiToken();
        if (!token) {
            appendMessage('Authentication required: Please set your Agent API Token to chat.', 'system');
            return;
        }

        appendMessage(text, 'user');
        userInput.value = '';
        const loadingDiv = appendLoading();

        try {
            const response = await fetch('/agent/invoke', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
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
