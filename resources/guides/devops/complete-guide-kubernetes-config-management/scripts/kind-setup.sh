#!/bin/bash
# Local test cluster for the guide's manifests (kind).
kind create cluster --name config-demo
kubectl create namespace production
kubectl apply -f manifests/configmap.yaml
kubectl apply -f manifests/secret.yaml
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/rbac.yaml
kubectl -n production get configmaps,secrets,deploy
