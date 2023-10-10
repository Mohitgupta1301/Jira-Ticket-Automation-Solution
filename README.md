# AI-Ops Solution Deployment Guide

This guide outlines the step-by-step process for setting up an AI-Ops solution, including deploying a Minikube cluster, Grafana, Prometheus, Jenkins, and integrating Python packages such as "Hugchat" and "Jira."

## Prerequisites

Before proceeding, ensure that the following prerequisites are met:

- A functioning Minikube cluster.
- Accessibility to Grafana and Prometheus.
- Jenkins installed and properly configured.
- Availability of required Python packages: "Hugchat" and "Jira."
- A valid Jira account for integration.

## Setting up the Minikube Cluster

Minikube provides a local Kubernetes environment for development and learning.

**Requirements:**

- A machine with at least 4 CPUs.
- Minimum of 2GB of free memory.
- At least 20GB of free disk space.
- A container or virtual machine manager (e.g., Docker, Hyper-V, VirtualBox, VMware).

## Setting Up Grafana in Minikube

Before starting, ensure you have the following:

- A Kubernetes cluster.
- The [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) command-line client installed and configured.
- The [helm](https://helm.sh/docs/intro/install/) command-line client installed and configured.

To deploy the Grafana-agent-operator Helm chart into your Kubernetes cluster, follow these steps:

1. Update Helm repositories:

    ```shell
    helm repo update
    ```

2. Install the Agent Operator Helm chart:

    ```shell
    helm install my-release stable/grafana-operator
    ```

3. Customize Helm chart parameters using a `values.yaml` file if needed.

4. To deploy the Agent Operator into a specific namespace, use the `-n` flag:

    ```shell
    kubectl create namespace ai-ops
    helm install my-release stable/grafana-operator -n ai-ops
    ```

## Setup Prometheus monitoring on Kubernetes cluster using Helm 

Prometheus is an Open-source systems monitoring and alerting toolkit. Prometheus collects and stores the metrics as time series data. It provides out-of-box monitoring capabilities for container orchestration platforms such as Kubernetes. 

## Prerequisites- 

A Kubernetes cluster should be available where we can set up Prometheus. we have used minikube to create a new Kubernetes cluster.   Minikube can be used to set up a local Kubernetes cluster on Windows or macOS or Linux. 

 
## Installing Prometheus- 

Look for official charts for Prometheus and the repositories into the helm repo using the following commands: 
Go to the following repo, https://artifacthub.io/ .
Look for official charts for Prometheus and Grafana and the repositories into the helm repo using the following commands:


1. Add the Prometheus and Grafana Helm repositories:

   ```shell
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   ```
   Next, we need to install Prometheus using the following command:
   ```shell
   helm install prometheus prometheus-community/prometheus
   ```

2. We can expose the prometheus-server service to the internet using node port, but the GUI provided by prometheus is not as good as the one provided by Grafana. We can use the following command for the same:

   ```shell
   kubectl expose service prometheus-server — type=NodePort — target-port=9090 — name=prometheus-server-ext

   minikube service prometheus-server-ext
   ```

## Install Jenkins

##Prerequisites 


1. One Ubuntu 22.04 server configured with a non-root sudo user and firewall by following the Ubuntu 22.04 initial server setup guide. We recommend starting with at least 1 GB of RAM. Visit Jenkins’s “Hardware Recommendations” for guidance in planning the capacity of a production-level Jenkins installation. 
2. Oracle JDK 11 installed, following our guidelines on installing specific versions of OpenJDK on Ubuntu 22.04. 


 Step 1 — Installing Jenkins 

First, add the repository key to your system: 
   ```shell
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key |sudo gpg --dearmor -o /usr/share/keyrings/jenkins.gpg
   ```

The gpg --dearmor command is used to convert the key into a format that apt recognizes.

Next, let’s append the Debian package repository address to the server’s sources.list:  
   ```shell
   sudo sh -c 'echo deb [signed-by=/usr/share/keyrings/jenkins.gpg] http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   ```

The [signed-by=/usr/share/keyrings/jenkins.gpg] portion of the line ensures that apt will verify files in the repository using the GPG key that you just downloaded.

After both commands have been entered, run apt update so that apt will use the new repository.
   ```shell
   sudo apt update
   ```

Finally, install Jenkins and its dependencies:
   ```shell
   sudo apt install jenkins
   ```

Now that Jenkins and its dependencies are in place, we’ll start the Jenkins server.

Step 2 — Starting Jenkins
now that Jenkins is installed, start it by using systemctl:
   ```shell
   sudo systemctl start jenkins.service
   ```
Since systemctl doesn’t display status output, we’ll use the status command to verify that Jenkins started successfully:
   ```shell
   sudo systemctl status jenkins
   ```

## Configuration Jenkins  

Install Generic webhook trigger and copy the webhook url provided by Generic webhook. And paste that url in the grafana contact point. 

 ## Prerequisites 

1. Jenkins installed and running. 
2. Grafana installed and accessible. 


## Step 1: Install the Generic Webhook Trigger Plugin 

- Open your Jenkins instance in a web browser. 
- Click on "Manage Jenkins" in the Jenkins dashboard. 
- Select "Manage Plugins." 
- Navigate to the "Available" tab and search for "Generic Webhook Trigger Plugin." 
- Check the checkbox next to the plugin and click "Install without restart." 
- Wait for the plugin to be installed. Jenkins will display a message when it's done. 

## Step 2: Configure a Jenkins Job 

- Create a new Jenkins job or open an existing one. 
- In the job configuration, scroll down to the "Build Triggers" section. 
- Check the "Generic Webhook Trigger" option. 
- Configure the webhook URL provided by Generic webhook as the "Generic Webhook URL." 

## Step 3: Set Up Grafana to Send Webhooks 

- Open your Grafana instance in a web browser. 
- Click on the gear icon (⚙️) in the lower-left corner to access the configuration menu. 
- Select "Notification channels" or similar, depending on your Grafana version. 
- Click on "New Channel" to create a new notification channel. 
- Give the channel a name and select the appropriate notification type (e.g., "Webhook"). 
- Paste the webhook URL from your Jenkins job configuration into the "URL" or "Endpoint" field of the Grafana notification channel. 
- Save the notification channel configuration. 

## Step 4: Test the Integration 

- To test the integration, trigger the Jenkins job using the configured webhook. 
- Grafana will send a webhook notification to Jenkins when a specific event occurs. 
- Jenkins will respond to the webhook, executing the configured job or pipeline. 
- Check the Jenkins job's build console for the webhook payload and any actions triggered by the webhook      

## Hugchat python package 

Unofficial HuggingChat Python API, extensible for chatbots etc. HugChat is a Python package that allows developers to build chatbot applications, generate creative text formats, answer questions informatively, translate languages, and perform web searches. 

  ## HugChat can be used to: 

- Build chatbot applications that interact with users in a natural and engaging manner. 
- Generate creative text formats such as poems, code, scripts, musical pieces, emails, and letters. 
- Answer questions informatively, even if they are open ended, challenging, or strange. 

## Installation- 
   ```shell
   pip insall hugchat
   ```
or
   ```shell
   pip3 install hugchat
   ``` 

 **The hugchat package is used in script to explain log errors and give possible solutions to them.** 


## Jira Python Package 

Jira is an agile, project management tool, developed by Atlassian, primarily used for, tracking project bugs, and issues. It has gradually developed, into a powerful, work management tool, that can handle, all stages of agile methodology. 

JIRA is a Python library, for connecting, with the JIRA tool. This library is easy to use, as compared, to the API method, for fetching data, related to Issues, Projects, Worklogs etc. The library, requires, a Python version, greater than 3.5. 

 ## Installation-  
   ```shell
   pip install Jira
   ```

By leveraging the jira Python package, you can streamline and automate various aspects of Jira ticket management, improving efficiency and reducing manual efforts in your project or issue tracking workflows. Remember to adapt the provided code examples to meet your specific needs and workflows, and ensure that your Jira instance is configured to work with the Jira API.



   
