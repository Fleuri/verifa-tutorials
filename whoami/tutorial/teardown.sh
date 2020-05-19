#!/bin/bash
kubectl drain minikube --ignore-daemonsets --delete-local-data --force
kubectl delete deployment --all
kubectl delete svc --all
kubectl delete rs --all
kubectl delete rc --all
kubectl uncordon minikube
