# Chnages needed for the production

The current solution uses APScheduler, and the second section will propose an alternative solution involving Celery with multiple workers for production usecase.

## Current Solution: APScheduler
1. Persistent Store Files: Each instance in a High Availability (HA) setup utilizes a distinct 2. store file. This ensures data persistence.
3. Resilience to Crashes: In case of an instance failure, the system is designed to resume operations by retrieving the same store file, allowing for uninterrupted job continuation.

## Alternative Solution(for production): Celery with Multiple Workers

1. Utilization of Celery: Implementing Celery as an alternative to APScheduler.
2. Multiple Workers for Scalability: Deploying multiple workers within Celery to manage and execute scaling jobs effectively.
3. Enhanced Performance: This approach potentially offers improved performance and scalability compared to the APScheduler-based solution.
