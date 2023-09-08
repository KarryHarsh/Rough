import threading

# Define the function you want to execute with arguments
def my_function(arg):
    print(f"Thread {threading.current_thread().name} with argument: {arg}")

# Define a function to create and start threads
def create_threads():
    arguments = [1, 2, 3, 4, 5]  # List of arguments to pass to the function

    # Create and start a thread for each argument
    threads = []
    for arg in arguments:
        thread = threading.Thread(target=my_function, args=(arg,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_threads = 3  # Number of threads you want to run concurrently

    # Create and start the specified number of threads
    for i in range(num_threads):
        thread = threading.Thread(target=create_threads)
        thread.start()

    # Wait for all threads that create and start threads to finish
    for i in range(num_threads):
        thread.join()

    print("All threads have finished.")
  
