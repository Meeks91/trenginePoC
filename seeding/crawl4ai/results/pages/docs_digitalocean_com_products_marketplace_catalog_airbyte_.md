# Airbyte
Generated on 11 Nov 2021 from [the Airbyte catalog page](https://marketplace.digitalocean.com/apps/airbyte)
The open platform that unifies all your data pipelines
Replicate your data in minutes with pre-built and custom connectors. Meet all your specific needs with the flexibility of open-source
## Software Included 
_This Marketplace listing does not include a detailed software list._
## Creating an App using the Control Panel 
Click the **Deploy to DigitalOcean** button to create a Droplet based on this 1-Click App. If you aren’t logged in, this link will prompt you to log in with your DigitalOcean account.
## Creating an App using the API 
In addition to creating a Droplet from the Airbyte 1-Click App using the control panel, you can also use the [DigitalOcean API](https://docs.digitalocean.com/reference/api). As an example, to create a 4GB Airbyte Droplet in the SFO2 region, you can use the following `curl` command. You need to either save your [API access token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) to an environment variable or substitute it in the command below.
```
curl -X POST -H 'Content-Type: application/json' \
         -H 'Authorization: Bearer '$TOKEN'' -d \
        '{"name":"choose_a_name","region":"sfo2","size":"s-2vcpu-4gb","image":"airbyte"}' \
        "https://api.digitalocean.com/v2/droplets"
```

## Getting Started After Deploying Airbyte 
When your droplet is up and running check for
  1. Docker is up and running
  2. `docker ps` shows all the required containers if not `cd airbyte` && `docker-compose up`
  3. Hurray you can access it at http://your_droplet_public_ipv4:8000


You can change the .env and docker-compose variables similar to instructions here <https://docs.airbyte.io/deploying-airbyte/on-aws-ec2>.
### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
