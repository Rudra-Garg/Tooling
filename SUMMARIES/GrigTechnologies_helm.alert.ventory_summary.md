```markdown
# Repository Summary: GrigTechnologies/helm.alert.ventory

1.  **Project Goal & Core Functionality:**
    *   The project appears to be a Helm chart for deploying "alert.ventory," an application focused on alerting and inventory management, based on the `Chart.yaml` description and file names.
    *   Key features include: backend API and worker components, TLS certificate management using cert-manager, and configuration via ConfigMaps.

2.  **Technology Stack:**
    *   **Languages:** YAML, Shell Script.
    *   **Frameworks/Libraries:** Kubernetes, Helm, cert-manager, NGINX Ingress Controller.
    *   **Key Dependencies:** Harbor registry (`harbor.grigtech.io`), Supabase, ZeptoMail, Zoho OAuth, Temporal. These suggest interactions with a Supabase database, sending emails via ZeptoMail, Zoho OAuth for authentication, and Temporal for workflow management.
    *   **Infrastructure/Ops:** Kubernetes, Helm for package management and deployment, potentially using NGINX Ingress Controller for routing and cert-manager for TLS, Harbor for image registry.

3.  **Repository Structure Overview (Based on file analysis):**
    *   `/`: Contains core deployment scripts (`nginx.sh`, `certificate.sh`, `app.sh`), the Helm chart definition (`Chart.yaml`), license information (`LICENSE`), and a basic `README.md`.
    *   `k8s/`: Contains Kubernetes resource definitions for cert-manager configuration (`cluster-issuer.yaml`, `certificate.yaml`).
    *   `templates/`: Contains Helm templates for deploying various backend components, including API and worker deployments, ConfigMaps, services, and ingresses (`backend-api/`, `backend-worker/`).
    *   The repository lacks explicit test files or directories, indicating a focus on deployment and configuration rather than application code testing within the Helm chart itself.

4.  **Key Files & Entry Points:**
    *   Crucial configuration files: `Chart.yaml`, `values.yaml`, `k8s/cluster-issuer.yaml`, `k8s/certificate.yaml`, `templates/backend-api/ingress.yaml`, various `configmap.yaml` files.
    *   Application entry points: This is a Helm chart; the application's entry point is defined in its Docker images, referenced in `values.yaml` (`harbor.grigtech.io/alert.ventory/backend:0.1.1`).
    *   Build/deployment-related files: `nginx.sh`, `certificate.sh`, `app.sh`. These are deployment scripts.
    *   Key application logic files: No application logic files are in this repository. It appears to only contain infrastructure and deployment related files.
    *   The `README.md` provides basic deployment instructions.

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Install Kubernetes and Helm, configure `kubectl` to connect to the target cluster, install cert-manager.
    *   **Running:** Run the deployment scripts in the specified order (`./nginx.sh`, `./certificate.sh`, `./app.sh`).
    *   **Building:** There is no explicit build process in this repository. The assumption is that the application images are built and pushed to the Harbor registry separately.
    *   **Deployment:** Deployment is handled via the shell scripts that deploy the NGINX Ingress controller, cert-manager, and then installs or upgrades the `alert-ventory` helm chart using the provided configurations.
    *   **Testing:** No testing is directly specified in the repository contents.
    *   Secrets and env vars are configured in `values.yaml` and passed to the backend components via ConfigMaps.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Helm charts for Kubernetes deployment, NGINX Ingress Controller for routing, cert-manager for TLS certificate management, ConfigMaps for configuration, Harbor for private container registry, backend split into API and worker components. Usage of various external services: Supabase, ZeptoMail, Zoho OAuth, and Temporal.

7.  **Overall Impression & Potential Use Case:**
    *   This is a Helm chart designed to deploy the "alert.ventory" application on a Kubernetes cluster. It configures ingress, TLS certificates, and the application's backend components, leveraging external services for database, email, authentication, and workflow management.
```