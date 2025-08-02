```markdown
# Repository Summary: Rudra-Garg/CS300

1.  **Project Goal & Core Functionality:**
    *   The project simulates a fog/edge computing environment for processing EEG data from mobile devices, distributing processing tasks across mobile, gateway, proxy, and cloud tiers. The goal is to analyze EEG data to determine concentration levels.
    *   Key features:
        *   Modular processing of EEG data (Client, Calculator, Connector modules).
        *   Simulated network latency and packet loss.
        *   Prometheus-based monitoring and Grafana dashboards.

2.  **Technology Stack:**
    *   **Languages:** Python (primarily for backend services and simulation).
    *   **Frameworks/Libraries:** Flask (for the mobile, gateway, proxy, and cloud applications), NumPy, Prometheus client, and Flask-Prometheus-Metrics.
    *   **Key Dependencies:** Prometheus, Grafana, Loki, Promtail are used for monitoring and logging. `psutil` is used for CPU monitoring.
    *   **Infrastructure/Ops:** Docker (defined in `Dockerfile` for each service), Docker Compose (defined in `docker-compose.yaml`), Nginx (used in the `proxy` and `cloud` services).

3.  **Repository Structure Overview (Based on `tree.txt` if available, otherwise inferred):**
    *   `.idea/`: Contains IntelliJ IDEA project settings (e.g., modules, inspection profiles, VCS configuration).
    *   `.vscode/`: Contains Visual Studio Code settings (e.g., cSpell words).
    *   `cloud/`: Contains the Dockerfile and Nginx configuration for the cloud service.
    *   `cloud_py/`: Contains the Python code and requirements for the cloud application.
    *   `config/`: Contains configurations for Grafana, Loki, and Prometheus. Also includes example config files for network and application simulation such as Config-1.json
    *   `gateway/`: Contains the Dockerfile, Python code, and entrypoint script for the gateway service.
    *   `mobile/`: Contains the Dockerfile, Python code, and entrypoint script for the mobile client.
    *   `proxy/`: Contains the Dockerfile, Nginx configuration, and entrypoint script for the proxy service.
    *   `proxy_py/`: Contains the Python code and entrypoint script for the proxy application.
    *   `shared_modules/`: Contains shared Python modules (client, calculator, connector, metrics, cpu_monitor) used by multiple services.
    *   Root: Contains base requirements.txt, `docker-compose.yaml`, `.gitignore`, `.env`.

4.  **Key Files & Entry Points:**
    *   Configuration files: `docker-compose.yaml`, `.env`, `config/prometheus.yml`, `config/grafana.ini`, `config/loki-config.yaml`, `config/promtail-config.yaml`, `config/grafana-provisioning/dashboards/main.yaml`, `cloud/nginx.conf`, `proxy/nginx.conf`, `config/Config-1.json`
    *   Application entry points: `mobile/mobile.py`, `gateway/gateway.py`, `proxy_py/proxy_app.py`, `cloud_py/cloud_app.py`
    *   Build/deployment-related files: `Dockerfile` files in each service directory, `docker-compose.yaml`
    *   Key application logic files: `shared_modules/client_module.py`, `shared_modules/concentration_calculator_module.py`, `shared_modules/connector_module.py`, `shared_modules/metrics.py`, `shared_modules/cpu_monitor.py`.
    *   Documentation: No specific `README.md` was provided in the input.

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Run `docker-compose up --build`.
    *   **Running:** The application runs via Docker Compose.
    *   **Building:** Docker images are built using `docker-compose up --build`.
    *   **Deployment:** Deployment is managed by `docker-compose.yaml`, defining networks, ports, resource limits, dependencies, and environment variables for each service.
    *   **Testing:** Health checks are defined for each service in the `docker-compose.yaml` file.
    *   *Constraint:* No specific testing mechanisms other than healthchecks are apparent.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Component-based architecture with modular Python code.
    *   Use of environment variables for configuration (e.g., `ENABLE_LATENCY`, `PROXY_URL`, `CLOUD_URL`, `MOBILE_PROCESSING_LEVEL`, `GATEWAY_PROCESSING_LEVEL`, `PROXY_PROCESSING_LEVEL`, `CLOUD_PROCESSING_LEVEL`).
    *   Consistent use of `entrypoint.sh` scripts to apply `tc` (traffic control) rules for latency simulation before launching the main application.
    *   Centralized logging using `json-file` driver with size limits, and monitoring using Prometheus, Loki, and Grafana.

7.  **Overall Impression & Potential Use Case:**
    *   This is a simulation environment for evaluating fog/edge computing architectures for real-time EEG data processing, focusing on analyzing processing distribution, latency, and CPU utilization across different tiers (mobile, gateway, proxy, cloud).
```