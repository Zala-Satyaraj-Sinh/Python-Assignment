import heapq


def main():
    w, n = map(int, input().split())

    jobs = []

    for order in range(n):
        arrival, job_id, priority, duration, resources = input().split()

        arrival = int(arrival)
        priority = int(priority)
        duration = int(duration)
        resources = int(resources)

        jobs.append((arrival, order, job_id, priority, duration, resources))

    # Sort by arrival time
    jobs.sort(key=lambda x: (x[0], x[1]))

    # Worker heap: (available_time, worker_id)
    workers = []

    for i in range(1, w + 1):
        heapq.heappush(workers, (0, i))

    # Waiting job heap:
    # (-priority, arrival_time, arrival_order, job_id, duration, resources)
    waiting = []

    results = []
    total_wait = 0

    job_index = 0
    current_time = 0

    while job_index < n or waiting:

        # If no jobs are waiting, move time to the next arrival
        if not waiting:
            current_time = max(current_time, jobs[job_index][0])

        # Add all jobs that have arrived
        while job_index < n and jobs[job_index][0] <= current_time:
            arrival, order, job_id, priority, duration, resources = jobs[job_index]

            heapq.heappush(
                waiting,
                (-priority, arrival, order, job_id, duration, resources)
            )

            job_index += 1

        # If no worker is available, move to the next worker completion
        if workers[0][0] > current_time:
            current_time = workers[0][0]

            # Add jobs that arrived during this time
            while job_index < n and jobs[job_index][0] <= current_time:
                arrival, order, job_id, priority, duration, resources = jobs[job_index]

                heapq.heappush(
                    waiting,
                    (-priority, arrival, order, job_id, duration, resources)
                )

                job_index += 1

        # Assign jobs to available workers
        while waiting and workers[0][0] <= current_time:

            available_time, worker_id = heapq.heappop(workers)

            _, arrival, order, job_id, duration, resources = heapq.heappop(waiting)

            start_time = max(current_time, available_time)
            finish_time = start_time + duration

            wait_time = start_time - arrival
            total_wait += wait_time

            results.append(
                (start_time, worker_id, job_id, finish_time)
            )

            heapq.heappush(
                workers,
                (finish_time, worker_id)
            )

            # Add jobs that arrived while assigning
            while job_index < n and jobs[job_index][0] <= current_time:
                a, o, jid, p, d, r = jobs[job_index]

                heapq.heappush(
                    waiting,
                    (-p, a, o, jid, d, r)
                )

                job_index += 1

        # Move time forward if jobs are still waiting
        if waiting and workers[0][0] > current_time:
            current_time = workers[0][0]

    # Print in execution/start-time order
    results.sort(key=lambda x: (x[0], x[1]))

    for start_time, worker_id, job_id, finish_time in results:
        print(job_id, f"W{worker_id}", start_time, finish_time)

    average_wait = total_wait / n
    print(f"AVG_WAIT {average_wait:.2f}")


if __name__ == "__main__":
    main()