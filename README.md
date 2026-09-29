#  Pyrites Grill — AWS Deployment & DevOps Mini Project

A hands-on cloud infrastructure project focused on deploying a full-stack web application on AWS, managing networking layers, securing databases, and automating infrastructure with **Terraform**.

---

## 1. Project Overview

**Pyrites Grill** is a restaurant booking app used as a practical workload to learn real-world DevOps practices. The primary focus of this project is infrastructure, networking, security, and cloud troubleshooting—not application development.

### Core Objectives
- Provision AWS infrastructure using **Terraform (IaC)**.
- Isolate resources safely using custom **VPC, Public/Private Subnets, and Security Groups**.
- Expose a Flask REST API to the web while securing an **Amazon RDS MySQL** database in a private network.
- Gain hands-on experience debugging network, service, and routing failures.

---

## AWS Architecture
![AWS Architecture](/images/architecture.png)

### Key Components

| Component | Purpose | Network Exposure |
| :--- | :--- | :--- |
| **Amazon S3** | Static frontend hosting | Public |
| **AWS VPC** | Isolated network environment | Custom Virtual Network |
| **Public Subnet** | Hosts the web application server | Public-facing |
| **Amazon EC2** | Runs the Flask API backend (`:5000`) | Public via IGW |
| **Private Subnet** | Protects backend data persistence | Private (No Internet) |
| **Amazon RDS** | Managed MySQL database (`:3306`) | Accessible only from EC2 |
| **Terraform** | Infrastructure as Code (IaC) provisioning | Local / CI |

---

## Real-World Challenges & Troubleshooting

Deploying across multiple AWS and Linux layers required step-by-step debugging. Here are the core errors encountered and how they were resolved:

| Layer / Issue | Problem | Root Cause | Solution / Takeaway |
| :--- | :--- | :--- | :--- |
| **1. Dynamic Public IP** | EC2 lost connection after restarts | AWS assigns new public IPs on reboot | Treat public IPs as temporary; map to Elastic IP in future iterations. |
| **2. Security Group** | Inbound traffic blocked | Port `5000` was not allowed in SG inbound rules | Updated Security Group rules to permit external traffic on port `5000`. |
| **3. App Binding** | Unreachable outside EC2 | Flask bound to `127.0.0.1` (localhost only) | Bound Flask server to `0.0.0.0` to listen on all network interfaces. |
| **4. Port Conflicts** | `Address already in use` | Zombie Flask processes occupying port `5000` | Identified process with `sudo lsof -i :5000` and terminated before restarting. |
| **5. API Routing** | `404 Not Found` / CORS misdirection | Frontend missing `/api` prefix on endpoints | Aligned frontend endpoint paths with Flask routes before diagnosing CORS. |
| **6. DB Connection** | Intermittent connection failures | Conflicting local SQLite vs. remote RDS env configs | Extracted credentials to environment variables and restricted RDS access to EC2 SG. |
| **7. Browser Caching** | Updates not reflecting | S3 served stale cached JavaScript files | Applied clear cache-control headers during static asset deployment. |

---

##  Future Roadmap & Improvements

While the initial version successfully runs end-to-end, the following production-grade improvements are planned:

- [ ] **Elastic IP:** Assign a static public IP to avoid backend endpoint shifts.
- [ ] **Daemonization (`systemd`):** Run Flask as a background Linux service for automatic failure recovery and boot startup.
- [ ] **WSGI + Reverse Proxy:** Deploy **Gunicorn** behind **Nginx** (ports `80`/`443`) instead of exposing Flask directly on port `5000`.
- [ ] **SSL/TLS Encryption:** Enable HTTPS for secure client-server communication.
- [ ] **Monitoring & Alerts:** Implement **Amazon CloudWatch** for memory, disk usage, and application logs.
- [ ] **CI/CD Pipeline:** Automate testing, building, and deployment using **GitHub Actions**.

---

###  Core Takeaway
> *Deploying software is more than writing code. A successful deployment requires understanding the full request path—from DNS and Route Tables down to Linux sockets and private subnets.*
