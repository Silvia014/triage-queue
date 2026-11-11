from dataclasses import dataclass
from datetime import datetime
from heapq import heappop, heappush
from threading import Lock


@dataclass
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime


class TriageQueue:
    def __init__(self):
        self._heap = []
        self._sequence = 0
        self._lock = Lock()
    def enqueue(self, patient: Patient) -> None:
        if patient.triage_level not in (1, 2, 3):
            raise ValueError("Triage level must be 1, 2, or 3.")

        with self._lock:
            heappush(
                self._heap,
                (patient.triage_level, self._sequence, patient),
            )
            self._sequence += 1

    def dequeue(self) -> Patient | None:
        with self._lock:
            if not self._heap:
                return None

            _, _, patient = heappop(self._heap)
            return patient

    def peek(self) -> Patient | None:
        with self._lock:
            if not self._heap:
                return None

            return self._heap[0][2]

    def list_queue(self) -> list[Patient]:
        with self._lock:
            ordered_entries = sorted(self._heap)
            return [patient for _, _, patient in ordered_entries]

    def stats(self) -> dict[int, int]:
        with self._lock:
            counts = {1: 0, 2: 0, 3: 0}
            for triage_level, _, _ in self._heap:
                counts[triage_level] += 1
            return counts

def show_patient(patient: Patient) -> None:
    print(
        f"{patient.name} | Nivel {patient.triage_level} | "
        f"Llegada: {patient.arrived_at.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )


def main() -> None:
    queue = TriageQueue()

    while True:
        print("\n--- Triage Queue ---")
        print("1. Add patient")
        print("2. Call next patient")
        print("3. View next patient")
        print("4. List waiting patients")
        print("5. View queue statistics")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Patient name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue

            try:
                level = int(input("Triage level (1=critical, 2=urgent, 3=standard): "))
                patient = Patient(
                    name=name,
                    triage_level=level,
                    arrived_at=datetime.now().astimezone(),
                )
                queue.enqueue(patient)
                print("Patient added to the queue.")
            except ValueError as error:
                print(f"Invalid input: {error}")

        elif choice == "2":
            patient = queue.dequeue()
            if patient is None:
                print("There are no patients waiting.")
            else:
                print("Calling next patient:")
                show_patient(patient)

        elif choice == "3":
            patient = queue.peek()
            if patient is None:
                print("There are no patients waiting.")
            else:
                print("Next patient:")
                show_patient(patient)

        elif choice == "4":
            patients = queue.list_queue()
            if not patients:
                print("There are no patients waiting.")
            else:
                for number, patient in enumerate(patients, start=1):
                    print(f"{number}. ", end="")
                    show_patient(patient)

        elif choice == "5":
            counts = queue.stats()
            print("Waiting patients by triage level:")
            for level in (1, 2, 3):
                print(f"Level {level}: {counts[level]}")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Choose one of the listed options.")


if __name__ == "__main__":
    main()