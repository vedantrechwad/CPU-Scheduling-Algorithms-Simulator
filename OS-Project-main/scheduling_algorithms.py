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

def fcfs(processes):
    # Convert input processes to Process objects
    process_objects = [Process(p['pid'], p['arrival_time'], p['burst_time']) for p in processes]
    
    # Sort processes by arrival time
    process_objects.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    timeline = []
    
    for process in process_objects:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            
        timeline.append({
            'pid': process.pid,
            'start': current_time,
            'end': current_time + process.burst_time
        })
        
        process.completion_time = current_time + process.burst_time
        current_time = process.completion_time
        
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    
    # Calculate averages
    avg_turnaround = sum(p.turnaround_time for p in process_objects) / len(process_objects)
    avg_waiting = sum(p.waiting_time for p in process_objects) / len(process_objects)
    
    return {
        'timeline': timeline,
        'processes': [{
            'pid': p.pid,
            'arrival_time': p.arrival_time,
            'burst_time': p.burst_time,
            'completion_time': p.completion_time,
            'turnaround_time': p.turnaround_time,
            'waiting_time': p.waiting_time
        } for p in process_objects],
        'averages': {
            'turnaround_time': round(avg_turnaround, 2),
            'waiting_time': round(avg_waiting, 2)
        }
    }

def srtn(processes):
    # Convert input processes to Process objects
    process_objects = [Process(p['pid'], p['arrival_time'], p['burst_time']) for p in processes]
    
    # Sort processes by arrival time
    process_objects.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    timeline = []
    ready_queue = []
    completed = 0
    
    while completed < len(process_objects):
        # Add arrived processes to ready queue
        for process in process_objects:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                if process not in ready_queue:
                    ready_queue.append(process)
        
        if not ready_queue:
            current_time += 1
            continue
            
        # Sort ready queue by remaining time
        ready_queue.sort(key=lambda x: x.remaining_time)
        current_process = ready_queue[0]
        
        # Execute for 1 unit of time
        timeline.append({
            'pid': current_process.pid,
            'start': current_time,
            'end': current_time + 1
        })
        
        current_process.remaining_time -= 1
        current_time += 1
        
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed += 1
            ready_queue.remove(current_process)
    
    # Calculate averages
    avg_turnaround = sum(p.turnaround_time for p in process_objects) / len(process_objects)
    avg_waiting = sum(p.waiting_time for p in process_objects) / len(process_objects)
    
    return {
        'timeline': timeline,
        'processes': [{
            'pid': p.pid,
            'arrival_time': p.arrival_time,
            'burst_time': p.burst_time,
            'completion_time': p.completion_time,
            'turnaround_time': p.turnaround_time,
            'waiting_time': p.waiting_time
        } for p in process_objects],
        'averages': {
            'turnaround_time': round(avg_turnaround, 2),
            'waiting_time': round(avg_waiting, 2)
        }
    }

def round_robin(processes, quantum):
    # Convert input processes to Process objects
    process_objects = [Process(p['pid'], p['arrival_time'], p['burst_time']) for p in processes]
    
    # Sort processes by arrival time
    process_objects.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    timeline = []
    ready_queue = []
    completed = 0
    
    while completed < len(process_objects):
        # Add arrived processes to ready queue
        for process in process_objects:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                if process not in ready_queue:
                    ready_queue.append(process)
        
        if not ready_queue:
            current_time += 1
            continue
            
        current_process = ready_queue.pop(0)
        execution_time = min(quantum, current_process.remaining_time)
        
        timeline.append({
            'pid': current_process.pid,
            'start': current_time,
            'end': current_time + execution_time
        })
        
        current_process.remaining_time -= execution_time
        current_time += execution_time
        
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed += 1
        else:
            ready_queue.append(current_process)
    
    # Calculate averages
    avg_turnaround = sum(p.turnaround_time for p in process_objects) / len(process_objects)
    avg_waiting = sum(p.waiting_time for p in process_objects) / len(process_objects)
    
    return {
        'timeline': timeline,
        'processes': [{
            'pid': p.pid,
            'arrival_time': p.arrival_time,
            'burst_time': p.burst_time,
            'completion_time': p.completion_time,
            'turnaround_time': p.turnaround_time,
            'waiting_time': p.waiting_time
        } for p in process_objects],
        'averages': {
            'turnaround_time': round(avg_turnaround, 2),
            'waiting_time': round(avg_waiting, 2)
        }
    }

def priority(processes):
    # Convert input processes to Process objects
    process_objects = [Process(p['pid'], p['arrival_time'], p['burst_time'], p['priority']) for p in processes]
    
    # Sort processes by arrival time
    process_objects.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    timeline = []
    ready_queue = []
    completed = 0
    
    while completed < len(process_objects):
        # Add arrived processes to ready queue
        for process in process_objects:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                if process not in ready_queue:
                    ready_queue.append(process)
        
        if not ready_queue:
            current_time += 1
            continue
            
        # Sort ready queue by priority (lower number = higher priority)
        ready_queue.sort(key=lambda x: x.priority)
        current_process = ready_queue.pop(0)
        
        timeline.append({
            'pid': current_process.pid,
            'start': current_time,
            'end': current_time + current_process.remaining_time
        })
        
        current_time += current_process.remaining_time
        current_process.remaining_time = 0
        current_process.completion_time = current_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        completed += 1
    
    # Calculate averages
    avg_turnaround = sum(p.turnaround_time for p in process_objects) / len(process_objects)
    avg_waiting = sum(p.waiting_time for p in process_objects) / len(process_objects)
    
    return {
        'timeline': timeline,
        'processes': [{
            'pid': p.pid,
            'arrival_time': p.arrival_time,
            'burst_time': p.burst_time,
            'completion_time': p.completion_time,
            'turnaround_time': p.turnaround_time,
            'waiting_time': p.waiting_time
        } for p in process_objects],
        'averages': {
            'turnaround_time': round(avg_turnaround, 2),
            'waiting_time': round(avg_waiting, 2)
        }
    }

def sjf(processes):
    # Convert input processes to Process objects
    process_objects = [Process(p['pid'], p['arrival_time'], p['burst_time']) for p in processes]
    
    # Sort processes by arrival time
    process_objects.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    timeline = []
    ready_queue = []
    completed = 0
    
    while completed < len(process_objects):
        # Add arrived processes to ready queue
        for process in process_objects:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                if process not in ready_queue:
                    ready_queue.append(process)
        
        if not ready_queue:
            current_time += 1
            continue
            
        # Sort ready queue by burst time
        ready_queue.sort(key=lambda x: x.remaining_time)
        current_process = ready_queue.pop(0)
        
        timeline.append({
            'pid': current_process.pid,
            'start': current_time,
            'end': current_time + current_process.remaining_time
        })
        
        current_time += current_process.remaining_time
        current_process.remaining_time = 0
        current_process.completion_time = current_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        completed += 1
    
    # Calculate averages
    avg_turnaround = sum(p.turnaround_time for p in process_objects) / len(process_objects)
    avg_waiting = sum(p.waiting_time for p in process_objects) / len(process_objects)
    
    return {
        'timeline': timeline,
        'processes': [{
            'pid': p.pid,
            'arrival_time': p.arrival_time,
            'burst_time': p.burst_time,
            'completion_time': p.completion_time,
            'turnaround_time': p.turnaround_time,
            'waiting_time': p.waiting_time
        } for p in process_objects],
        'averages': {
            'turnaround_time': round(avg_turnaround, 2),
            'waiting_time': round(avg_waiting, 2)
        }
    } 