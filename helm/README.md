# Making a helm chart

In this tutorial we will show a simple way of creating a helm chart.
Feel free to use any application you find suitable but in this tutorial we will be using the whoami python application found in tutorials/whoami. 

Prerequisites
- helm
- minikube (or another kubernetes cluster)
- Some app you want to make a chart out of

## Tutorial

Use the following command to create a chart template.

```bash
helm create whoami
```
Helm will create the following layout for you.

```
whoami/
├── charts
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   └── service.yaml
├── .helmignore
├── Chart.yaml
└── values.yaml
```
We can start by editing the **Chart.yaml** and specifying our values. 
We can take a look at what we need to define from [here](https://helm.sh/docs/topics/charts/).

```yaml
apiVersion: v2
name: whoami
description: API that shows information about the running environment
type: application
version: 0.1.0
appVersion: 0.1.6
```

Then we can start editing **values.yaml** to specify our needs. We need to expose our service ports to be apple to connect to it and we also need to setup autoscaling to be highly available. 

```yaml
replicaCount: 1
image:
  repository: verifa/whoami
service:
  type: NodePort
  port: 5000
  nodePort: 30000
containerPort: 5000
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
``` 

We also need to make some changes to the files in *templates/* because we introduced new definitions in the values.yaml that are not in the template.

**service.yaml**

```yaml
ports:
    - port: {{ .Values.service.port }}
      nodePort: {{ .Values.service.nodePort }}
      protocol: TCP
```

Now we should be good to go. We can try to run this locally using the following commands

```bash
kubectl create namespace whoami
helm install whoami --namespace whoami --dry-run --debug ./whoami
```

If we have no issues in the output we get from the "dry run" we can remove the debug options.

```bash
helm upgrade -i whoami --namespace whoami ./whoami
```

Once the pods are up and running you can go visit the app. To get the addresss you can run the following commands.

```bash
export NODE_PORT=$(kubectl get --namespace whoami -o jsonpath="{.spec.ports[0].nodePort}" services whoami)
export NODE_IP=$(kubectl get nodes --namespace whoami -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT
```
