# Platform Engeeniring Project

## Overview

A simple platform for managing environments for a wheather webapp and a DynamoDB database.

## Installation

### Prerequests

* Terraform
* Docker
* Kubectl
* AWS CLI 
* Helm

### Setting up the EKS cluster and the ALB Ingress Controller:

```bash
cd infra
terraform apply
```

Type "yes".

### Install the DynamoDB ACK Serivce Controller:

```bash
bash ack_controller_install.sh
```

### Set up IRSA for the DynamoDB Controller:

* NOTE: The script uses the eksctl docker container command.

```bash
bash ack_irsa.sh
```

### Create DynamoDB table:

```bash
kubectl create -f table.yaml
```

## run platform in venv (dev):

### Install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run platform:
```bash
python3 app.py
```


