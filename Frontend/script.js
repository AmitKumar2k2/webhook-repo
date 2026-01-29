let isConnected = false;
let lastUpdateTime = null;

function updateStatus(connected) {
    const statusEl = document.getElementById('status');
    const statusText = statusEl.querySelector('span');

    isConnected = connected;

    if (connected) {
        statusEl.className = 'status connected';
        statusText.textContent = 'Connected';
    } else {
        statusEl.className = 'status disconnected';
        statusText.textContent = 'Disconnected';
    }
}

function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
    });
}

function formatEventMessage(event) {
    const author = `<span class="author">${event.author}</span>`;
    const timestamp = formatTimestamp(event.timestamp);

    switch (event.action) {
        case 'push':
            return `${author} pushed to <span class="branch">${event.to_branch}</span> on ${timestamp}`;
        case 'pull_request':
            return `${author} submitted a pull request from <span class="branch">${event.from_branch}</span> to <span class="branch">${event.to_branch}</span> on ${timestamp}`;
        case 'merge':
            return `${author} merged branch <span class="branch">${event.from_branch}</span> to <span class="branch">${event.to_branch}</span> on ${timestamp}`;
        default:
            return `${author} performed ${event.action} on ${timestamp}`;
    }
}

function renderEvents(events) {
    const eventsList = document.getElementById('events-list');

    if (!events || events.length === 0) {
        eventsList.innerHTML = `
            <li class="no-events">
                <h3>No events yet</h3>
                <p>Waiting for GitHub activity...</p>
            </li>`;
        return;
    }

    eventsList.innerHTML = events.map(event => `
        <li class="event-item ${event.action}">
            <div class="event-content">
                ${formatEventMessage(event)}
            </div>
        </li>
    `).join('');
}

async function fetchEvents() {
    try {
        const response = await fetch('/api/events');
        if (!response.ok) throw new Error(response.status);

        const events = await response.json();
        renderEvents(events);
        updateStatus(true);

        lastUpdateTime = new Date();
        document.getElementById('last-updated').textContent =
            lastUpdateTime.toLocaleTimeString();
    } catch (error) {
        console.error(error);
        updateStatus(false);
    }
}

// Initial load
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, 15000);

document.addEventListener('DOMContentLoaded', () => {
    console.log('GitHub Activity Monitor loaded');
});
