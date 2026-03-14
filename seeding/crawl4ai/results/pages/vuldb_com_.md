[VDB-263991](https://vuldb.com/?id.263991 "VulDB") · [CVE-2024-31460](https://vuldb.com/?source_cve.263991 "Cve") · [GCVE-0-2024-31460](https://vuldb.com/?kb.gcve "Gcve")
# Cacti up to 1.2.26 automation_tree_rules.php create_all_header_nodes sql injection
CVSS Meta Temp ScoreCVSS is a standardized scoring system to determine possibilities of attacks. The Temp Score considers temporal factors like disclosure, exploit and countermeasures. The unique Meta Score calculates the average score of different sources to provide a normalized scoring system. | Current Exploit Price (≈)Our analysts are monitoring exploit markets and are in contact with vulnerability brokers. The range indicates the observed or calculated exploit price to be seen on exploit markets. A good indicator to understand the monetary effort required for and the popularity of an attack. | CTI Interest ScoreOur Cyber Threat Intelligence team is monitoring different web sites, mailing lists, exploit markets and social media networks. The CTI Interest Score identifies the interest of attackers and the security community for this specific vulnerability in real-time. A high score indicates an elevated risk to be targeted for this vulnerability.  
---|---|---  
7.1 | $0-$5k | 0.00  
## Summary 
A vulnerability was found in [Cacti up to 1.2.26](https://vuldb.com/?product.cacti). It has been rated as [critical](https://vuldb.com/?kb.risk). This affects the function `create_all_header_nodes` in the library _lib/api_automation.php_ of the file _automation_tree_rules.php_. Performing a manipulation results in sql injection. This vulnerability is identified as [CVE-2024-31460](https://vuldb.com/?source_cve.263991). The attack can be initiated remotely. There is not any exploit available. Upgrading the affected component is advised.
## Details 
A vulnerability, which was classified as critical, was found in [Cacti up to 1.2.26](https://vuldb.com/?product.cacti). This affects the function `create_all_header_nodes` in the library _lib/api_automation.php_ of the file _automation_tree_rules.php_. The manipulation with an unknown input leads to a sql injection vulnerability. CWE is classifying the issue as [CWE-89](https://vuldb.com/?vulnerability_cwe.263991 "Cwe"). The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component. This is going to have an impact on confidentiality, integrity, and availability. The summary by CVE is:
> Cacti provides an operational monitoring and fault management framework. Prior to version 1.2.27, some of the data stored in `automation_tree_rules.php` is not thoroughly checked and is used to concatenate the SQL statement in `create_all_header_nodes()` function from `lib/api_automation.php` , finally resulting in SQL injection. Using SQL based secondary injection technology, attackers can modify the contents of the Cacti database, and based on the modified content, it may be possible to achieve further impact, such as arbitrary file reading, and even remote code execution through arbitrary file writing. Version 1.2.27 contains a patch for the issue.
It is possible to read the advisory at [github.com](https://vuldb.com/?advisory_url.263991). This vulnerability is uniquely identified as [CVE-2024-31460](https://vuldb.com/?source_cve.263991 "Cve") since 04/03/2024. The exploitability is told to be easy. It is possible to initiate the attack remotely. Technical details of the vulnerability are known, but there is no available exploit. The attack technique deployed by this issue is [T1505](https://vuldb.com/?vulnerability_attck.263991 "Attck") according to MITRE ATT&CK. 
By approaching the search of [inurl:automation_tree_rules.php](https://vuldb.com/?exploit_googlehack.263991) it is possible to find vulnerable targets with Google Hacking. 
Upgrading to version 1.2.27 eliminates this vulnerability.
Entries connected to this vulnerability are available at [VDB-263998](https://vuldb.com/?id.263998) and [VDB-293583](https://vuldb.com/?id.293583).
## Product 
**Type**
  * [Log Management Software](https://vuldb.com/?type.log_management_software)


**Name**


**Version**


**License**


**Website**
  * Product: <https://github.com/Cacti/cacti/>


## CPE 2.3 
## CPE 2.2 
## CVSSv4 
VulDB Vector: VulDB Reliability: 
## CVSSv3 
VulDB Meta Base Score: 7.2VulDB Meta Temp Score: 7.1VulDB Base Score: [6.3](https://www.first.org/cvss/v3.1/specification-document#Base-Metrics)VulDB Temp Score: [6.0](https://www.first.org/cvss/v3.1/specification-document#Temporal-Metrics)VulDB Vector: VulDB Reliability: NVD Base Score: [8.8](https://vuldb.com/?source_nvd.263991)NVD Vector: CNA Base Score: [6.5](https://vuldb.com/?source_nvd.263991)CNA Vector: 
## CVSSv2 
[ AV | AC | Au | C | I | A  
---|---|---|---|---|---  
💳 | 💳 | 💳 | 💳 | 💳 | 💳  
💳 | 💳 | 💳 | 💳 | 💳 | 💳  
💳 | 💳 | 💳 | 💳 | 💳 | 💳  
Vector | Complexity | Authentication | Confidentiality | Integrity | Availability  
---|---|---|---|---|---  
Unlock | Unlock | Unlock | Unlock | Unlock | Unlock  
Unlock | Unlock | Unlock | Unlock | Unlock | Unlock  
Unlock | Unlock | Unlock | Unlock | Unlock | Unlock ](https://vuldb.com/?pay)VulDB Base Score: VulDB Temp Score: VulDB Reliability:   
## Exploiting 
Class: Sql injectionCWE: [CWE-89 / CWE-74 / CWE-707](https://vuldb.com/?vulnerability_cwe.263991 "Cwe")CAPEC: ATT&CK: Physical: NoLocal: NoRemote: YesAvailability: Status: Not definedGoogle Hack: EPSS Score: EPSS Percentile: Price Prediction: Current Price Estimation: [ 0-Day | Unlock | Unlock | Unlock | Unlock  
---|---|---|---|---  
Today | Unlock | Unlock | Unlock | Unlock ](https://vuldb.com/?pay)  
## Threat Intelligence 
Interest: Active Actors: Active APT Groups: 
## Countermeasures 
Recommended: UpgradeStatus: 0-Day Time: Upgrade: Cacti 1.2.27
## Timeline 
04/03/2024 05/13/2024 +40 days 05/13/2024 +0 days 12/18/2024 +219 days
## Sources 
Product: [github.com](https://github.com/Cacti/cacti/)Advisory: [github.com](https://vuldb.com/?advisory_url.263991 "Advisory")Status: ConfirmedCVE: [CVE-2024-31460](https://vuldb.com/?source_cve.263991 "Cve") ()GCVE (CVE): [GCVE-0-2024-31460](https://vuldb.com/?kb.gcve)GCVE (VulDB): [GCVE-100-263991](https://vuldb.com/?kb.gcve)See also: 
## Entry 
Created: 05/13/2024 17:48Updated: 12/18/2024 22:03Changes: [05/13/2024 17:48 (65), 12/18/2024 22:03 (13)](https://vuldb.com/?diff.263991)Complete: Cache ID: 86:449:81
## Discussion
No comments yet. Languages: en.
[Please log in to comment.](https://vuldb.com/?login)
[◂ Previous](https://vuldb.com/?id.263990)[Overview](https://vuldb.com/?live.recent)[Next ▸](https://vuldb.com/?id.263992)
# Are you interested in using VulDB?
Download the whitepaper to learn more about our service!
