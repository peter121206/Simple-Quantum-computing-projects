from qiskit import QuantumCircuit, execute, Aer
from qiskit.algorithms import Grover
from qiskit.circuit.library import ZFeatureMap
from qiskit.algorithms import AmplificationProblem
from qiskit.primitives import Sampler
import numpy as np

# Define the maze as a binary string
maze = "0101010110000010"  # Example maze

# Create the quantum circuit for the oracle
oracle = QuantumCircuit(len(maze))
for i, bit in enumerate(maze):
    if bit == "1":
        oracle.x(i)  # Apply an X gate to the qubit if the corresponding bit is 1

oracle.barrier()  # Add a barrier to the circuit

# Define the target state as the solution
good_state = "0" * len(maze)

# Create the amplification problem with the oracle and target state
problem = AmplificationProblem(oracle, is_good_state=[good_state])

# Create a Grover instance with the oracle
grover = Grover(oracle)

# Construct the Grover's search algorithm circuit for the given problem
circuit = grover.construct_circuit(problem, power=40)  # Perform 40 iterations of Grover's algorithm

# Choose the statevector simulator backend
backend = Aer.get_backend('statevector_simulator')

# Execute the circuit on the chosen backend and obtain the result
job = execute(circuit, backend, shots=1)
result = job.result()

# Retrieve the statevector representing the final quantum state
solution = result.get_statevector()

# Find the index of the state with the highest probability amplitude
solution_index = np.argmax(np.abs(solution.data) ** 2)

# Convert the index to its binary representation and pad with leading zeros
binary_solution = format(solution_index, 'b').zfill(len(maze))

# Print the statevector and binary solution
print("Solution:", solution)
print("Binary Solution:", binary_solution)
