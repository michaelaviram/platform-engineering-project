# INSTALLATION OF PYTHON, KUBECTL AND HELM
FROM ubuntu:latest AS setup

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3.12-venv \
    apt-transport-https ca-certificates curl gnupg

# Install kubectl 
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | \
    gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | \
    tee /etc/apt/sources.list.d/kubernetes.list && \
    chmod 644 /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && apt-get install -y kubectl

# Install helm
RUN curl https://baltocdn.com/helm/signing.asc | \
    gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null && \
    apt-get install apt-transport-https --yes && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | \
    tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt-get update && apt-get install helm

RUN useradd platform


# COPY SRC AND INSTALLATION OF PYTHON DEPENDENCIES
FROM setup AS builder

WORKDIR /app
SHELL ["/bin/bash", "-c"]
COPY requirements.txt .
RUN python3 -m venv .venv && source .venv/bin/activate && \
    pip install --upgrade pip && pip install -r requirements.txt
COPY . .


# RUNTIME DIRECTIVES
FROM setup AS runtime
COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
USER platform

CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
EXPOSE 8080/tcp
