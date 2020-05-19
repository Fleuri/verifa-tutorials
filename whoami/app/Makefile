IMAGE=verifa/whoami
VERSION=0.1.6

build:
	docker build -t $(IMAGE):$(VERSION) .

push:
	docker push $(IMAGE):$(VERSION)
	docker tag $(IMAGE):$(VERSION) $(IMAGE):latest
	docker push $(IMAGE):latest

run:
	docker run -d -p 8000:5000 --rm --name "whoami" $(IMAGE):$(VERSION)

kube:
	kubectl create -f svc.yaml 
	kubectl create -f dep.yaml

