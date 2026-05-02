// Modals
function openTaskModal(assignee = '', date = '') {
    const modal = document.getElementById('taskModal');
    if (assignee) document.getElementById('modalAssignee').value = assignee;
    if (date) document.getElementById('modalDate').value = date;
    modal.classList.add('active');
}

function openHelpModal() {
    document.getElementById('helpContextInput').value = '';
    document.getElementById('helpMatchResultContainer').style.display = 'none';
    document.getElementById('helpModal').classList.add('active');
}

function findHelpMatch() {
    const input = document.getElementById('helpContextInput').value.trim().toLowerCase();
    if (!input) {
        alert("Please enter what you need help with.");
        return;
    }

    if (!window.TEAM_DATA) return;

    // Split input into keywords
    const keywords = input.split(/[\s,]+/);

    let bestMatch = null;
    let minLoad = Infinity;

    window.TEAM_DATA.forEach(member => {
        // Skip if on leave or load is 100 or more
        if (member.on_leave || member.load_score >= 100) return;

        const context = member.context_tags ? member.context_tags.toLowerCase() : "";
        let isMatch = false;

        // Check if any keyword matches their context tags
        for (let word of keywords) {
            if (word.length > 2 && context.includes(word)) {
                isMatch = true;
                break;
            }
        }

        // If matched or if no specific match but we need *someone* fallback
        // We'll require a strict match if possible, otherwise if no strict match, we could fallback,
        // but user requested "the person should have knowledge of the help required".
        // So we strictly require `isMatch` to be true.
        if (isMatch) {
            if (member.load_score < minLoad) {
                minLoad = member.load_score;
                bestMatch = member;
            }
        }
    });

    const container = document.getElementById('helpMatchResultContainer');
    const content = document.getElementById('helpMatchContent');

    if (bestMatch) {
        content.innerHTML = `
            <img src="${bestMatch.avatar_url}" style="width: 40px; height: 40px; border-radius: 50%;">
            <div style="flex: 1;">
                <div style="font-weight: 600;">${bestMatch.name}</div>
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Expert in: ${bestMatch.context_tags}. Load: ${bestMatch.load_score}%</div>
            </div>
            <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;">Schedule Slot</button>
        `;
        container.style.display = 'block';
    } else {
        content.innerHTML = `
            <div style="flex: 1; text-align: center; color: var(--warning); padding: 8px;">
                No suitable match found with available capacity for that topic.
            </div>
        `;
        container.style.display = 'block';
    }
}

function closeModals(event) {
    if (event && !event.target.classList.contains('modal-overlay')) return;
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModals();
});

// Tab Switching
function switchTab(viewId) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
    
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + viewId).classList.add('active');

    if (viewId === 'pulse-view') {
        setTimeout(renderPulseGraph, 50);
    }
}

// Circular Graph Rendering
function renderPulseGraph() {
    const container = document.getElementById('pulseContainer');
    const svgLayer = document.getElementById('svg-layer');
    
    // Clear previous nodes except center orb & svg
    Array.from(container.children).forEach(child => {
        if (!child.classList.contains('center-orb') && child.id !== 'svg-layer') {
            child.remove();
        }
    });
    svgLayer.innerHTML = '';

    if (!window.TEAM_DATA) return;

    const numNodes = TEAM_DATA.length;
    const radius = 220; // Radius of the circle
    const centerX = container.clientWidth / 2;
    const centerY = container.clientHeight / 2;

    const nodePositions = [];

    // 1. Calculate positions and render nodes
    TEAM_DATA.forEach((member, index) => {
        const angle = (index / numNodes) * 2 * Math.PI - Math.PI / 2; // start from top
        
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        nodePositions.push({ x, y, member });

        // Calculate progress ring
        const r = 34;
        const circ = 2 * Math.PI * r;
        const dash = (member.load_score / 100) * circ;

        // Create HTML for node
        const nodeDiv = document.createElement('div');
        nodeDiv.className = `pulse-node ${member.on_leave ? 'on-leave' : ''}`;
        nodeDiv.style.left = `${x}px`;
        nodeDiv.style.top = `${y}px`;
        nodeDiv.title = `${member.name}: ${member.status_summary}`;

        nodeDiv.innerHTML = `
            <div class="node-avatar-wrapper">
                <img src="${member.avatar_url}" class="node-avatar">
                <svg class="node-ring">
                    <circle class="node-ring-bg" cx="36" cy="36" r="34"></circle>
                    <circle class="node-ring-progress" cx="36" cy="36" r="34" style="stroke-dasharray: ${dash} ${circ}"></circle>
                </svg>
                <div class="node-mood">${member.mood_emoji}</div>
            </div>
            <div class="node-info">
                <div class="node-name">${member.name}</div>
                <div class="node-status">${member.load_score}% Load</div>
            </div>
        `;
        container.appendChild(nodeDiv);
    });

    // 2. Draw connections
    let svgContent = '';
    
    // Draw lines forming a ring between members
    for (let i = 0; i < numNodes; i++) {
        const p1 = nodePositions[i];
        const p2 = nodePositions[(i + 1) % numNodes]; // Connect to next
        
        // If either is on leave, link breaks
        const isBroken = p1.member.on_leave || p2.member.on_leave;
        const lineClass = isBroken ? 'connection-line broken' : 'connection-line';
        
        svgContent += `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" class="${lineClass}"></line>`;
    }
    
    // Draw lines to center orb
    for (let i = 0; i < numNodes; i++) {
        const p = nodePositions[i];
        const isBroken = p.member.on_leave;
        const lineClass = isBroken ? 'connection-line broken' : 'connection-line';
        svgContent += `<line x1="${p.x}" y1="${p.y}" x2="${centerX}" y2="${centerY}" class="${lineClass}" style="opacity: 0.3;"></line>`;
    }

    svgLayer.innerHTML = svgContent;
}

// Re-render on window resize to fix positions
window.addEventListener('resize', () => {
    if (document.getElementById('pulse-view').classList.contains('active')) {
        renderPulseGraph();
    }
});
