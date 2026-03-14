[Product updates](https://www.digitalocean.com/blog/tags/product-updates)
# What's new and what's next at DigitalOcean: Managed Kafka, more Droplet choices, GPUs for AI/ML apps, and more
By DigitalOcean
  * Published: September 26, 2023
  * 7 min read


Never before has DigitalOcean been better suited to help startups and small businesses thrive. With a host of investments in and updates to our platform available now and in coming months, companies that choose DigitalOcean are choosing cost-effective solutions that improve your productivity and bring much-needed peace of mind.
We’re excited to announce several product enhancements that we’re committed to launching in coming months, starting with [DigitalOcean Managed Kafka](https://www.digitalocean.com/blog/introducing-digitalocean-managed-kafka), which is available right now. A fully-managed, event streaming platform as a service, Managed Kafka offers peace of mind by removing the burden associated with managing a complex solution like Kafka on your own.
DigitalOcean has the products and expertise startups and small businesses need to scale simply—and we’re constantly improving our platform to suit the evolving needs of every one of our users. Take a look at some recent updates that your business can take advantage of now, and a few exciting product enhancements planned for the near future.
  * [Upgrade: DigitalOcean Backup](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#storage-enhancements)
  * [New: Scalable Storage for Managed Databases](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#storage-enhancements)
  * [New: Object Storage in Bangalore](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#storage-enhancements)
  * [Free: DDoS Protection](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#hassle-free-security)
  * [New: Droplet types and performance](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#better-performance-for-a-range-of-products)


Watch the video to get a summary of the updates, or read the details below:
##  [Artificial intelligence (AI) and machine learning (ML)](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#artificial-intelligence-ai-and-machine-learning-ml)
  * **Start using NVIDIA H100 GPUs on Paperspace** :__ In July, we [acquired Paperspace](https://www.digitalocean.com/products/paperspace), a leading provider of cloud infrastructure for highly scalable GPU-accelerated applications, to help startups and SMBs simplify the process of developing, deploying, and scaling modern AI applications at a fraction of the cost. With extremely popular NVIDIA H100 tensor core GPUs available now, startups and SMBs can begin their AI/ML journeys on Paperspace today. [Paperspace is integrated with DigitalOcean Spaces](https://updates.paperspace.com/paperspace-x-digitalocean-integrations-2MZY0U) so you can easily access and manipulate your Spaces Object Storage through Paperspace’s Notebook experience. Plus with an SSO integration with DigitalOcean, accessing products and computing capabilities across platforms is simple.
  * **More Paperspace updates to come** : We will soon introduce other updates such as: simplifying getting started with AI/ML with model deployment templates; streamlined integration with Hugging Face; and improved management tools inclusive of metrics, history, and logs. We also plan on upgrading the underlying network infrastructure with up to 400G capabilities to speed up accelerated computing workloads and boost the Paperspace VM connectivity to the Internet via highly available network in the upcoming months.


##  [Storage enhancements](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#storage-enhancements)
  * **Managed Kafka, a fully managed event streaming platform as a service** : Apache Kafka is the de facto standard for building real-time, data streaming applications and is very popular in industries like streaming, IoT, and data analytics. Due to its inherent operational complexity and high costs, though, many small businesses haven’t been able to take full advantage of Kafka. Today we’re introducing Managed Kafka, a fully managed event streaming platform as a service. It removes the significant difficulty of self-managing Kafka and includes benefits such as automatic updates, high availability, and easy scalability. Like all of our products, Managed Kafka offers low, predictable pricing that starts at $147 per month. Check out the [Managed Kafka announcement](https://www.digitalocean.com/blog/introducing-digitalocean-managed-kafka) to learn more.
  * **Faster, frequent, and comprehensive Backups** : [DigitalOcean Backups—](https://docs.digitalocean.com/products/images/backups/)automatically created disk images of Droplets at weekly intervals—provide an easy way to revert to an older state or to create new Droplets. Customers often have a need for more frequent backups than we’ve offered in the past to better bolster their data protection strategy. To address this need, we’ll soon introduce the ability to create daily backups and other enhancements. Both daily and weekly backups will be differential, significantly reducing the time required to create backups. We’ll open the beta for daily Droplet backups in the near future.
  * **Scalable Storage for Managed Databases** : Many customers run out of storage long before they fully utilize the compute capacity of their database cluster. We will introduce Scalable Storage for [Managed PostgreSQL](https://www.digitalocean.com/products/managed-databases-postgresql) and [Managed MySQL](https://www.digitalocean.com/products/managed-databases-mysql) that will allow users to easily increase the storage capacity of a database cluster **without** upgrading the entire cluster configuration and **without** downtime. This provides flexibility and makes it easier for businesses to support an ever-increasing data footprint. Additionally, by removing the need to increase the vCPU and RAM, which is typically more expensive, costs are better kept in check. We will also introduce database plans with a storage limit of 15TB, a significant increase over our previous limit of 7TB. Scalable Storage for Managed Databases will be available in Q4 2023.
  * **Highly-performant Object Storage in the Bangalore, India data center** : With highly-performant and scalable [object storage now available in the Bangalore data center (BLR1)](https://www.digitalocean.com/blog/spaces-blr), businesses in India can store data within the country—boosting performance by having compute and storage in the same location—which may support their compliance strategy. All Spaces buckets in BLR1 support 800 RPS for read/write operations making it ideal for data analytics workflows, training AI models, log files generated by applications, and video streaming applications.


##  [Hassle-free security](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#hassle-free-security)
  * **DDoS Protection – free robust defense for your apps** : With ever-increasing DDoS attacks, businesses are understandably concerned about experiencing network disruptions or even full-on service outages. That’s where DigitalOcean DDoS protection comes in. Operating within the [OSI Network (L3) and Transport (L4) layers](https://en.wikipedia.org/wiki/OSI_model) at our data center edge, this service provides robust protection from network layer, generalized DDoS attacks without adding latency to your traffic. DDoS protection covers your DigitalOcean cloud infrastructure—including Droplets, Kubernetes clusters, Managed Databases, Load Balancers, and assigned Reserved IPs—across all of our data centers. DDoS protection is free, always on, and built into the DigitalOcean platform—just as it has been for years.


##  [Robust, low-cost support](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#robust-low-cost-support)
  * **Support plans for every business** : Your cloud infrastructure should not get in the way of the success of your business. We offer a range of support plans that help you to resolve issues quickly so you can better focus on your business. Depending on the plan, highly technical staff members will answer questions via email, chat, video calls and Slack, and they escalate emergency tickets for faster troubleshooting. They also provide expert guidance on better resource allocation, cost optimization, security improvements, and other best practices. To ensure [great support remains affordable](https://www.digitalocean.com/products/support), we recently introduced a low-cost plan for $24/month with eight-hour response times for all issues, regardless of severity.


##  [Better performance for a range of products](https://www.digitalocean.com/blog/new-product-updates-kafka-and-more#better-performance-for-a-range-of-products)
  * **Premium CPU-Optimized Droplets** : Whether it’s crystal clear audio, glitch-free video, or uninterrupted gaming, everyone loves seamless digital experiences. To better deliver those experiences, we introduced [Premium CPU-Optimized Droplets](https://www.digitalocean.com/products/droplets/cpu-optimized), virtual machines built for high throughput and consistent performance that are ideal for network and computing-intensive workloads such as streaming media, online gaming, machine learning, and data analytics. Premium CPU-Optimized Droplets offer up to [five times higher outbound network speeds, 58% higher performance, and 290% faster disk writes than standard Droplets](https://www.digitalocean.com/blog/introducing-premium-cpu-optimized-droplets). Since their launch earlier this year, Premium CPU Optimized Droplets have become extremely popular, with startups such as [Validin](https://www.digitalocean.com/customers/validin) using them to power their data indexing platform.
  * **Enhanced memory and storage for Basic Premium Droplets** : We’re always looking to provide more flexibility to customers so they can better address new use cases for their growing business with the power of cloud computing. Basic Premium Droplets, our shared virtual machines—powered by newer AMD EPYC™ and Intel Xeon® CPUs along with superfast NVMe SSDs—are designed to deliver superior performance at an affordable price. In August 2023, we [expanded the Basic Premium Droplet lineup](https://www.digitalocean.com/blog/announcing-new-basic-premium-plans) to include new plans with enhanced memory and storage to give businesses more flexibility and a wider choice of virtual machines.
  * **Managed Databases with powerful compute** : Basic Premium compute plans are coming to Managed Databases. With faster NVMe SSD storage disks, the Basic Premium compute plans will improve the read and write performance of your database clusters. These plans, available in Q4 2023, are ideal for customers who need cost-effective database configuration options with larger disk storage and higher performance requirements.
  * **More Premium Droplet variants coming** : We’re excited to announce that we will be extending the Premium variant to new Droplet types in 2023. Starting in October, users will have access to Premium General Purpose Droplets. These Droplets utilize newer generation CPUs, faster NVMe drives, and offer up to 10 Gbps of outbound data transfer speeds making them ideal for running e-commerce, consumer, and SaaS apps.
  * **Robust WordPress hosting with powerful automation** : Businesses on DigitalOcean have told us that they need a WordPress solution that’s hassle-free and delivers fast and reliable WordPress website experiences without any interruptions. We’re introducing [Cloudways Autoscale](https://www.cloudways.com/blog/announcing-autoscale-for-wordpress/), a new fully-managed WordPress hosting solution which includes autoscaling, load balancing, and high availability. Powered by Kubernetes, Autoscale uses load balancers to automatically distribute traffic efficiently to maximize website speed and performance. Ideal for companies running e-commerce stores, ticket booking sites, and high-traffic influencers, Autoscale easily handles traffic spikes by automatically scaling your hosting resources up or down based on traffic demand. You can [request early access](https://www.cloudways.com/en/autoscale.php) to the beta now and be among the first to experience the future of cloud hosting.


We hope you are as excited about these updates and enhancements as we are. Check out this [webinar](https://try.digitalocean.com/whats-new-in-digitalocean/) or fill out this [form](https://try.digitalocean.com/product-releases/) if you want to learn more about any of the product updates. [Contact our sales team to learn more about how DigitalOcean can help your business grow >](https://www.digitalocean.com/company/contact/sales)
### About the author
DigitalOcean
Author
## Related Articles
Product updates
### Native .NET Buildpack Support is Now Available on App Platform
  * March 5, 2026
  * 2 min read


[Read more](https://www.digitalocean.com/blog/net-buildpack-support-app-platform)
Product updates
### Supabase Template is Now Available on DigitalOcean App Platform
  * February 26, 2026
  * 3 min read


[Read more](https://www.digitalocean.com/blog/supabase-template-app-platform)
Product updates
### Expanding our Agentic Inference Cloud: Introducing GPU Droplets Powered by AMD Instinct™ MI350X GPUs
  * February 19, 2026
  * 2 min read


[Read more](https://www.digitalocean.com/blog/now-available-amd-instinct-mi350x-gpus)
© 2026 DigitalOcean, LLC.Cookie Preferences
