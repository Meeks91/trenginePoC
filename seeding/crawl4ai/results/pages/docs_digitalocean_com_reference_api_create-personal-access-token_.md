# How to Create a Personal Access Token
Validated on 1 Aug 2024 • Last edited on 10 Dec 2025
To use the DigitalOcean API, you need to generate a personal access token. Personal access tokens function like ordinary OAuth access tokens. You use them to authenticate to the API by including one in a bearer-type `Authorization` header with your request.
**Keep your tokens secret.** They function like passwords. Do not hard code your tokens into programs where they may accidentally be released in version control and are harder to rotate. Instead, use environment variables. If a token becomes compromised, delete it to revoke that token’s access. 
## About Custom Scopes 
Previously, DigitalOcean personal access tokens (PATs) [had two scopes](https://docs.digitalocean.com/notes/2024/custom-scope-token-ga/): read access to all team resources or full (read and write) access to all team resources.
Custom scopes grant more specific permissions, like only creating Droplets or updating cloud firewalls, which lets you secure your workflows by granting only the permissions the token needs and restricting access to other resources and actions.
Generally, the [CRUD scopes](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) map to equivalent actions on the associated kind of resource:
  * _Create_ scope lets you create the resource type and perform additive actions within that resource type. For example, `database:create` lets you create database clusters and create new users or databases within that cluster.
  * _Read_ scope lets you view information about a resource by type and also view information that the resource returns. For example, `app:read` lets you view App Platform apps and their logs.
  * _Update_ scope allows you modify a resource type and perform actions that would otherwise modify a resource. For example, `droplet:update` lets you power a Droplet on or off.
  * _Delete_ scope lets you delete a resource by type and perform actions that delete information about the resource type. For example, `database:delete` lets you delete databases from a database cluster and remove existing users from a database.


Each custom scope correlates to one [public API endpoint](https://docs.digitalocean.com/reference/api/digitalocean/).
## Creating a Token 
To generate a personal access token, log in to [the DigitalOcean Control Panel](https://cloud.digitalocean.com).
In the left menu, click **API** , which takes you to the **Applications & API** page on the **Tokens** tab. In the **Personal access tokens** section, click the **Generate New Token** button.
On the **Create A New Personal Access Token** page, fill out the fields:
  * **Token name**. Choose a name for the token. This is for your own reference.
  * **Expiration**. Choose when the token expires. After the interval passes, the token can no longer authenticate you to the API and it disappears from your account.
  * **Scopes**. Choose the permissions that define which resources and actions the token can access. The available options are based on your [team role](https://docs.digitalocean.com/platform/teams/roles/).
    * **Custom Scopes** lets you select specific scopes from the full list of scopes available to you based on your team role.
If a team owner expands the permissions of your team role, a token with custom scopes maintains its original scopes and does not include any new scopes.
    * **Read Only** grants the token read scope for all resources available based on the permissions of your team role.
If a team owner expands the read permissions of your team role, a read only token reflects the updated permissions.
    * **Full Access** grants the token all scopes available based on the permissions of your team role.
If a team owner expands the permissions of your team role, a full access token reflects the updated permissions.


If a team owner restricts the permissions of your team role, those permissions are also no longer available to any existing tokens.
You can use the **Quick bulk scope select** to select all scopes for any CRUD action, **Search by resource type** to look for a scope by name, or select and expand sections in the full list:
The bottom of the page displays the summary of custom chosen scopes. When you finish selecting your options, click **Generate Token** to create the token and return to the **Applications & API** page. Save the displayed token. For security purposes, the secret is only shown once.
You can use tokens with custom scopes in the same way as previous tokens. If you try to use a token to call an endpoint that requires a scope the token does not have, the API returns a 403 Forbidden response.
## Managing Tokens with Custom Scopes 
In the **Personal access tokens** section, you can view the scopes for existing tokens.
You can click the entry in the **Scopes** column to view details about the token’s usage and scopes.
In the **…** menu for a token, you can rename, regenerate, or delete the token.
## Limits 
  * You cannot edit the scope of a token after creation. You can rename and regenerate tokens with custom scopes.


### We can't find any results for your search.
Try using different keywords or simplifying your search terms.
