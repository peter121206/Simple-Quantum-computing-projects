from qiskit import QuantumCircuit, execute, Aer

# Create a quantum circuit with two qubits
circuit = QuantumCircuit(2, 2)

# Alice generates a random key and encodes the message
key = [0, 1]  # Example key
message = 'SECRET'  # Example message

circuit.h(0)
circuit.cx(0, 1)
circuit.barrier()

# Alice sends the qubits to Bob over a quantum channel

# Bob receives the qubits and decodes the message
circuit.barrier()
circuit.cx(0, 1)
circuit.h(0)
circuit.measure([0, 1], [0, 1])

# Simulate the circuit and get the results
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1)
result = job.result()
counts = result.get_counts(circuit)

# Bob retrieves the message using the shared key
decrypted_message = ''.join([message[i] if key[i] == int(list(counts.keys())[0][::-1]) else 'X' for i in range(len(message))])

print("Decrypted message:", decrypted_message)
