# DronDelExperimentation
Welcome to the DronDelExperimentation repository! This repository hosts an implementation of concepts detailed in the paper titled "A Deterministic Search Approach for Solving Stochastic Drone Search and Rescue Planning Without Communication". 
Within this repository, you'll discover essential code for conducting experiments, along with select maps we utilized. These maps are encoded following the specifications outlined in the InstanceFormat file.

The core functionality of this project is centralized in the run.py script, particularly within the run_solver function. This function accepts as parameters: an instance object that specifies the details of a problem, an algorithm chosen by the user, timeout which defines how much time will the code run before it returns the best solution, and a parameter called "return_path". When set to true, this parameter returns the best-found path; when set to false, it generates a CSV file containing run data.

Additionally, run.py includes two auxiliary functions: single_run and multi_run. These serve as examples illustrating how to execute the code. The single_run function is tailored for running a single instance, while multi_run enables the simultaneous execution of multiple instances across different processes.

For comprehensive analysis of instances stored in an encoded format within the maps folder, we utilize the decode_reduced function of a decoder object. This function decodes maps from the designated folder and applies filtering based on user-defined criteria. Please note that timing of procceses is implemented using the 'time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)' function which is only available on UNIX based platforms.

## License

This project is licensed under the MIT License 

