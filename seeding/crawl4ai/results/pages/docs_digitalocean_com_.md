# DigitalOcean Docs
Learn how to build, deploy, and scale your applications with DigitalOcean. Explore our products with our documentation's technical walkthroughs, example code, reference information for our APIs, CLI, and client libraries, and more.
## Get Started 
Information about the DigitalOcean platform, like billing details, release notes, product availability by datacenter, support plans, and account details.
Information on DigitalOcean product features, pricing, availability, and limits; how to use products from the control panel; how to manage your account, teams, and billing; and platform details, release notes, and product policies.
Manage resources programmatically and integrate across the developer ecosystem with CLIs, APIs, and SDKs.
Looking for technical support with your DigitalOcean account or infrastructure? Start here.
## Browse by 
### Product Genre 
Build your application the way you want with our suite of compute products including VMs, managed containers, PaaS, and serverless functions.
Build, train, and deploy AI agents with the DigitalOcean Gradient™ AI Agentic Cloud.
Store and access any amount of data reliably in the cloud, with S3-compatible Spaces Object Storage, network-based Volumes block storage, or NFS-based Network File Storage.
Create backups, upload custom images, use preconfigured images to create resources, and store Docker images in a private registry.
Run fully managed database clusters running your choice of database engine and avoid manual setup and maintenance.
Secure and control the traffic to your applications with VPC networking, traffic filtering, and load balancing.
Track the health of your infrastructure, URLs, and more, set alerts to stay informed, and organize your resources with projects.
Teams are how you manage your billing and infrastructure on DigitalOcean. You can work by yourself by remaining the only person on your team or collaborate by adding more people to teams you own.
### Developer Tools 
Manage your DigitalOcean resources from the command line with doctl, our open-source command line interface (CLI).
Programmatically manage your Droplets, Spaces, and other DigitalOcean resources using conventional HTTP requests. Use RESTful APIs to programmatically manage Droplets, Spaces, and other DigitalOcean resources.
Interact with Paperspace resources programmatically using the Paperspace API or CLI, and find documentation for legacy tools.
Automate DigitalOcean infrastrucuture and configuration management using the open source Ansible framework.
Deploy and change many resources simultaneously using the open source Terraform tool.
PyDo is DigitalOcean’s official Python client library based on DigitalOcean’s OpenAPIv3 specification.
This is a list of official and community-created client libraries that let you use the DigitalOcean’s APIs in a variety of programming languages.
We use and contribute to open source software.
Use MCP servers to manage DigitalOcean services from any MCP-compatible client.
## Latest Updates 
### Upcoming Changes 
  * App Platform’s XL build resources (8 CPUs and 20 GiB of memory during builds) are now enabled for all apps by default. The `xl-build` flag is now deprecated and will be removed in a future release. Remove `xl-build` from your [app spec](https://docs.digitalocean.com/products/app-platform/how-to/update-app-spec/) to avoid potential errors once the flag is fully retired.
  * [DigitalOcean Managed Caching](https://docs.digitalocean.com/products/databases/valkey/) is being discontinued on 30 June 2025.
To replace Managed Caching, we are offering [Managed Valkey](https://docs.digitalocean.com/products/databases/valkey/), a Redis-compatible alternative with RDMA and higher throughput. All existing Managed Caching clusters automatically convert to Valkey clusters by 30 June 2025 during your [upgrade window](https://docs.digitalocean.com/products/databases/valkey/how-to/schedule-updates/), retaining all data.


### 13 March 2026 
  * Namespace access keys are now available for Functions. They provide user-specific credentials per namespace, so you can create a key for each user or application and revoke access individually. Keys linked to removed team members are revoked automatically. The legacy shared namespace token is deprecated and will be removed on 3 June 2026. During the migration period, both methods work. After 3 June 2026, legacy tokens will no longer authenticate.
Visit [How to Manage Namespace Access Keys](https://docs.digitalocean.com/products/functions/how-to/manage-namespace-access/) to learn more about managing namespace access keys.
  * [Team owners and resource modifiers](https://docs.digitalocean.com/platform/teams/roles/) can now view resource usage and limits in the DigitalOcean Control Panel. You can use this interface to understand resource capacity, manage resource growth, and initiate support requests to increase limits when needed. For more information, see [View Resource Limits](https://docs.digitalocean.com/platform/teams/how-to/view-resource-limits/).


### 12 March 2026 
  * The following models are now available on DigitalOcean Gradient™ AI Platform for [serverless inference](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/), [Agent Development Kit](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/build-agents-using-adk/), and [creating agents](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/create-agents/):
    *     * [Kimi K2.5](https://www.kimi.com/ai-models/kimi-k2-5)
    * [MiniMax M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5) (Public Preview)
For more information, see the [Available Models page](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/#foundation-models).
  * [Network File Storage](https://docs.digitalocean.com/products/nfs/) now offers two performance tiers. The new **Standard Tier** provides cost-effective shared storage for general-purpose workloads. The existing **High Performance Tier** delivers higher throughput that scales with share size for data-intensive workloads like AI/ML training and high-throughput analytics.
Network File Storage is generally available in ATL1, NYC2, and AMS3. For details, see [NFS features](https://docs.digitalocean.com/products/nfs/details/features/) and [pricing](https://docs.digitalocean.com/products/nfs/details/pricing/).


### 6 March 2026 
  * The following OpenAI model is now available on DigitalOcean Gradient™ AI Platform for [serverless inference](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/) and [Agent Development Kit](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/build-agents-using-adk/):
For more information, see the [Available Models page](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/#foundation-models-openai).


For more, see our [full release notes](https://docs.digitalocean.com/release-notes/). 
### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
Cookie Preferences
