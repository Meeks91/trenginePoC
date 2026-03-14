# VictoriaMetrics Single
Generated on 14 Jan 2026 from [the VictoriaMetrics Single catalog page](https://marketplace.digitalocean.com/apps/victoriametrics-single)
**VictoriaMetrics** is a free [open source](https://en.wikipedia.org/wiki/Open-source_software) [time series database](https://en.wikipedia.org/wiki/Time_series_database) (TSDB) and monitoring solution, designed to collect, store and process real-time metrics.
It supports the [Prometheus](https://en.wikipedia.org/wiki/Prometheus_\(software\)) pull model and various push protocols ([Graphite](https://en.wikipedia.org/wiki/Graphite_\(software\)), [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB), OpenTSDB) for data ingestion. It is optimized for storage with high-latency IO, low IOPS and time series with [high churn rate](https://docs.victoriametrics.com/FAQ.html#what-is-high-churn-rate).
For reading the data and evaluating alerting rules, [VictoriaMetrics](https://victoriametrics.com) supports the PromQL, [MetricsQL](https://docs.victoriametrics.com/metricsql/) and Graphite query languages. VictoriaMetrics Single is fully autonomous and can be used as a long-term storage for time series.
VictoriaMetrics Single = Hassle-free monitoring solution. Easily handles 10M+ of active time series on a single instance. Perfect for small and medium environments.
## Software Included 
Package | Version | License  
---|---|---  
[VictoriaMetrics Single](https://docs.victoriametrics.com/victoriametrics/)  
## Creating an App using the Control Panel 
Click the **Deploy to DigitalOcean** button to create a Droplet based on this 1-Click App. If you aren’t logged in, this link will prompt you to log in with your DigitalOcean account.
## Creating an App using the API 
In addition to creating a Droplet from the VictoriaMetrics Single 1-Click App using the control panel, you can also use the [DigitalOcean API](https://docs.digitalocean.com/reference/api). As an example, to create a 4GB VictoriaMetrics Single Droplet in the SFO2 region, you can use the following `curl` command. You need to either save your [API access token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) to an environment variable or substitute it in the command below.
```
curl -X POST -H 'Content-Type: application/json' \
         -H 'Authorization: Bearer '$TOKEN'' -d \
        '{"name":"choose_a_name","region":"sfo2","size":"s-2vcpu-4gb","image":"victoriametrics-victoriametricss"}' \
        "https://api.digitalocean.com/v2/droplets"
```

## Getting Started After Deploying VictoriaMetrics Single 
### Config 
VictoriaMetrics configuration is located at `/etc/victoriametrics/single/scrape.yml` on the droplet.
This One Click app uses 8428, 2003, 4242 and 8089 ports to accept metrics from different protocols. It’s recommended to disable ports for protocols which are not needed. [Ubuntu firewall](https://help.ubuntu.com/community/UFW) can be used to easily disable access for specific ports.
### Scraping metrics 
VictoriaMetrics supports metrics scraping in the same way as Prometheus does. Check the configuration file to edit scraping targets. See more details about scraping at [How to scrape Prometheus exporters](https://docs.victoriametrics.com/single-server-victoriametrics/#how-to-scrape-prometheus-exporters-such-as-node-exporter).
### Sending metrics 
Besides scraping, VictoriaMetrics accepts write requests for various ingestion protocols. This One Click app supports the following protocols:
  * [OpenTelemetry metrics format](https://docs.victoriametrics.com/single-server-victoriametrics/#sending-data-via-opentelemetry)



  * [Prometheus](https://docs.victoriametrics.com/single-server-victoriametrics/#how-to-import-data-in-prometheus-exposition-format) on port :8428
  * [Graphite (statsd)](https://docs.victoriametrics.com/single-server-victoriametrics/#how-to-send-data-from-graphite-compatible-agents-such-as-statsd) on port :2003 tcp/udp
  * [OpenTSDB](https://docs.victoriametrics.com/single-server-victoriametrics/#how-to-send-data-from-opentsdb-compatible-agent) on port :4242
  * Influx (telegraph) on port :8089 tcp/udp


See more details and examples in [official documentation](https://docs.victoriametrics.com/single-server-victoriametrics/).
### UI 
VictoriaMetrics provides a [User Interface (UI)](https://docs.victoriametrics.com/single-server-victoriametrics/#vmui) for query troubleshooting and exploration. The UI is available at `http://your_droplet_public_ipv4:8428/vmui`. It lets users explore query results via graphs and tables.
To check it, open the following in your browser `http://your_droplet_public_ipv4:8428/vmui` and then enter `vm_app_uptime_seconds` to the Query Field to Execute the Query.
Run the following command to query and retrieve a result from VictoriaMetrics Single with `curl`:
```
curl -sg http://your_droplet_public_ipv4:8428/api/v1/query_range?query=vm_app_uptime_seconds | jq
```

### Accessing 
Once the Droplet is created, you can use DigitalOcean’s web console to start a session or SSH directly to the server as root:
```
ssh root@your_droplet_public_ipv4
```

### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
