# OpenSearch
Generated on 14 Jan 2026 from [the OpenSearch catalog page](https://marketplace.digitalocean.com/apps/opensearch)
OpenSearch is a community-driven, open source search and analytics suite derived from Apache 2.0 licensed Elasticsearch 7.10.2 & Kibana 7.10.2. It consists of a search engine daemon, OpenSearch, and a visualization and user interface, OpenSearch Dashboards. OpenSearch enables people to easily ingest, secure, search, aggregate, view, and analyze data.
These capabilities are popular for use cases such as application search, log analytics, and more. With OpenSearch people benefit from having an open source product they can use, modify, extend, monetize, and resell how they want. At the same time, OpenSearch will continue to provide a secure, high-quality search and analytics suite with a rich roadmap of new and innovative functionality.
## Software Included 
Package | Version | License  
---|---|---  
3.4.0 | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  
[OpenSearch Dashboards](https://opensearch.org/) | 3.4.0 | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  
## Creating an App using the Control Panel 
Click the **Deploy to DigitalOcean** button to create a Droplet based on this 1-Click App. If you aren’t logged in, this link will prompt you to log in with your DigitalOcean account.
## Creating an App using the API 
In addition to creating a Droplet from the OpenSearch 1-Click App using the control panel, you can also use the [DigitalOcean API](https://docs.digitalocean.com/reference/api). As an example, to create a 4GB OpenSearch Droplet in the SFO2 region, you can use the following `curl` command. You need to either save your [API access token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) to an environment variable or substitute it in the command below.
```
curl -X POST -H 'Content-Type: application/json' \
         -H 'Authorization: Bearer '$TOKEN'' -d \
        '{"name":"choose_a_name","region":"sfo2","size":"s-2vcpu-4gb","image":"sharklabs-opensearch"}' \
        "https://api.digitalocean.com/v2/droplets"
```

## Getting Started After Deploying OpenSearch 
Once the droplet is ready, you should ssh to it using:
```
ssh root@your_droplet_public_ipv4
```

The initial message as you ssh into the box is going to show you the password for the `admin` user that you can use to make requests to OpenSearch and OpenSearch Dashboards.
With the password, head to <https://your_droplet_public_ipv4:5601/> to access OpenSearch Dashboards to start playing around with your deployment. This is going to require the password for the `admin` user you got after ssh-ing into the Droplet.
This 1 Click uses a self-signed TLS certificate so you’ll have to either disable TLS certificates checks on your OpenSearch clients or get it from the Droplet and configure it on your clients. The file lives at `/opt/opensearch/config/root-ca.pem`.
### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
Cookie Preferences
