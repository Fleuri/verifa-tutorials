# Introduction to Flux

In this tutorial, you will:

1. Install and set up Flux with Helm
2. Commit a change to a git repository
3. Observe flux auto-deploying your changes

## 0. Before you start

This tutorial is based on the one at [fluxcd.io](https://docs.fluxcd.io/en/1.19.0/tutorials/get-started-helm/).

You'll need access to a Kubernetes node; a local Minikube installation is fine. You'll also need a public Github repository; we'll be using [whoami](../whoami/) from [another tutorial](../whoami/tutorial/). Fork the repository if you haven't already.

## 1. Install and set up Flux with Helm

If you don't already have Helm installed, install it now by following the instructions [here](https://helm.sh/docs/intro/install/).

Start your Kubernetes node if it's not already running. If you're using Minikube, the command is simply `minikube start`.

Create a `flux` namespace by running:

```bash
kubectl create ns flux
```

Open **flux-values.yaml** and replace `verifa/tutorials` with your Github username. You'll now need to install Flux with Helm, passing this file to the command with the `-f` flag, as follows:

```bash
helm upgrade -i flux fluxcd/flux --namespace flux --version 1.3.0 -f flux-values.yaml
```

Note: The `git.readonly` value is not in the fluxcd.io tutorial but providing it means you don't have to give your deploy key write access on Github.

You could also use `helm install`, but passing the `-i` flag to `helm upgrade` makes it install a release if it's not found.

Next, open **operator-values.yaml**. There's nothing to change but you can familiarise yourself with the options. Again, you'll need to pass it to Helm as follows:

```bash
helm upgrade -i helm-operator fluxcd/helm-operator --namespace flux --version 1.0.2 -f operator-values.yaml
```

Note: The `helm.versions` value is not in the fluxcd.io tutorial but it seems to be necessary to prevent the Helm Operator pod from looking for a non-existent Tiller (Tillers were removed in Helm v3).

## 2. Commit a change

In part 1 you installed Flux to your Kubernetes node and pointed it at your Github repository. By default, Flux looks for all Yaml files that aren't in a Helm chart directory (defined by the presence of Chart.yaml, values.yaml and a templates folder), so in this case, it's finding **ns.yaml**, which defines a `whoami` namespace, and **release.yaml**, which *does* point to a Helm chart directory. Under `spec`, it currently reads:

```yaml
  chart:
    git: ssh://git@github.com/verifa/tutorials/whoami
    ref: master
    path: whoami/helm
```

Replace `verifa/tutorials` with your Github username.

Let's take a look at our Helm chart directory, simply called **helm**. Open **Chart.yaml** and you'll see some basic information about the app, including the `appVersion`. If you did the fluxcd.io tutorial, you might have practised updating the version number, so let's do something else now. Open **values.yaml** and change `replicacount` from 2 to 3. Before pushing this change, run:

```bash
kubectl get pod --namespace=whoami
```

to confirm four pods are running. Now `push` to Github.

## 3. Observe flux auto-deploying your changes

Within the next five minutes, Flux should notice the change and automatically spin up a new pod. You can re-run the previous command (try prepending `watch`) to make sure this happens. If not, you can check the logs by running:

```bash
kubectl -n flux logs deployment/flux -f
```

The rest of the files in the **helm** directory are largely unchanged from their defaults. You can see this for yourself by running `helm create test` or learn more about creating Helm charts and releases in [another tutorial](../helm/).
