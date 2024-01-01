package main

import (
	"context"
	"fmt"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"log"
	"path/filepath"
)

var clientset *kubernetes.Clientset

func listDeployment(namespace string) {
	dpClient := clientset.AppsV1().Deployments(namespace)
	deploys, err := dpClient.List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		log.Fatal(err)
	}
	for _, deploy := range deploys.Items {
		fmt.Printf("%v\t%v\n", deploy.Name, deploy.Namespace)
	}

}

func listPod(namespace string) {
	podClient := clientset.CoreV1().Pods(namespace)
	pods, err := podClient.List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		log.Fatal(err)
	}
	for _, pod := range pods.Items {
		fmt.Printf("%v\t%v\n", pod.Name, pod.Namespace)
	}
}

func main() {
	homePath := homedir.HomeDir()
	if homePath == "" {
		log.Fatal("failed to get the home directory")
	}
	kubeconfig := filepath.Join(homePath, ".kube", "config")
	config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
	//config, err := clientcmd.BuildConfigFromFlags("", "kube-config.yml")
	if err != nil {
		log.Fatal(err)
	}
	clientset, err = kubernetes.NewForConfig(config)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("list deployment")
	listDeployment(metav1.NamespaceDefault)

	log.Println("list pod")
	listPod("kube-system")
}
