import hashlib
import json
from datetime import datetime


# ---------------- BLOCKCHAIN ----------------

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index)
            + self.timestamp
            + json.dumps(self.data, sort_keys=True)
            + self.previous_hash
        )

        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            {"message": "Smart Health Blockchain Started"},
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            data,
            latest_block.hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def display_chain(self):

        for block in self.chain:
            print("\n-----------------------------")
            print("Block Number :", block.index)
            print("Timestamp    :", block.timestamp)
            print("Data         :", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Hash         :", block.hash)


# ---------------- SMART HEALTH SYSTEM ----------------

class SmartHealthSystem:

    def __init__(self):
        self.blockchain = Blockchain()
        self.doctors = {}
        self.patients = {}

    # Doctor registration
    def register_doctor(self):

        doctor_id = input("Enter Doctor ID: ")
        name = input("Enter Doctor Name: ")
        specialization = input("Enter Specialization: ")

        self.doctors[doctor_id] = {
            "name": name,
            "specialization": specialization
        }

        print("\nDoctor registered successfully!")

    # Patient registration
    def register_patient(self):

        patient_id = input("Enter Patient ID: ")
        name = input("Enter Patient Name: ")
        age = input("Enter Age: ")

        self.patients[patient_id] = {
            "name": name,
            "age": age
        }

        print("\nPatient registered successfully!")

    # Online consultation
    def consultation(self):

        patient_id = input("Enter Patient ID: ")
        doctor_id = input("Enter Doctor ID: ")

        if patient_id not in self.patients:
            print("Patient not found!")
            return

        if doctor_id not in self.doctors:
            print("Doctor not found!")
            return

        symptoms = input("Enter Patient Symptoms: ")
        diagnosis = input("Enter Doctor Diagnosis: ")
        prescription = input("Enter Prescription: ")

        data = {
            "patient_id": patient_id,
            "patient_name": self.patients[patient_id]["name"],
            "doctor_id": doctor_id,
            "doctor_name": self.doctors[doctor_id]["name"],
            "specialization":
                self.doctors[doctor_id]["specialization"],
            "symptoms": symptoms,
            "diagnosis": diagnosis,
            "prescription": prescription
        }

        self.blockchain.add_block(data)

        print("\nConsultation completed successfully!")
        print("Medical record stored in blockchain.")

    # Display patient records
    def view_records(self):

        patient_id = input("Enter Patient ID: ")

        found = False

        for block in self.blockchain.chain:

            if block.index == 0:
                continue

            if block.data["patient_id"] == patient_id:

                found = True

                print("\n==============================")
                print("Patient Name :", block.data["patient_name"])
                print("Doctor Name  :", block.data["doctor_name"])
                print("Symptoms     :", block.data["symptoms"])
                print("Diagnosis    :", block.data["diagnosis"])
                print("Prescription :", block.data["prescription"])
                print("Block Hash   :", block.hash)

        if not found:
            print("\nNo medical records found.")

    # Check blockchain
    def verify_blockchain(self):

        if self.blockchain.is_chain_valid():
            print("\nBlockchain is VALID.")
        else:
            print("\nBlockchain has been TAMPERED!")


# ---------------- MAIN PROGRAM ----------------

def main():

    system = SmartHealthSystem()

    while True:

        print("\n")
        print("======================================")
        print(" SMART HEALTH ONLINE CONSULTING SYSTEM")
        print("======================================")
        print("1. Register Doctor")
        print("2. Register Patient")
        print("3. Online Consultation")
        print("4. View Patient Medical Records")
        print("5. Display Blockchain")
        print("6. Verify Blockchain")
        print("7. Exit")
        print("======================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            system.register_doctor()

        elif choice == "2":
            system.register_patient()

        elif choice == "3":
            system.consultation()

        elif choice == "4":
            system.view_records()

        elif choice == "5":
            system.blockchain.display_chain()

        elif choice == "6":
            system.verify_blockchain()

        elif choice == "7":
            print("Thank you!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()