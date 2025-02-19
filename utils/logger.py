from collections import deque

log_file = 'LOG.log'
log_queue = deque(maxlen=50)

def log_message(message):
    log_queue.append(message)
    with open(log_file, 'a') as f:
        f.write('\n'.join(log_queue) + '\n')
    log_queue.clear()