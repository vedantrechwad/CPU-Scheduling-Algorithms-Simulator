let currentAlgorithm = '';

document.addEventListener('DOMContentLoaded', function() {
    showLandingPage();
    
    // Add form submission handler
    const form = document.getElementById('processForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const data = collectSchedulingData();
            if (!data) return;

            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Simulating...';
            submitButton.disabled = true;

            // Send data to server
            fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                displayResults(data);
                document.getElementById('results').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
            })
            .finally(() => {
                // Reset button state
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            });
        });
    }
});

function showLandingPage() {
    document.getElementById('landingPage').style.display = 'block';
    document.getElementById('algorithmPages').style.display = 'none';
    currentAlgorithm = '';
}

function backToLanding() {
    showLandingPage();
}

function selectAlgorithm(algorithm) {
    currentAlgorithm = algorithm;
    
    // Update page title
    const titles = {
        'fcfs': 'First Come First Serve (FCFS)',
        'srtn': 'Shortest Remaining Time Next (SRTN)',
        'round_robin': 'Round Robin Scheduling',
        'priority': 'Priority Scheduling',
        'sjf': 'Shortest Job First (SJF)'
    };
    document.getElementById('algorithmTitle').textContent = titles[algorithm];
    
    // Show algorithm implementation page
    document.getElementById('landingPage').style.display = 'none';
    document.getElementById('algorithmPages').style.display = 'block';
    
    // Reset form and results
    document.getElementById('processForm').reset();
    document.getElementById('results').style.display = 'none';
    
    setupSchedulingInputs();
}

function setupSchedulingInputs() {
    const quantumInput = document.getElementById('quantumInput');
    const quantumField = document.getElementById('quantum');
    
    if (currentAlgorithm === 'round_robin') {
        quantumInput.style.display = 'block';
        quantumField.required = true;
    } else {
        quantumInput.style.display = 'none';
        quantumField.required = false;
    }
    
    const processesDiv = document.getElementById('processes');
    processesDiv.innerHTML = '<h6>Processes</h6>';
    
    document.getElementById('processCount').value = '';
}

function updateProcessCount() {
    const countInput = document.getElementById('processCount');
    const count = parseInt(countInput.value);
    
    if (isNaN(count) || count < 1 || count > 10) {
        alert('Please enter a number between 1 and 10');
        countInput.value = '';
        return;
    }
    
    updateSchedulingProcesses(count);
}

function updateSchedulingProcesses(count) {
    const processesDiv = document.getElementById('processes');
    processesDiv.innerHTML = '<h6>Processes</h6>';
    
    for (let i = 0; i < count; i++) {
        const process = document.createElement('div');
        process.className = 'process-entry mb-2 fade-in';
        process.innerHTML = `
            <div class="row">
                <div class="col">
                    <input type="number" class="form-control" id="pid${i}" placeholder="PID" value="${i + 1}" readonly>
                </div>
                <div class="col">
                    <input type="number" class="form-control" id="arrival${i}" placeholder="Arrival Time" required>
                </div>
                <div class="col">
                    <input type="number" class="form-control" id="burst${i}" placeholder="Burst Time" required>
                </div>
                <div class="col priority-input" style="display: ${currentAlgorithm === 'priority' ? 'block' : 'none'}">
                    <input type="number" class="form-control" id="priority${i}" placeholder="Priority" ${currentAlgorithm === 'priority' ? 'required' : ''}>
                </div>
            </div>
        `;
        processesDiv.appendChild(process);
    }
}

function collectSchedulingData() {
    const numProcesses = parseInt(document.getElementById('processCount').value);
    const processes = [];
    const algorithm = currentAlgorithm;
    let quantum = null;

    // Validate number of processes
    if (isNaN(numProcesses) || numProcesses < 1 || numProcesses > 10) {
        alert('Please enter a valid number of processes (1-10)');
        return null;
    }

    // Get quantum value for Round Robin
    if (algorithm === 'round_robin') {
        quantum = parseInt(document.getElementById('quantum').value);
        if (isNaN(quantum) || quantum < 1) {
            alert('Please enter a valid time quantum');
            return null;
        }
    }

    // Collect process data
    for (let i = 0; i < numProcesses; i++) {
        const arrivalTime = parseInt(document.getElementById(`arrival${i}`).value);
        const burstTime = parseInt(document.getElementById(`burst${i}`).value);
        const priority = algorithm === 'priority' ? 
            parseInt(document.getElementById(`priority${i}`).value) : null;

        // Validate process data
        if (isNaN(arrivalTime) || isNaN(burstTime) || 
            arrivalTime < 0 || burstTime < 1) {
            alert(`Please enter valid values for Process ${i + 1}`);
            return null;
        }

        if (algorithm === 'priority' && 
            (isNaN(priority) || priority < 0)) {
            alert(`Please enter a valid priority for Process ${i + 1}`);
            return null;
        }

        processes.push({
            pid: i + 1,
            arrival_time: arrivalTime,
            burst_time: burstTime,
            priority: priority
        });
    }

    // Prepare request data
    const requestData = {
        algorithm: algorithm,
        processes: processes,
        quantum: quantum
    };

    return requestData;
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    // Create timeline visualization
    const timelineContainer = document.createElement('div');
    timelineContainer.className = 'timeline-container';
    
    // Find the maximum time for scaling
    const maxTime = Math.max(...data.timeline.map(t => t.end));
    
    timelineContainer.innerHTML = `
        <h6>Timeline</h6>
        <div class="timeline">
            ${data.timeline.map(entry => `
                <div class="timeline-process" style="left: ${(entry.start / maxTime) * 100}%; width: ${((entry.end - entry.start) / maxTime) * 100}%;">
                    <div class="process-label">P${entry.pid}</div>
                    <div class="process-time">${entry.start} - ${entry.end}</div>
                    <div class="process-duration">Duration: ${entry.end - entry.start}</div>
                </div>
            `).join('')}
        </div>
    `;
    resultsDiv.appendChild(timelineContainer);
    
    // Create process details table
    const tableContainer = document.createElement('div');
    tableContainer.className = 'table-responsive';
    tableContainer.innerHTML = `
        <h6>Process Details</h6>
        <table class="table">
            <thead>
                <tr>
                    <th>Process ID</th>
                    <th>Arrival Time</th>
                    <th>Burst Time</th>
                    <th>Completion Time</th>
                    <th>Turnaround Time</th>
                    <th>Waiting Time</th>
                </tr>
            </thead>
            <tbody>
                ${data.processes.map(process => `
                    <tr>
                        <td>P${process.pid}</td>
                        <td>${process.arrival_time}</td>
                        <td>${process.burst_time}</td>
                        <td>${process.completion_time}</td>
                        <td>${process.turnaround_time}</td>
                        <td>${process.waiting_time}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    resultsDiv.appendChild(tableContainer);
    
    // Create averages section
    const averagesDiv = document.createElement('div');
    averagesDiv.id = 'averages';
    averagesDiv.innerHTML = `
        <h6>Average Times</h6>
        <p>Average Turnaround Time: <span>${data.averages.turnaround_time}</span></p>
        <p>Average Waiting Time: <span>${data.averages.waiting_time}</span></p>
    `;
    resultsDiv.appendChild(averagesDiv);
    
    // Show the results section
    resultsDiv.style.display = 'block';
} 