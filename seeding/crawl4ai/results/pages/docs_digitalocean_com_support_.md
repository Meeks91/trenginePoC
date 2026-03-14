# Support Home
Validated on 20 Mar 2024 • Last edited on 17 Apr 2025
## Accounts 
You can only transfer Droplet Snapshots directly to another account or team. You have to migrate other resources manually to another account or team.
If your account is locked during sign-up, [contact DigitalOcean support](https://cloudsupport.digitalocean.com) so we can authorize your access to your account.
No, support plans apply only to DigitalOcean.
Team collaboration is built into the DigitalOcean experience from sign-up.
You can disable device verification by enabling two-factor authentication (2FA) or by authenticating with Google or GitHub.
If you’ve lost access to your 2FA device, you can disable 2FA using your backup method (backup codes or SMS).
Use the Can’t Sign In form to send a support request if you can’t sign into your account.
Switch to a different login method on your DigitalOcean account (like email and password), then switch back to Google or GitHub and select the account you want to use.
Your username is the email you used to sign up for DigitalOcean. You can request a password reset email from the login page.
Try restoring access to your email account by contacting your email administrator, renewing your domain’s registration, or setting up another email server.
Try to restore access to your GitHub account by following GitHub’s account recovery process or 2FA credential recovery process.
Try to restore access to your Google account by following GitHub’s account recovery process.
Reset your account password and add additional security by enabling 2FA or SSO.
You may be required to enter a verification code each time you sign in if you use an ad blocker. You may be asked to verify your browser from a trusted location and device if you have deleted cookies for digitalocean.com or you have disabled cookies entirely.
If you didn’t receive a login email you requested from DigitalOcean, check your spam folder, make sure you’re looking at the right email address, and try refreshing for new mail.
## API 
Debugging and solutions for common authorization and access token request errors when using the OAuth API.
## App Platform 
Use the app’s Settings tab to remove domains associated with App Platform apps.
Increase the heap memory by setting the environment variable NODE_OPTIONS=–max-old-space-size=4096.
Delete the existing dev database and create a new one. Then make sure that the app deployment completes successfully.
You cannot add the same domain name to multiple apps or split an app and domain name across more than one account.
Specify the registry property in the app spec.
Functions does not support forwarding to Managed OpenSearch.
Troubleshoot by making sure the Dockerfile and its commands build on Linux AMD64 and other steps.
App Platform automatically generates and issues the SSL certificate during the configuration.
Your app may have crashed while trying to receive an upload or return a response larger than it has been configured to manage.
Your team balance may be past due. Pay your balance to lift restrictions on actions you can take on the platform.
You can find the client IP address of a request connecting to your app in the `do-connecting-ip` HTTP header.
Timeouts can be caused by high CPU utilization, so check your app’s CPU utilization and consider scaling your app.
Dedicated egress IPs route egress (outbound) traffic from an app. To route ingress (inbound) traffic to an app, use one of App Platform’s public ingress IPs.
Add the root domain to the list of domains in the app’s settings along with the wildcard subdomain.
App Platform apps may be slow or unable to resolve `.gov` domains because the domain administrators have blocked DigitalOcean’s IP addresses. To fix this, you can contact the domain administrator or use a custom DNS resolver.
If your resources have been destroyed due to a prolonged past due balance, you can contact support to request the app spec for deleted apps to recreate the app with the same configuration.
Disable the feature in the app spec using the disable_email_obfuscation field.
Increase your app’s maximum execution time in its .user.ini file to give it more time to complete requests.
Remove the domain from the old app before deleting the old app, or wait 24 hours for the DNS to update.
In your Dockerfile, the `USER` instruction needs to be after the `FROM` and `WORKDIR` instructions.
Ensure your Dockerfile’s path is correctly defined using the `dockerfile_path` parameter in your app spec file.
Multiple 408 errors are often caused by your app sending health checks with very short timeouts to App Platform. They typically don’t affect the functionality of the app.
App Platform builds have a fixed amount of memory available, so try optimizing your builds to stay within the 8 GB limit. You can increase the amount of memory in App Platform deployments by upgrading to a different plan.
Dev Databases have no direct backup feature but you can use a cron job to back up your data to another database.
You need to explicitly add the subdomain in your app’s settings.
You cannot pause, stop, or disable an app. You can delete the app and re-create it when needed.
Component-level variables override app-level variables, so you may have defined environment variables at both levels.
App Platform does not support connecting to DigitalOcean Managed Databases during the build process if the database has trusted sources enabled.
App Platform does not support backups, but you can use DigitalOcean Managed Databases to back up your data.
Dev databases are located in the same region as your app and cannot be migrated to another region.
Your upload may be exceeding your app’s allotted file storage space or it could be timing out.
You see the CDN load balancer’s IP address. Use `dig` to see the dynamic IP address of the app.
Application crashes, high memory consumption, and high disk usage are usually responsible for apps restarting.
App Platform provides two static ingress IPs you can use to map A records to your app.
Environment variables are only available as build-args for Dockerfile builds in App Platform.
You can change an app’s source repository by updating the app’s spec.
Ensure the missing module is listed in the `dependencies` section of the `package.json` file.
App Platform does not currently support injecting values as files on disk. Use environment variables to create files at run time.
Review your app’s build logs to diagnose which process failed during building.
Database bind variables are only available during an app’s deployment and run times.
Your app is likely unavailable on the port App Platform uses to perform health checks. Customize the health check or update the ports in your app.
Review some common troubleshooting techniques for App Platform.
## Backups 
The only way to restore files from an image is to recreate a Droplet or volume from the image and copy the flies from there.
Yes, you can choose between daily and weekly backups and customize the backup window.
Convert your backups to snapshots to save them indefinitely.
You cannot currently download DigitalOcean backups or snapshots, but you can use third-party tools to save your data locally.
Creating a backup or snapshot takes roughly 2 minutes per GB of used space.
## Bare Metal GPUs 
You can request BIOS-level changes to bare metal GPUs through a support ticket. Some changes require reprovisioning.
Public speed test servers may not accurately reflect network performance in data center environments. Use tools like `iperf` or real-world endpoints for accurate testing.
## Billing 
We use payment information to verify your identity, which allows us to keep DigitalOcean safe against spammers and bots.
When you connect PayPal as a payment method, the small prepayment verifies your account.
We do not offer refunds.
No, you cannot prepay for DigitalOcean support plans.
Apple Pay is available on the Safari browser. Try these troubleshooting steps if Apple Pay isn’t visible on your account.
Google Pay is available on Chromium-based browsers like Chrome, Brave, and Microsoft Edge. Sometimes there are issues with password managers like 1Password. Try these troubleshooting steps if Google Pay isn’t visible on your account.
Download the CSV version of your invoice for more detailed billing information.
We do not offer extensions, but we can help you find other solutions.
You can edit your personal account settings on the **My Account** page. You can edit your team settings on the **Settings** page. You can update your billing address, tax location, or add a tax ID on the **Billing Settings** page.
Your card may be declined for a number of reasons, including banking restrictions, unavailable funds, or trying to use a prepaid card.
Once you pay a past-due balance, you need to manually turn your resources (like Droplets) back on using the control panel.
## Cloudways 
No, support plans apply only to DigitalOcean.
## Container Registry 
Try to reupload the image to see if it resolves the issue.
## DDoS 
We temporarily trigger a blackhole when a DDoS attack against a resource reaches a mitigation limit. We recommend contacting support and planning strategies to keep your resources online in the future.
Next steps to take if you receive a message from DigitalOcean support because your Droplet is sending an outgoing flood or DDoS.
## DNS 
Use the app’s Settings tab to remove domains associated with App Platform apps.
If you use vanity or branded DNS nameservers that delegate to DigitalOcean’s nameservers, you must update to new IP addresses.
Update your registrar to use DigitalOcean’s name servers.
App Platform provides two static ingress IPs you can use to map A records to your app.
No, we do not support DNSSEC.
You cannot import a DNS zone, but you can add the domain and manually create the DNS records.
A domain could fail to resolve because the name server changes did not completely propagate, `DNSSEC` or the domain registrar needs verification, the DigitalOcean name servers are not configured at your registrar, or there are different name server providers active.
Use Punycode to add a non-ASCII domain name to DigitalOcean.
We do not support directly transferring domain ownership from one team to another. Instead, you can download a zone file with all of the domain’s DNS information.
Delete the Let’s Encrypt certificate associated with the domain in your account’s Settings section.
To debug your network configuration, verify the Droplet’s network interfaces and check its network configuration file.
Our DNS recursive servers now require Authoritative Answer flags when resolving host names.
## Droplets 
Make sure NVIDIA Fabric Manager is running and has the same version number as the GPU drivers.
There may be an issue with the autoscale pool or Droplet configuration, the VPC network’s size, or resource limits on the team or datacenter.
Health checks often fail due to firewalls or misconfigured backend server software.
Boot the Droplet from the recovery ISO, then connect using the Recovery Console and delete files to free some disk space.
You can disable the address on your Droplet from the command line or through updating your Droplet’s `eth1` interface configuration.
You can access your Droplet’s file manager by connecting to the Droplet using SSH or the Droplet Console.
Ensure your Droplet’s public and private network interfaces are correctly named `eth0` and `eth1`.
You cannot convert a Droplet IP address into a Reserved IP.
You cannot undo restoring a Droplet from a backup, but you can use an existing snapshot to restore a Droplet to a previous point in time.
All Droplets are assigned IPs that are owned by DigitalOcean, which is headquartered in the US.
Attaching a volume adds separate storage and does not increase a Droplet’s root disk size.
Older Droplets that did not have VPC enabled prior to October 2020 cannot be added to a VPC network without changing its IP address.
Edit your Droplet’s sshd_config file to change its SSH port.
You cannot retain a Droplet’s IPv4 when you transfer the Droplet to a new region. Use a reserved IP address to maintain a static IP address.
Take a snapshot of your Droplet and then create new Droplet from the snapshot in the new datacenter.
You cannot create Droplets in certain datacenters due to limited capacity. If you have snapshots in a limited capacity datacenter, transfer them to another datacenter to create Droplets from them.
You cannot downsize a Droplet from a snapshot. Data is not always stored sequentially in memory, so reducing the size of a disk can result in data loss or corruption.
You cannot create Droplets with a specific IP address, but you can use reserved IPs for a static address that you can migrate between Droplets.
Create a snapshot of the Droplet, then create a new Droplet from that snapshot.
To rename your Droplet, change the Droplet’s name in the control panel, then change its hostname from the command line using `hostnamectl` or by editing `/etc/hostname` and `/etc/hosts`.
Droplets do not have a dedicated IP address, but you can create a Reserved IP, which is a reassignable static IP address.
Transfer files over SSH with SFTP.
We do not email a Droplet’s root password. You can reset your root password if you don’t remember it.
Diagnose and troubleshoot firewall issues that could be causing network connectivity issues.
To debug your network configuration, verify the Droplet’s network interfaces and check its network configuration file.
If you lose the private SSH key you use to log in to a Droplet, you need to re-enable password authentication to recover access.
You may be receiving this error for various reasons, including a missing SSH key or incorrect password.
Older operating systems can pose large security risks.
You can recover your Droplet if you took a snapshot of the Droplet, enabled automated backups, or used SnapShooter for Droplet backups.
No, but you can use reserved IPs to assign the same address to new or redeployed Droplets.
You can review disk usage on your Droplet and then remove unnecessary files.
You cannot resize Droplets to smaller plans, but you can migrate your data to a smaller Droplet.
No, we do not provide Windows images for Droplets or support Windows custom images.
Convert your backups to snapshots to save them indefinitely.
We have guides to help you migrate your data from your previous provider.
Use the recovery ISO to access Droplets that fail to boot up or have system problems.
You can typically install an SSL certificate by adding a few lines of configuration to the Droplet’s web server, or by using tools that automatically add the configuration for you.
File system corruption can cause a Droplet to boot into read only mode.
You can reset your Droplet’s password using the control panel or the recovery ISO.
High RAM or CPU usage is normally the result of applications or kernel processes on the Droplet. You can monitor high CPU usage processes on the Droplet and stop them if necessary.
Yes, you can point an unlimited number of domains to a single Droplet, and you can serve multiple websites from a single Droplet.
SMTP is blocked on Droplets to prevent spam and abuse. Use a third-party email as a service provider instead.
You can check to see if a Droplet’s migration has completed by checking its history.
There are three ways to manually back up a Droplet. You can create a DigitalOcean snapshot for an on-demand full disk image, convert an automatic DigitalOcean backup into a snapshot, or use a third-party tool for a partial backup.
You can transfer snapshots of Droplets to others by email address or by team.
Problems with SSH authentication includes permission denied with SSH keys and passwords.
Problems with SSH connectivity include hostname resolution errors and connections being refused or timing out.
Next steps to take if you receive a message from DigitalOcean support because your Droplet is sending an outgoing flood or DDoS.
Problems during SSH protocol initiation include the client suddenly getting dropped or closed, the client returning errors about cipher negotiation, or issues with an unknown or changed remote host.
Problems with SSH shell environments include being unable to fork a process, the system reporting it’s not a valid shell, or issues reaching the home directory.
## Firewalls 
Diagnose and troubleshoot firewall issues that could be causing network connectivity issues.
Use this guide to gather information about your firewalls and diagnose problems.
Configure your firewall to allow outgoing traffic through ports 80 and 443.
## Functions 
Functions does not support forwarding to Managed OpenSearch.
The function handler needs to return a response object to HTTP requests from Postman or curl.
## DigitalOcean Gradient™ AI Platform 
Create a scheduled function to trigger automatic knowledge base reindexing.
## IPv6 
You can disable IPv6 by modifying your Droplet’s network interface configuration.
Addresses assigned to a Droplet remain static for the life of the Droplet.
Diagnose and troubleshoot firewall issues that could be causing network connectivity issues.
Use this guide to gather information about your firewalls and diagnose problems.
Configure your firewall to allow outgoing traffic through ports 80 and 443.
## Kafka 
Verify the connection string, ensure correct port usage, and add your local machine to the database cluster’s trusted sources.
Add your machine to the database cluster’s list of trusted sources in the firewall settings.
## Kubernetes 
Gather information to resolve CoreDNS-related DNS problems in DOKS clusters.
For Droplets created before 2 October 2024, you must manually add VPC peering routes to interconnect with VPC-native DOKS clusters
Health checks often fail due to firewalls or misconfigured backend server software.
Enable DNS caching, use non-shared machine types for the cluster, and scale out or reduce DNS traffic.
Edit the ConfigMap which nginx uses to enable PROXY protocol.
Launch an Init Container or run a DaemonSet.
Displaying CPU and memory usage in the Kubernetes Dashboard is not supported at this time.
The output of the `kubectl top` command does not measure the entire system load in the same way the control panel does.
A node can show as NotReady if it is unhealthy and not accepting pods.
You can configure load balancers that are provisioned by DOKS using Kubernetes service annotations.
Kubernetes service ’externaltrafficpolicy’ field controls how nodes respond to health checks.
You can resize a DOKS node by creating a new node pool of the desired size.
Recommended solutions for common errors raised by Clusterlint, a non-invasive best practices checker for DigitalOcean Kubernetes clusters.
## Load Balancers 
Health checks often fail due to firewalls or misconfigured backend server software.
Edit the ConfigMap which nginx uses to enable PROXY protocol.
By default, load balancers time out after the connection has been idle for 60 seconds. You can customize the timeout duration.
Load balancers return 503 errors when there are either no Droplets assigned to them or all of the assigned Droplets are unhealthy.
Your load balancer may be down or not directing traffic to the target Droplet.
You can configure load balancers that are provisioned by DOKS using Kubernetes service annotations.
Kubernetes service ’externaltrafficpolicy’ field controls how nodes respond to health checks.
Enable PROXY protocol support on your Droplets.
## MongoDB 
Remove the _id field from your JSON data so MongoDB can automatically generate unique _id values for each document during import.
Use a public DNS server, such as Google’s 8.8.8.8, to resolve SRV lookups required by MongoDB’s connection string.
Increase your cluster’s disk space or delete data to unblock your MongoDB database.
Verify the connection string, ensure correct port usage, and add your local machine to the database cluster’s trusted sources.
Add your machine to the database cluster’s list of trusted sources in the firewall settings.
Verify the format and values in the connection string for typos or formatting errors.
Prepend your database client command to the connection string.
We are currently processing the cluster, most likely for maintenance. You can expect no downtime or performance issues.
## Monitoring 
Modify your metrics agent’s configuration on `systemctl` or `initctl` systems to disable process name collection.
You must install the DigitalOcean metrics agent to enable alerts for your Droplets.
Configure your firewall to allow outgoing traffic through ports 80 and 443.
## MySQL 
Update backup user permissions, remove the –single-transaction flag, or downgrade mysqldump.
Use MySQL’s import command instead of source for handling large data imports.
Remove or replace the DEFINER in the dump file.
Adjust the sort_buffer_size value while assessing its impact on memory consumption and query performance.
Verify your connection string, login credentials, and user permissions.
Verify the connection string, ensure correct port usage, and add your local machine to the database cluster’s trusted sources.
Add your machine to the database cluster’s list of trusted sources in the firewall settings.
Check for query timeouts and ensure your network connection is stable.
Verify the format and values in the connection string for typos or formatting errors.
Check your network connection and optimize your query.
Prepend your database client command to the connection string.
Ensure the hostname is correct and confirm the database exists in your specified cluster.
Verify the hostname is correct and check for DNS resolution issues.
Update user settings or change the password type to resolve authentication errors in MySQL.
Upgrade your client to support TLSv1.2 or TLSv1.3 for secure MySQL connections.
We are currently processing the cluster, most likely for maintenance. You can expect no downtime or performance issues.
## Networking 
We temporarily trigger a blackhole when a DDoS attack against a resource reaches a mitigation limit. We recommend contacting support and planning strategies to keep your resources online in the future.
You can disable the address on your Droplet from the command line or through updating your Droplet’s `eth1` interface configuration.
Ensure your Droplet’s public and private network interfaces are correctly named `eth0` and `eth1`.
Addresses assigned to a Droplet remain static for the life of the Droplet.
Use this guide to gather information about your firewalls and diagnose problems.
Our DNS recursive servers now require Authoritative Answer flags when resolving host names.
Configure your firewall to allow outgoing traffic through ports 80 and 443.
Yes, you can point an unlimited number of domains to a single Droplet, and you can serve multiple websites from a single Droplet.
SMTP is blocked on Droplets to prevent spam and abuse. Use a third-party email as a service provider instead.
## Opensearch 
Functions does not support forwarding to Managed OpenSearch.
Verify the connection string, ensure correct port usage, and add your local machine to the database cluster’s trusted sources.
Add your machine to the database cluster’s list of trusted sources in the firewall settings.
## Paperspace 
To continue using Paperspace as a VDI solution, migrate to a [dedicated GPU machine](https://docs.digitalocean.com/products/paperspace/pricing/).
No, support plans apply only to DigitalOcean.
## PostgreSQL 
Update the user’s privileges to `CREATE`, `USAGE`, or `ALL` on the public schema.
Use the command CREATE EXTENSION vector; instead of pgvector.
Add the –no-role-passwords flag to the pg_dumpall command.
Resolve the pg_dump server version mismatch by upgrading pg_dump, matching it to the server version, or using a third-party backup tool.
Verify the database cluster, username, and password.
Verify the connection string, ensure correct port usage, and add your local machine to the database cluster’s trusted sources.
Add your machine to the database cluster’s list of trusted sources in the firewall settings.
Verify the hostname and check your local machine for DNS resolution issues.
Verify the hostname and confirm the database exists in the specified cluster.
Verify the format and values in the connection string for typos or formatting errors.
Prepend your database client command to the connection string.
We are currently processing the cluster, most likely for maintenance. You can expect no downtime or performance issues.
## Reserved IPs 
You cannot convert a Droplet IP address into a Reserved IP.
You cannot retain a Droplet’s IPv4 when you transfer the Droplet to a new region. Use a reserved IP address to maintain a static IP address.
You cannot create Droplets with a specific IP address, but you can use reserved IPs for a static address that you can migrate between Droplets.
Droplets do not have a dedicated IP address, but you can create a Reserved IP, which is a reassignable static IP address.
## SnapShooter 
Either remount the tmp folder with exec permissions or set the backup engine to use the home directory instead.
## Snapshots 
The only way to restore files from an image is to recreate a Droplet or volume from the image and copy the flies from there.
You cannot create Droplets in certain datacenters due to limited capacity. If you have snapshots in a limited capacity datacenter, transfer them to another datacenter to create Droplets from them.
You cannot downsize a Droplet from a snapshot. Data is not always stored sequentially in memory, so reducing the size of a disk can result in data loss or corruption.
Snapshots of Droplets are a best estimate based on the disk usage. Snapshots of volumes operate at the block storage level, so the snapshot size may not match what the filesystem reports.
This error happens when the Droplet you’re trying to restore no longer exists, so try creating a new Droplet from the snapshot instead.
No, but you can use reserved IPs to assign the same address to new or redeployed Droplets.
You cannot currently download DigitalOcean backups or snapshots, but you can use third-party tools to save your data locally.
Creating a backup or snapshot takes roughly 2 minutes per GB of used space.
## Spaces 
Create another bucket to transfer data to, save your files locally, or use an automatic backup tool.
## Teams 
You can only transfer Droplet Snapshots directly to another account or team. You have to migrate other resources manually to another account or team.
No, each team needs their own plan.
We do not support directly transferring domain ownership from one team to another. Instead, you can download a zone file with all of the domain’s DNS information.
Team collaboration is built into the DigitalOcean experience from sign-up.
You can transfer snapshots of Droplets to others by email address or by team.
## Third-Party Applications 
You can renew your certificate manually using Certbot.
You can install cPanel and WHM on AlmaLinux, Rocky, and Ubuntu Droplets.
No, we do not provide Windows images for Droplets or support Windows custom images.
Yes, you can serve multiple WordPress instances from a single Droplet.
## Volumes 
Block storage volumes can only be attached to one Droplet at a time. You can share data using a network filesystem instead.
Attaching a volume adds separate storage and does not increase a Droplet’s root disk size.
Differences in filesystem overhead, reserved space, and unit conversions can make a resized volume appear smaller than its allocated size.
## VPC 
Older Droplets that did not have VPC enabled prior to October 2020 cannot be added to a VPC network without changing its IP address.
### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
