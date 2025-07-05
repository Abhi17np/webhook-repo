function fetchEvents() {
    fetch('/events')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('events');
            container.innerHTML = '';
            data.forEach(event => {
                let text = '';
                if (event.event_type === 'push') {
                    text = `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
                } else if (event.event_type === 'pull_request') {
                    text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                } else if (event.event_type === 'merge') {
                    text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                }
                const div = document.createElement('div');
                div.className = 'event';
                div.textContent = text;
                container.appendChild(div);
            });
        });
}

setInterval(fetchEvents, 15000);
window.onload = fetchEvents;
