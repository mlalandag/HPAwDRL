# HPAwDRL
Horizontal Pod Scaling with Deep Reinforcement Learning

Enlaces

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/


## Kubernetes Python Client

https://github.com/kubernetes-client/python


## Prometheus ##

Prometheus es una herramienta de código abierto que permite obtener y almacenar métricas y series temporales de datos. Dispone de integraciones para numerosos sistemas, incluido kubernetes, y será el método que nos permitirá obtener la información de entrada que necesitamos para nuestro agente de aprendizaje reforzado.
 
https://prometheus.io/

Instalar Prometheus en Minikube

https://blog.marcnuri.com/prometheus-grafana-setup-minikube

kubectl get svc

minikube service prometheus-server-np --url

Metrics

sum (rate (container_cpu_usage_seconds_total{namespace="php-apache", name!~".*prometheus.*", image!="", container!="POD", id!~".*/docker/.*"}[3m])) by (pod)

Number of pods:

count(kube_pod_info{namespace="php-apache"}) by (namespace)
count(kube_pod_info{namespace="php-apache", pod!~".*load.*"}) by (namespace)

https://stackoverflow.com/questions/40327062/how-to-calculate-containers-cpu-usage-in-kubernetes-with-prometheus-as-monitori