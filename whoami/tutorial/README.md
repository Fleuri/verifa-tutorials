# Get started with Docker and Kubernetes

In this tutorial, you will:

1. Create a "whoami" app in Python
2. Dockerize it
3. Deploy it with Docker Swarm
4. Deploy it with Kubernetes

## 0. Before you start

This tutorial assumes you'll be using [Visual Studio Code](https://code.visualstudio.com/) (VS Code) to write [Python](https://www.python.org/) on Linux. You can use another editor, language or operating system to achieve the same result but you'll need to make some adjustments to the examples given here.

If you want to skip step 1, perhaps because you're already confident in your Python abilities, a [ready-made version is available](../app/).

## 1. Create your app

To get started, open a terminal in this directory. You'll need to create a virtual environment, which you can do with [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/). Follow the instructions [here](https://pipenv-fork.readthedocs.io/en/latest/install.html) to install it if necessary, then run `pipenv install flask`.

If you now open **app.py** in VS Code and hit Ctrl+F5 to run without debugging, you should see Flask start to run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Open that in your browser and you should see "Working." Go to [http://127.0.0.1:5000/api/whoami](http://127.0.0.1:5000/api/whoami) or `curl` that address in a terminal and you should see some very simple Json. Press Shift+F5 in VS Code to stop the process.

Open **whoami.py** in the **lib** folder to see the start of a Whoami class. Your task is to change `to_json()` so it returns some useful information. Basic requirements include:

* IP address
* Hostname
* MAC address
* Platform
* Environment variables (keys)
* Python version

If a piece of information isn't available, your app will need to be able to include an appropriate error or status message in its Json output.

Some useful Python modules to import are [os](https://docs.python.org/3/library/os.html), [platform](https://docs.python.org/3/library/platform.html), [socket](https://docs.python.org/3/library/socket.html) and [uuid](https://docs.python.org/3/library/uuid.html).

You should also write some basic unit tests in **test_whoami.py**. You'll need `pytest` to run them, which you can add to the virtual environment with `pipenv install --dev pytest`. One test has been provided for you to confirm that MAC addresses are being formatted correctly.

Before moving on, make sure your code is documented, [well-formatted](https://black.readthedocs.io/en/stable/) and [typed](https://mypy.readthedocs.io/en/stable/). You may wish to run `pipenv install --dev --pre black pylint mypy` and set all three to run on save within VS Code.

## 2. Dockerize your app

Your next task is to run your app in a Docker container on your machine. First, download and install [Docker](https://docs.docker.com/get-docker/) if you haven't already. Complete the [hello-world](https://docs.docker.com/get-started/) introduction if you're new to Docker.

Back in your whoami project, you might need to update the included **Dockerfile**. Run `python3 --version`, then find the corresponding python image on [Docker Hub](https://hub.docker.com/_/python?tab=tags) and replace the Dockerfile's FROM line. If you are using any Python packages not included in the standard library, add them to **requirements.txt**. You'll notice `flask` is already there.

If everything is set up properly, you can then open a terminal in the project's root directory and enter:

```bash
docker build -t whoami:0.1.0 .
```

to build your image. The `-t` option specifies the name `whoami` and the tag `0.1.0`. Run `docker images` afterwards and you should see it listed.

Next, run:

```bash
docker run -p 8000:5000 --rm --name="whoami" whoami:0.1.0
```

The `-p 8000:5000` option publishes the container's port 5000 (flask) to Docker's external port 8000, and `--rm` removes the container when the process exits. Run `curl -H Host:whoami.docker.localhost http://127.0.0.1:8000/api/whoami` to confirm it's working.

Create an account on Docker Hub if you don't have one, then create a new (public) "whoami" repository. Open **Makefile** and replace the placeholder name with your own. You can now use the commands `make build` to build your image and `make push` to push it to Docker Hub.

Now run:

```bash
make build push
```

You may need to authenticate with your Docker Hub credentials. Extend the Makefile with a `run` command.

## 3. Deploy your app with Docker Swarm

Your next task is to deploy your app using Docker's built-in swarm mode. For the sake of this tutorial, your computer will be the one and only node in the swarm (cluster). Start off by running:

```bash
docker swarm init
```

Open **stack.yaml** and once again replace the placeholder with your Docker Hub username. Your stack will be a single app for now but you can extend this later (see "Extras").

Next, run:

```bash
docker stack deploy --compose-file stack.yaml whoami
```

and your stack will be deployed to the swarm. After a moment, you can run `docker ps` to list all running containers: you should see two copies of whoami. Run `curl http://localhost:8000/api/whoami` and you should notice that the hostname corresponds to one of the listed container IDs - run it a few times and you should get a response from the other container at least once.

Extend the Makefile with a `swarm` command that deploys your stack to the swarm.

Stop your service with `docker service rm whoami_api`. Attempting to stop or remove your containers before removing the service will lead the the service just creating a new one in its place, since it has a desired state of two replicas.

## 4. Deploy your app with Kubernetes

For the final part of this tutorial, you'll be deploying your app with Kubernetes. Start off by following the Minikube installation instructions on the [Kubernetes website](https://kubernetes.io/docs/tasks/tools/install-minikube/).

Once Minikube is installed and running, you'll first need to first create a service, then deploy your app. Both are achieved through the `kubectl` command, which you should have installed as part of the Minikube installation process.

Take a look at the **svc.yaml** and **dep.yaml** files. The former describes a NodePort service that exposes your container's ports, while the latter specifies a whoami pod and declares that there should always be two replicas running. Replace the placeholder name with your Docker Hub name again in the dep file.

With that done, and Minikube started, you can run:

```bash
kubectl create -f svc.yaml
```

to start the service, then:

```bash
kubectl create -f dep.yaml
```

to deploy your app. Run `watch kubectl get deployment` immediately afterwards and watch as your two pods come online (it can take a minute).

If something's not working, use `kubectl describe <resource-type> <resource-name>`, e.g. `kubectl describe deployment whoami-dep` to troubleshoot.

Extend the Makefile with a `kube` command that creates your service and deployment in Kubernetes.

Note that your API is no longer exposed through localhost on port 8000 but through Minikube on port 30000. You should be able to access it with `curl $(minikube ip):30000/api/whoami`. Again, if you `curl` multiple times you will notice the hostname changing as your request is directed to different pods automatically.

Try running `minikube dashboard` to see the deployment and service you created, and the pods and replica set *they* created.

If you need to tear everything down from Minikube, run the included **teardown.sh** file. You might first need to make it executable with `chmod +x teardown.sh`.

## 5. Extras

If you have time, here are some extra tasks you may wish to take on:

* Extend the API's functionality to include other useful, non-secret information about the environment it's running in
* Replace the version numbers in the .yaml files with a placeholder and find a way to fill them on the fly with the Makefile's VERSION variable
* Add a reverse proxy to the stack so that when you deploy it with Docker Swarm, you're not exposing container ports directly
* Configure rolling updates for your Kubernetes deployment
* Move on to a related tutorial using this app: [Helm](../helm/) or [Flux](../flux/)
