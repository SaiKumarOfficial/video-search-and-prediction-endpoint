# Setup Blue-Green Deployment in EKS 


## Prerequisites

Before you begin, ensure you have the following tools installed:

1. **AWS CLI:**
   - [Download AWS CLI](https://aws.amazon.com/cli/)

2. **eksctl:**
   - For Windows:
     ```shell
     choco install -y eksctl
     choco upgrade -y eksctl
     ```

3. **kubectl:**
   - [Download kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Steps to Follow

### 1. Start Kubernetes Server

   i. Open Docker Desktop on your local machine.

   ii. Run in CMD:
   ```shell
   minikube start
   ```

### 2. Configure AWS Locally

   i. Run:
   ```shell
   aws configure
   ```

   ii. Configure with your root access and secret key IDs in your desired region (Ex: ap-south-1).

   iii. To get root access key ID, go to profile > security-credentials > create access key.

### 3. Create EKS Cluster

   ```shell
   eksctl create cluster --name <cluster-name> --region <region-name> --fargate
   ```

   To delete the cluster:
   ```shell
   eksctl delete cluster --name <cluster-name> --region <region-name>
   ```

### 4. Update Kubeconfig

   ```shell
   aws eks update-kubeconfig --name <cluster-name> --region <region-name>
   ```

### 5. Create Namespace and Setup Secrets

   - To create namespace:
     ```shell
     kubectl create namespace <your-namespace>
     ```

   - To create Kubernetes Secret:
     ```shell
     kubectl create secret generic aws-secrets \
       --namespace=<your-namespace> \
       --from-literal=AWS_ACCESS_KEY_ID=<your-access-key-id> \
       --from-literal=AWS_SECRET_ACCESS_KEY=<your-secret-key-id> \
       --from-literal=AWS_BUCKET_NAME=<your-bucket-name> \
       --from-literal=AWS_REGION=<your-region>
     ```

   - To check:
     ```shell
     kubectl get ns
     kubectl get secrets -n <your-namespace>
     ```

### 6. Create Fargate Profile

   ```shell
   eksctl create fargateprofile --cluster <cluster-name> --region <region-name> --name alb-sample-app --namespace <your-namespace>
   ```

### 7. Deploy the Deployment, Service, and Ingress

   Go to the k8s/ directory.

   Deploy blue (old version) deployment:
   ```shell
   kubectl apply -f blue-deploy.yml
   kubectl apply -f blue-ingress.yml
   ```

   Check:
   ```shell
   kubectl get pods -n <your-namespace> -w
   kubectl get svc -n <your-namespace>
   kubectl get ingress -n <your-namespace>
   ```

### 8. Check the Pods Logs

   ```shell
   kubectl logs <your-pod-name> --namespace=<your-namespace>
   ```

   To get into the container:
   ```shell
   kubectl exec -it <your-pod-name> -n <your-namespace> -- /bin/sh
   ```

### 9. Run Pods Locally (Optional)

   ```shell
   kubectl port-forward <your-pod-name 8080:80 -n <your-namespace>
   ```

### 10. Setup ALB Add-On

   10a. To configure IAM OIDC provider:

   ```shell
   export cluster_name=demo-cluster
   oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
   aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
   ```

   If not configured, run the following:
   ```shell
   eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
   ```

   10b. Download IAM policy:
   ```shell
   curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json
   ```

   10c. Create IAM Policy:
   ```shell
   aws iam create-policy \
     --policy-name AWSLoadBalancerControllerIAMPolicy \
     --policy-document file://iam_policy.json
   ```

   10d. Create IAM Role:
   ```shell
   eksctl create iamserviceaccount --cluster=<your-cluster-name> --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=arn:aws:iam::967474752012:policy/AWSLoadBalancerControllerIAMPolicy --approve
   ```

### 11. Deploy ALB Controller

   Add Helm repo:
   ```shell
   helm repo add eks https://aws.github.io/eks-charts
   ```

   Update the repo:
   ```shell
   helm repo update eks
   ```

   Install:
   ```shell
   helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
     -n kube-system \
     --set clusterName=<your-cluster-name> \
     --set serviceAccount.create=false \
     --set serviceAccount.name=aws-load-balancer-controller \
     --set region=<region> \
     --set vpcId=<your-vpc-id>
   ```

   Verify that the deployments are running:
   ```shell
   kubectl get deployment -n kube-system aws-load-balancer-controller
   ```

   Verify the pods are running or not:
   ```shell
   kubectl get pods -n kube-system -w
   kubectl get deploy -n kube-system
   ```

   Check the Ingress address to access the blue (old) version application.

### 12. Deploy Green (New) Versioned Application

   Run the following commands in the k8s directory where the deployment files are located:
   ```shell
   kubectl apply -f green-deploy.yml
   ```

   Check pods and services:
   ```shell
   kubectl get pods -n <your-namespace> -w
   kubectl get svc -n <your-namespace>
   ```

   Rollout the application by changing the Ingress:
   ```shell
   kubectl apply -f green-ingress.yml
   kubectl get ingress -n <your-namespace>
   ```

   Finally, you can see the new versioned application.
   
---

Feel free to customize this README template to suit your project's specific needs. Add any additional information or sections as necessary.