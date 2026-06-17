// const API = 'http://localhost:8000';
const API = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';

// DOM elements
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const crawlPanel = document.getElementById('crawlPanel');
const chatPanel = document.getElementById('chatPanel');
const urlInput = document.getElementById('urlInput');
const maxPages = document.getElementById('maxPages');
const crawlBtn = document.getElementById('crawlBtn');
const crawlBtnText = document.getElementById('crawlBtnText');
const crawlStatus = document.getElementById('crawlStatus');
const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');
const indexedUrl = document.getElementById('indexedUrl');

// check backend health on load
async function checkHealth() {
    try{
        const res = await fetch(`${API}/health`);
        const data = await res.json();

        setStatus('online', 'completed');

        // If a website was already indexed, go straight to chat
        if (data.chain_ready && data.indexed_url){
            showChat(data.indexed_url);
        }
    } catch (err) {
        setStatus('error', "Backend offline");
    }
}

function setStatus(state, text){
    statusDot.className = `status-dot ${state}`
    statusText.textContent = text;
}

function setCrawlStatus(message, type) {
    crawlStatus.textContent = message;
    crawlStatus.className = `crawl-status ${type}`;
}

function showChat(url) {
    crawlPanel.classList.add('hidden');
    chatPanel.classList.remove('hidden');
    indexedUrl.textContent = url;
}

function showCrawl() {
    chatPanel.classList.add('hidden');
    crawlPanel.classList.remove('hidden');
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-text">
                Website indexed successfully. Ask me anything about it.
            </div>
        </div>
    `;
}

// Crawl a website
crawlBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();

    if (!url) {
        setCrawlStatus('Please enter a URL.', 'error');
        return;
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        setCrawlStatus('URL must start with http:// or https://', 'error');
        return;
    }

    // Disable button, show loading state
    crawlBtn.disabled = true;
    crawlBtnText.textContent = 'Indexing...';
    setCrawlStatus('Crawling website, chunking, embedding... this may take 30-60 seconds.', 'loading');

    try {
        const res = await fetch(`${API}/crawl`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                max_pages: parseInt(maxPages.value) || 10
            })
        });

        const data = await res.json();

        if (!res.ok) {
            setCrawlStatus(`Error: ${data.detail}`, 'error');
            return;
        }

        setCrawlStatus(
            `Indexed ${data.pages_crawled} pages, ${data.chunks_created} chunks. Ready!`,
            'success'
        );

        // Switch to chat after short delay
        setTimeout(() => showChat(url), 1200);

    } catch (err) {
        setCrawlStatus('Failed to connect to backend. Is it running?', 'error');
    } finally {
        crawlBtn.disabled = false;
        crawlBtnText.textContent = 'Index Website';
    }
});

// Add a message bubble to the chat
function addMessage(role, text, sources = []) {
    const msg = document.createElement('div');
    msg.className = `message ${role}`;

    const avatar = role === 'user' ? '👤' : '🤖';

    let sourcesHtml = '';
    if (sources.length > 0) {
        const chips = sources.map(src => {
            const label = src.replace('https://', '').replace('http://', '');
            return `<a href="${src}" target="_blank" class="source-chip" title="${src}">${label}</a>`;
        }).join('');
        sourcesHtml = `<div class="message-sources">${chips}</div>`;
    }

    msg.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">${text}</div>
            ${sourcesHtml}
        </div>
    `;

    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add typing indicator while waiting
function addTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message bot';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

// Send a question
async function sendQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;

    // Add user message
    addMessage('user', question);
    questionInput.value = '';
    sendBtn.disabled = true;
    addTypingIndicator();

    try {
        const res = await fetch(`${API}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await res.json();
        removeTypingIndicator();

        if (!res.ok) {
            addMessage('bot', `Error: ${data.detail}`);
            return;
        }

        addMessage('bot', data.answer, data.sources);

    } catch (err) {
        removeTypingIndicator();
        addMessage('bot', 'Failed to get answer. Is the backend running?');
    } finally {
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

// Send on button click
sendBtn.addEventListener('click', sendQuestion);


// Send on Enter key
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
    }
});

// Reset — clear index and go back to crawl screen
resetBtn.addEventListener('click', async () => {
    try {
        await fetch(`${API}/reset`, { method: 'DELETE' });
    } catch (err) {
        console.error('Reset failed:', err);
    }
    showCrawl();
    urlInput.value = '';
    setCrawlStatus('', '');
});


// Start
checkHealth();