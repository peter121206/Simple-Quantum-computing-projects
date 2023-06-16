from qiskit import QuantumCircuit, execute, Aer

# Create a quantum circuit with two qubits
circuit = QuantumCircuit(2, 2)

# Game instructions:
# Manipulate qubits to match the target state '11' (entangled)

# Player's moves:
circuit.h(0)
circuit.cx(0, 1)

# Measure the qubits
circuit.measure([0, 1], [0, 1])

# Simulate the circuit and get the results
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1)
result = job.result()
outcome = list(result.get_counts(circuit).keys())[0]

if outcome == '11':
    print("Congratulations! You won!")
else:
    print("Oops! Better luck next time!")

