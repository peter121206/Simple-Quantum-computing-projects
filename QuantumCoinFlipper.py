from qiskit import QuantumCircuit, execute, Aer

# Create a quantum circuit with one qubit
circuit = QuantumCircuit(1, 1)

# Apply a Hadamard gate to create superposition
circuit.h(0)

# Measure the qubit
circuit.measure(0, 0)

# Simulate the circuit and get the results
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1)
result = job.result()
counts = result.get_counts(circuit)

print("Coin flip result:", list(counts.keys())[0])
