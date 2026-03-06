const API_BASE_URL = window.API_BASE_URL || 'http://localhost:8000';

const QUICK_ACTIONS = [
  'Registration',
  'Tuition fees',
  'Campus map',
  'Scholarships',
  'Dormitories',
  'International Office',
];

const messagesEl = document.getElementById('messages');
const quickActionsEl = document.getElementById('quick-actions');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('message-input');
const clearButtonEl = document.getElementById('clear-chat');
const sendButtonEl = document.getElementById('send-btn');

let sessionId = '';
let isLoading = false;

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function setLoading(loading) {
  isLoading = loading;
  inputEl.disabled = loading;
  sendButtonEl.disabled = loading;
}

function appendMessage(content, sender = 'bot', html = false) {
  const row = document.createElement('div');
  row.className = `message-row ${sender}`;

  const bubble = document.createElement('div');
  bubble.className = `bubble ${sender}`;

  if (html) {
    bubble.innerHTML = content;
  } else {
    bubble.textContent = content;
  }

  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showTyping() {
  const typing = document.createElement('div');
  typing.id = 'typing-indicator';
  typing.className = 'message-row';
  typing.innerHTML = '<div class="typing">NEU Bot is typing...</div>';
  messagesEl.appendChild(typing);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
  document.getElementById('typing-indicator')?.remove();
}

function resetChat() {
  messagesEl.innerHTML = '';
  sessionId = '';
  appendMessage('Hello! I am NEU AI Assistant. How can I help you today?');
}

async function sendMessage(message) {
  if (!message.trim() || isLoading) {
    return;
  }

  appendMessage(message, 'user');
  setLoading(true);
  showTyping();

  try {
    const payload = {
      message,
      session_id: sessionId || undefined,
      language: 'EN',
    };

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    sessionId = data.session_id || sessionId;

    hideTyping();
    appendMessage(data.message || 'No response received.', 'bot', true);
  } catch (error) {
    hideTyping();
    appendMessage('Sorry, I encountered an error. Please try again.');
    console.error(error);
  } finally {
    setLoading(false);
  }
}

function buildQuickActions() {
  quickActionsEl.innerHTML = '';
  for (const action of QUICK_ACTIONS) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'quick-action';
    button.textContent = action;
    button.addEventListener('click', () => {
      sendMessage(action);
    });
    quickActionsEl.appendChild(button);
  }
}

document.getElementById('start-chat-btn').addEventListener('click', () => {
  const hero = document.getElementById('hero-section');
  const chatSection = document.getElementById('chat-section');

  hero.classList.add('hero-exit');
  setTimeout(() => {
    hero.style.display = 'none';
    chatSection.classList.remove('chat-hidden');
    chatSection.scrollIntoView({ behavior: 'smooth' });
  }, 420);
});

formEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (!message) {
    return;
  }

  inputEl.value = '';
  inputEl.style.height = '42px';
  await sendMessage(message);
});

inputEl.addEventListener('keydown', async (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    const message = inputEl.value.trim();
    if (!message) {
      return;
    }

    inputEl.value = '';
    inputEl.style.height = '42px';
    await sendMessage(message);
  }
});

inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = `${Math.min(inputEl.scrollHeight, 130)}px`;
});

clearButtonEl.addEventListener('click', resetChat);

buildQuickActions();
resetChat();




