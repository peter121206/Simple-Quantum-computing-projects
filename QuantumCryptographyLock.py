import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer
import random

message = 'secret'

# Determine the number of qubits needed based on the length of the message
n = len(message)

# Create quantum and classical registers for qubits and measurement results
qr = QuantumRegister(n, name='qr')
cr = ClassicalRegister(n, name='cr')

# Alice creates a quantum circuit
alice = QuantumCircuit(qr, cr, name='Alice')

# Generate a random binary key for Alice
alice_key = bin(random.randint(0, 2**n - 1))[2:].zfill(n)
# Apply X gate to qubits based on the binary key
for index, digit in enumerate(alice_key):
    if digit == '1':
        alice.x(qr[index])

# Generate a random table to determine basis (X or Z) for each qubit
alice_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        alice.h(qr[index])
        alice_table.append('X')
    else:
        alice_table.append('Z')

# Function to send Alice's state to Bob's circuit
def SendState(qc1, qc2, qc1_name):
    # Retrieve the quantum state of qc1 in qasm code
    qs = qc1.qasm().split(sep=';')[4:-1]
    for index, instruction in enumerate(qs):
        qs[index] = instruction.lstrip()
    for instruction in qs:
        # Apply the instructions to qc2 to replicate Alice's state
        if instruction[0] == 'x':
            old_qr = int(instruction[5:-1])
            qc2.x(qr[old_qr])
        elif instruction[0] == 'h':
            old_qr = int(instruction[5:-1])
            qc2.h(qr[old_qr])
        elif instruction[0] == 'm':
            pass
        else:
            raise Exception('Unable to parse instruction')

# Bob creates a quantum circuit
bob = QuantumCircuit(qr, cr, name='Bob')

# Bob receives Alice's state by applying the SendState function
SendState(alice, bob, 'Alice')

# Generate a random table for Bob to determine basis (X or Z) for each qubit
bob_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        bob.h(qr[index])
        bob_table.append('X')
    else:
        bob_table.append('Z')

# Measure all qubits in Bob's circuit
for index in range(len(qr)):
    bob.measure(qr[index], cr[index])

# Execute the quantum circuit on a simulator backend
backend = BasicAer.get_backend('qasm_simulator')
result = execute(bob, backend=backend, shots=1).result()

# Retrieve Bob's key from the measurement result
bob_key = list(result.get_counts(bob))[0]
bob_key = bob_key[::-1]  # Reverse the key

# Compare Alice's and Bob's tables to determine which qubits to keep or discard
keep = []
discard = []
for qubit, basis in enumerate(zip(alice_table, bob_table)):
    if basis[0] == basis[1]:
        keep.append(qubit)
    else:
        discard.append(qubit)

# Compare Alice's and Bob's keys to calculate the similarity
acc = 0
for bit in zip(alice_key, bob_key):
    if bit[0] == bit[1]:
        acc += 1

# Create new keys for Alice and Bob based on the qubits to keep
new_alice_key = [alice_key[qubit] for qubit in keep]
new_bob_key = [bob_key[qubit] for qubit in keep]
# Compare the new keys for similarity
acc = 0
for bit in zip(new_alice_key, new_bob_key):
    if bit[0] == bit[1]:
        acc += 1

# Calculate the percentage of similarity between the new keys
similarity = acc / len(new_alice_key)
print('Percentage of similarity between the keys:', similarity)

# Check if the key exchange was successful or tampered
if similarity == 1:
    print("Key exchange has been successful")
    print("New Alice's key:", new_alice_key)
    print("New Bob's key:", new_bob_key)
    
else:
    print("Key exchange has been tampered! Check for eavesdropper or try again")
    print("New Alice's key is invalid:", new_alice_key)
    print("New Bob's key is invalid:", new_bob_key)
