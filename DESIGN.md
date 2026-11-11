# Triage Queue Design

The queue uses a min-heap of `(triage_level, sequence, patient)` entries.
Lower triage numbers have higher priority. The increasing sequence number
preserves FIFO order for patients with the same priority.

A lock protects each heap operation. If one worker enqueues a critical
patient while another calls the next patient, the lock makes those operations
happen one at a time. The critical patient is then first in the next dequeue.

A dequeue removes the patient while holding the lock, so only one worker can
take that queue entry. The worker should mark the patient as called before
releasing the lock; this makes the waiting-to-called transition atomic and
prevents two workers from processing the same queue entry.