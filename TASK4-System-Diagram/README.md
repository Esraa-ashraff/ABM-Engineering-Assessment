# Task 4: Scalable System Architecture

## 📌 Overview
This document outlines the architectural design for a distributed, horizontally scalable web automation and scraping system. The core focus of this design is **Resiliency**, **Observability**, and **Asynchronous Task Processing** to handle high-volume data extraction with automated failover mechanisms.

---

## 📊 System Architecture Diagram

The following diagram illustrates the data flow from task ingestion to persistence, including the monitoring and recovery layers.

```mermaid
flowchart TD
    %% Clients
    subgraph Clients["1. Clients / Producers"]
        style Clients fill:#f9f,stroke:#333,stroke-width:2px
        API[REST API Gateway]
        SCHED[Scheduler / Cron Service]
        style API fill:#9f9,stroke:#333,stroke-width:1px
        style SCHED fill:#9f9,stroke:#333,stroke-width:1px
    end

    %% Queue
    subgraph Queue["2. Message Broker (RabbitMQ)"]
        style Queue fill:#ff9,stroke:#333,stroke-width:2px
        direction TB
        EX_IN[Exchange: tasks.fanout]
        Q_SCRAPE[Queue: scrape.tasks]
        Q_CAPTCHA[Queue: captcha.tasks]
        Q_DLQ[Queue: dlq.failed]
        EX_IN --> Q_SCRAPE
        EX_IN --> Q_CAPTCHA
        EX_IN --> Q_DLQ
        style EX_IN fill:#fcf,stroke:#333,stroke-width:1px
        style Q_SCRAPE fill:#ffc,stroke:#333,stroke-width:1px
        style Q_CAPTCHA fill:#ffc,stroke:#333,stroke-width:1px
        style Q_DLQ fill:#fcc,stroke:#333,stroke-width:1px
    end

    %% Workers
    subgraph Workers["3. Worker Pool (Auto-scaled)"]
        style Workers fill:#9ff,stroke:#333,stroke-width:2px
        W1[Scraper Worker 1]
        W2[Scraper Worker 2]
        W3[Captcha Solver Worker]
        WN[Worker N ...]
        style W1 fill:#cff,stroke:#333,stroke-width:1px
        style W2 fill:#cff,stroke:#333,stroke-width:1px
        style W3 fill:#cff,stroke:#333,stroke-width:1px
        style WN fill:#cff,stroke:#333,stroke-width:1px
    end

    %% Storage / Data Layer
    subgraph Storage["4. Distributed Data Layer"]
        style Storage fill:#fcf,stroke:#333,stroke-width:2px
        PG[(PostgreSQL\nResults & Metadata)]
        RD[(Redis\nSession Cache / Rate Limits)]
        S3[(Object Store\nVideos + Screenshots)]
        style PG fill:#fdd,stroke:#333,stroke-width:1px
        style RD fill:#fdd,stroke:#333,stroke-width:1px
        style S3 fill:#fdd,stroke:#333,stroke-width:1px
    end

    %% Monitoring
    subgraph Monitor["5. Monitoring & Observability"]
        style Monitor fill:#ddf,stroke:#333,stroke-width:2px
        PROM[Prometheus]
        GRAF[Grafana Dashboards]
        ALERT[AlertManager]
        ELK[ELK Stack\nCentralized Logs]
        style PROM fill:#ddf,stroke:#333,stroke-width:1px
        style GRAF fill:#ddf,stroke:#333,stroke-width:1px
        style ALERT fill:#ddf,stroke:#333,stroke-width:1px
        style ELK fill:#ddf,stroke:#333,stroke-width:1px
    end

    %% Failover / Recovery
    subgraph Failover["6. Failover & Recovery"]
        style Failover fill:#fdd,stroke:#333,stroke-width:2px
        DLQ_PROC[DLQ Processor\nRetry Logic]
        HB[Health-check Service]
        style DLQ_PROC fill:#fcc,stroke:#333,stroke-width:1px
        style HB fill:#fcc,stroke:#333,stroke-width:1px
    end

    %% Connections
    API -->|Async Job| EX_IN
    SCHED -->|Scheduled Job| EX_IN

    Q_SCRAPE --> W1 & W2 & WN
    Q_CAPTCHA --> W3

    W1 & W2 & W3 -->|Persist| PG
    W1 -->|Cache Session| RD
    W1 -->|Upload Artifacts| S3

    W1 & W2 & W3 -.->|Metrics| PROM
    W1 & W2 & W3 -.->|Structured Logs| ELK

    PROM --> GRAF & ALERT
    ALERT -->|Critical Alert| DEV[On-call Engineer]

    Q_DLQ --> DLQ_PROC
    DLQ_PROC -->|Re-queue| EX_IN
    DLQ_PROC -->|Escalate| ELK

    HB -->|Liveness Probes| Workers
```

---

## ⚙️ Component Descriptions

### 1. Message Distribution (RabbitMQ)
The system leverages **RabbitMQ** to achieve temporal decoupling between request ingestion and execution.
* **Exchange Logic:** Uses a `fanout` exchange to route tasks to specialized queues based on the task type (Scraping vs. Captcha solving).
* **Dead Letter Queue (DLQ):** Tasks that fail after maximum retries are routed to `dlq.failed` for manual inspection or automated escalation, preventing data loss.

### 2. Horizontal Scaling & Worker Pool
* **Worker Isolation:** Scraping and Captcha solving are separated into different pools to optimize resource allocation (as Captcha solving is more compute-intensive).
* **Elasticity:** Workers are containerized via **Docker** and managed by **Kubernetes HPA**, scaling dynamically based on **Queue Depth** (the number of pending tasks).

### 3. Monitoring & Observability Stack
* **System Health & Load:** **Prometheus** scrapes real-time metrics (CPU, RAM, Active Browser Contexts), while **Grafana** provides live visualization of the system's health.
* **Error Logging:** All workers emit structured JSON logs to an **ELK Stack** (Elasticsearch, Logstash, Kibana) for deep-dive debugging and trace analysis.

### 4. Failover & Resiliency Mechanisms
* **Automatic Redelivery:** If a worker node crashes mid-task, RabbitMQ detects the lost connection and automatically re-queues the message for another available worker.
* **State Recovery:** **PostgreSQL** manages structured data with streaming replication, while **Redis** handles ephemeral session states to ensure rapid recovery from node restarts.
* **Self-Healing:** A dedicated **Health-check Service** (Liveness Probes) automatically replaces unhealthy worker pods if a browser memory leak or hung process is detected.

---

## 🚀 Data Flow Summary

The end-to-end task lifecycle follows these steps:

1. **Request:** A client sends a `POST` request to the API Gateway.
2. **Queueing:** The task is validated and pushed to the **RabbitMQ Exchange**.
3. **Execution:** An available **Worker** pulls the task, launches a Playwright session, and handles data extraction or image/video processing.
4. **Persistence:** * Structured data is saved to **PostgreSQL**.
    * Media artifacts (videos/screenshots) are uploaded to **S3**.
    * Execution metrics are pushed to **Prometheus**.
5. **Acknowledge:** Upon successful completion, a `basic_ack` is sent to RabbitMQ to finalize and remove the task from the queue.

---

## 🤖 AI-Human Collaboration (Prompting Methodology)

The system's architecture was refined through a structured, iterative collaboration with LLMs, where I acted as the **Lead Systems Architect**. The process focused on maximizing the potential of the required stack:

### Phase 1: RabbitMQ Architecture Strategy
Instead of simple task passing, I directed the AI to design a sophisticated routing logic using **RabbitMQ**:
* **Prompting Logic:** I instructed the AI to implement a **Fanout Exchange** to decouple different task types (Scraping vs. Captcha) and specifically requested a **Dead Letter Queue (DLQ)** strategy to ensure "Poison Messages" don't cause infinite retry loops.

### Phase 2: Scaling & Data Integrity
I prompted for the integration of specific "Industry-Standard" components to support the message queue:
* **Dynamic Scaling:** I guided the AI to define a **Kubernetes HPA** logic that scales the Worker Pool based on **RabbitMQ Queue Depth** (messages ready) rather than just CPU usage, ensuring the system reacts to workload spikes in real-time.
* **Persistence Layer:** I specifically directed the AI to design a schema that links **RabbitMQ Message IDs** with **PostgreSQL Transactional Records** for full end-to-end traceability.

### Phase 3: Resiliency & Failover Refinement
To ensure the system met the "Failover and Recovery" requirement, I challenged the LLM to provide solutions for specific edge cases:
* **Worker Resilience:** Prompted for a configuration of **Manual Acknowledgments (ACK)** to ensure that if a worker crashes, RabbitMQ automatically re-queues the message.
* **System Health:** Directed the AI to implement **Liveness Probes** that monitor both the Worker process and its heartbeat connection to RabbitMQ.

> **Result:** This collaborative approach allowed for a rapid transition from basic requirements to a robust, enterprise-grade architecture, ensuring that RabbitMQ acts as a reliable backbone for the entire scaling operation.
