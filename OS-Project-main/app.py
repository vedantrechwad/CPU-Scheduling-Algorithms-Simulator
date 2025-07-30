from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from scheduling_algorithms import fcfs, srtn, round_robin, priority, sjf

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None

def first_fit(processes, blocks):
    allocations = [-1] * len(processes)
    
    for i, process_size in enumerate(processes):
        for j, block_size in enumerate(blocks):
            if block_size >= process_size:
                allocations[i] = j
                blocks[j] -= process_size
                break
    
    return allocations

def best_fit(processes, blocks):
    allocations = [-1] * len(processes)
    block_sizes = blocks.copy()
    
    for i, process_size in enumerate(processes):
        best_fit_index = -1
        best_fit_size = float('inf')
        
        for j, block_size in enumerate(block_sizes):
            if block_size >= process_size and block_size < best_fit_size:
                best_fit_index = j
                best_fit_size = block_size
        
        if best_fit_index != -1:
            allocations[i] = best_fit_index
            block_sizes[best_fit_index] -= process_size
    
    return allocations

def worst_fit(processes, blocks):
    allocations = [-1] * len(processes)
    block_sizes = blocks.copy()
    
    for i, process_size in enumerate(processes):
        worst_fit_index = -1
        worst_fit_size = -1
        
        for j, block_size in enumerate(block_sizes):
            if block_size >= process_size and block_size > worst_fit_size:
                worst_fit_index = j
                worst_fit_size = block_size
        
        if worst_fit_index != -1:
            allocations[i] = worst_fit_index
            block_sizes[worst_fit_index] -= process_size
    
    return allocations

def is_safe_state(processes, available):
    n = len(processes)
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    
    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i]:
                can_allocate = True
                for j in range(len(available)):
                    if processes[i][j] > work[j]:
                        can_allocate = False
                        break
                
                if can_allocate:
                    for j in range(len(available)):
                        work[j] += processes[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        
        if not found:
            break
    
    return len(safe_sequence) == n, safe_sequence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'algorithm' not in data or 'processes' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        algorithm = data['algorithm']
        processes = data['processes']
        quantum = data.get('quantum')
        
        # Validate processes
        if not processes:
            return jsonify({'error': 'No processes provided'}), 400
            
        # Validate quantum for Round Robin
        if algorithm == 'round_robin' and (not quantum or quantum < 1):
            return jsonify({'error': 'Invalid time quantum for Round Robin'}), 400
            
        # Process the scheduling algorithm
        if algorithm == 'fcfs':
            result = fcfs(processes)
        elif algorithm == 'srtn':
            result = srtn(processes)
        elif algorithm == 'round_robin':
            result = round_robin(processes, quantum)
        elif algorithm == 'priority':
            result = priority(processes)
        elif algorithm == 'sjf':
            result = sjf(processes)
        else:
            return jsonify({'error': 'Invalid algorithm selected'}), 400
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in simulate route: {str(e)}")
        return jsonify({'error': str(e)}), 400

# For local development
if __name__ == '__main__':
    app.run(debug=True) 