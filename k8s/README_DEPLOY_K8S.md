Patasi Bai AI — Kubernetes deployment and CI/CD

What I pushed
- .github/workflows/ci-cd.yaml  — GitHub Actions workflow to build Docker image, push to GHCR and deploy to Kubernetes
- k8s/namespace.yaml
- k8s/deployment.yaml
- k8s/service.yaml
- k8s/ingress.yaml
- k8s/secret-template.yaml
- k8s/kustomization.yaml

What I need from you or the Kubernetes contact (quick checklist)
1) Kubeconfig (base64): Add as GitHub secret in repo Settings → Secrets → Actions → KUBE_CONFIG_DATA. To create the value, run:
   cat ~/.kube/config | base64 -w0
   and paste the output as the secret value.

2) Registry access for pulling images (if GHCR private): create docker-registry secret in the cluster or make the GHCR image public. Example to create secret:
   kubectl create secret docker-registry ghcr-secret \
     --docker-server=ghcr.io \
     --docker-username=<GITHUB_USERNAME> \
     --docker-password=<PERSONAL_ACCESS_TOKEN> \
     --docker-email=you@example.com -n default

3) Set real values in k8s/secret-template.yaml or create Kubernetes secrets manually for DATABASE_URL and payment keys.

4) Replace example.com in k8s/ingress.yaml with your domain, and ensure an ingress controller (nginx) and cert-manager are installed for TLS.

WhatsApp message to send now to the Kubernetes contact (copy/paste)
Hi [Name], thanks for helping with the Kubernetes setup. I pushed the CI/CD workflow and k8s manifests to branch "patasi-bai-ai-co" in the repo. To complete deployment I need one of the following from you:

Option A — provide kubeconfig (quick):
1) Run on your machine: cat ~/.kube/config | base64 -w0
2) Reply with the base64 string (I will ask you to paste it into GitHub repo secret named KUBE_CONFIG_DATA) — this will allow the CI workflow to deploy.

Option B — you can create a service account and give me a kubeconfig limited to the target namespace. If you prefer this, please send the kubeconfig or a kubeconfig with minimal permissions for deployments in namespace "default" (or tell me the namespace).

Also please confirm:
- Is the cluster GKE / EKS / AKS / DigitalOcean / k3s / other? (reply cluster type)
- Do you want me to use GHCR (images pushed by GitHub Actions) or Docker Hub? I used GHCR in the workflow — confirm OK.

Once you send the kubeconfig (base64) or create the secret in the repo, the GitHub Action will build the image and deploy.

Security note: if you prefer not to paste kubeconfig into chat, you can add KUBE_CONFIG_DATA yourself in the repo secrets and I will trigger the deployment after you set it.

What I will do next after you provide the secret
- Trigger a commit (or you can push any change to the branch) and the GitHub Action will build the image, push to GHCR and run kubectl apply to deploy manifests.
- I will monitor rollout and report status back here with logs and any errors.

If you want me to proceed now, I can trigger the workflow once the secret is added. Otherwise, tell your contact to add the secret or share the kubeconfig base64 value here.
