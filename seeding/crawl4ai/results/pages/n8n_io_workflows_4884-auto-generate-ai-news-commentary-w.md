  * [ Google Sheets ](https://n8n.io/integrations/google-sheets/)
  * [ HTTP Request ](https://n8n.io/integrations/http-request/)
  * [No Operation, do nothing](https://n8n.io/integrations/no-operation-do-nothing/)


# 
Auto-generate AI news commentary with Dumpling AI and GPT-4o
Use for free 
Created by
Last update
Last update 16 days ago 
Categories


Share
This workflow turns trending news into thoughtful first-person commentary for platforms like LinkedIn. It uses **Dumpling AI’s News Search and Scraping APIs** to find and extract article content, then feeds the cleaned text to **GPT-4o** to write personalized insights. The final output is saved back to **Google Sheets** as a draft for easy review or posting.
### ✅ What this workflow does
  1. **Triggers daily** using a Schedule node.
  2. **Fetches a list of content topics** from a Google Sheet.
  3. **Uses Dumpling AI** to search for relevant news articles based on each topic.
  4. **Scrapes the article content** with Dumpling AI’s `/scrape` endpoint.
  5. **Cleans and aggregates the article content** using a Code node.
  6. **Generates first-person commentary** with GPT-4o tailored for LinkedIn.
  7. **Appends the generated post** back to the Google Sheet next to its topic.


### 🧩 Nodes in this workflow
  * **Schedule Trigger** : Starts the workflow daily.
  * **Google Sheets (Read Topics)** : Pulls topic rows that don’t have a generated commentary yet.
  * **Split In Batches** : Processes each topic one at a time.
  * **Wait** : Adds a delay to manage API limits.
  * **HTTP Request (Search News)** : Uses Dumpling AI's `/search-news` to find relevant articles for the topic.
  * **Split Out** : Iterates over the list of article results.
  * **HTTP Request (Scrape Article)** : Extracts the full article text using Dumpling AI’s `/scrape`.
  * **Aggregate** : Collects and merges article content fields.
  * **Code (Clean Article)** : Strips links, formatting, and irrelevant text.
  * **OpenAI (GPT-4o)** : Generates a short, first-person LinkedIn post-style commentary using a custom prompt.
  * **Google Sheets (Write Back)** : Appends the final output next to the original topic in the sheet.


### 🧑‍💼 Who is this for?
  * **Founders, content creators, marketers** , or **agency teams** looking to maintain an active presence on LinkedIn or newsletters by sharing smart takes on industry trends.


### 💡 What problem does this solve?
Most people want to comment on current events but don't have the time to summarize articles or write well-structured posts. This automation saves hours of manual work by:
  * Finding the right article.
  * Extracting and cleaning the content.
  * Writing it in a natural, first-person voice using AI.


### ⚙️ What you need to use this:
  * A **Google Sheet** with at least two columns: `topic` and `generated commentary`.
  * A **Dumpling AI API Key** with access to the `/search-news` and `/scrape` endpoints.
  * An **OpenAI GPT-4o connection**.


### [Qualify TikTok influencers from username with Dumpling AI + GPT-4
  * Google Sheets
  * HTTP Request
  * Switch

](https://n8n.io/workflows/9126-qualify-tiktok-influencers-from-username-with-dumpling-ai-gpt-4/)### [Generate email newsletters from Telegram keywords with Dumpling AI and GPT
  * HTTP Request
  * Loop Over Items (Split in Batches)
  * Telegram Trigger
  * +10

](https://n8n.io/workflows/8187-generate-email-newsletters-from-telegram-keywords-with-dumpling-ai-and-gpt/)### [Telegram bot: extract & store TikTok and LinkedIn data to Google Sheets with Dumpling AI
  * Edit Fields (Set)
  * Telegram

](https://n8n.io/workflows/11546-telegram-bot-extract-and-store-tiktok-and-linkedin-data-to-google-sheets-with-dumpling-ai/)
### [Generate AI viral videos with Seedance and upload to TikTok, YouTube & Instagram
  * Google Sheets
  * HTTP Request
  * Merge

](https://n8n.io/workflows/5338-generate-ai-viral-videos-with-seedance-and-upload-to-tiktok-youtube-and-instagram/)### [Generate AI videos with Google Veo3, save to Google Drive and upload to YouTube
  * Google Sheets
  * HTTP Request

](https://n8n.io/workflows/4846-generate-ai-videos-with-google-veo3-save-to-google-drive-and-upload-to-youtube/)### [Generate & auto-post AI videos to social media with Veo3 and Blotato
  * Google Sheets
  * HTTP Request
  * Edit Fields (Set)

](https://n8n.io/workflows/5035-generate-and-auto-post-ai-videos-to-social-media-with-veo3-and-blotato/)
### [✨🤖Automate Multi-Platform Social Media Content Creation with AI
  * HTTP Request
  * Merge
  * +17

](https://n8n.io/workflows/3066-automate-multi-platform-social-media-content-creation-with-ai/)### [Fully automated AI video generation & multi-platform publishing
  * Google Sheets
  * HTTP Request
  * +11

](https://n8n.io/workflows/3442-fully-automated-ai-video-generation-and-multi-platform-publishing/)### [Generate AI viral videos with VEO 3 and upload to TikTok
  * Google Sheets
  * HTTP Request
  * Edit Fields (Set)

](https://n8n.io/workflows/8642-generate-ai-viral-videos-with-veo-3-and-upload-to-tiktok/)
This website uses cookies 
We use cookies to personalise content, ads and to analyse our traffic. We also share information about your use of our site with our advertising and analytics partners who may combine it with other information that you’ve provided to them or that they’ve collected from your use of their services.  [ Read more ](https://n8n.io/legal/?eco_features=CAMPAIGN_PERSONALIZATION#privacy)
Strictly necessary 
Performance 
Targeting 
Functionality 
Save & Close 
Accept all 
Decline all 
Show details  Hide details 
Cookie declaration 
About cookies 
Strictly necessary 
Performance 
Targeting 
Functionality 
Strictly necessary cookies allow core website functionality such as user login and account management. The website cannot be used properly without strictly necessary cookies. 
Cookie report Name  |  Provider / Domain |  Expiration  |  Description   
---|---|---|---  
__cf_logged_in |  .cloudflare.com  |  4 weeks 2 days  |  Part of our security firewall Cloudflare (e.g. identifying trusted users)   
AMCVS_XXXXX |  .cloudflare.com  |  Session  |  Adobe Experience Cloud cookie that serves as a flag indicating that the session has been initialized. Its value is always 1 and discontinues when the session has ended.   
CF_VERIFIED_DEVICE_XXXXX |  .cloudflare.com  |  1 year  |  Cloudflare   
sparrow_id |  .cloudflare.com  |  5 months 4 weeks  |  This cookie is used by Cloudflare to help optimise the performance and security of the website and access to it. They do not contain user credentials, IP anonymisation is used.   
rl_session |  .n8n.io  |  1 year  |  This cookie is used for managing user session on the website. It typically maintains the user's state during the session, ensuring that users remain connected and their interactions with the site are coherent throughout their visit. This can include keeping users logged in, tracking their actions, or persisting settings during the session.   
__sec_tid |  n8n.io  |  9 months 4 weeks   
__sec__token |  n8n.io  |  1 day   
_shopify_essential |  merch.n8n.io  |  1 year  |  This cookie is essential for the secure checkout and payment function on the website and is provided by Shopify.   
__Host-airtable-session.sig |  airtable.com  |  1 year  |  This cookie is used to ensure secure user sessions and for authentication purposes.   
keep_alive |  merch.n8n.io  |  Session  |  This cookie is used to maintain an active user session on the website and ensure that the user's connection remains secure and uninterrupted during their browsing session.   
__sec__fid |  n8n.io  |  9 months 4 weeks   
brwConsent |  .airtable.com  |  5 minutes  |  This cookie is used to record the user's consent to the use of cookies on the website, ensuring compliance with the website's privacy policy by remembering the user's preferences and consent state regarding cookies.   
AWSALBTGCORS |  airtable.com  |  1 week  |  This cookie is used to support load balancing, ensuring that visitor page requests are routed to the same server in any browsing session.   
__sec_crid |  n8n.io  |  9 months 4 weeks   
CookieScriptConsent |  .n8n.io  |  1 year  |  This cookie is used by Cookie-Script.com service to remember visitor cookie consent preferences. It is necessary for Cookie-Script.com cookie banner to work properly.   
__sec__ghost |  n8n.io  |  9 months 4 weeks   
localization |  merch.n8n.io  |  1 year  |  These cookies are set on pages with the Flickr widget.   
__Host-airtable-session |  airtable.com  |  1 year  |  This cookie is used to manage the user session in a secure way, ensuring the user's interaction with the website is seamless and secure while accessing Airtable integrations or content.   
__cf_bm |  .paddle.com  |  29 minutes 57 seconds  |  This cookie is used to distinguish between humans and bots. This is beneficial for the website, in order to make valid reports on the use of their website.   
__sec__cid |  n8n.io  |  1 day   
Performance cookies are used to see how visitors use the website, eg. analytics cookies. Those cookies cannot be used to directly identify a certain visitor. 
Cookie report Name  |  Provider / Domain |  Expiration  |  Description   
---|---|---|---  
ph_phc_XXXXX_posthog |  .tapfiliate.com  |  1 year  |  Posthog   
AMCV_XXXXX |  .cloudflare.com  |  4 weeks 2 days  |  Adobe Experience Cloud cookie that enables tracking visitors across multiple domains.   
cfz_google-analytics_v4 |  .cloudflare.com  |  1 year  |  Cloudflare Zaraz Google Analytics cookie   
cfzs_google-analytics_v4 |  .cloudflare.com  |  Session  |  Cloudflare Zaraz Google Analytics session cookie   
rl_user_id |  .n8n.io  |  1 year  |  This cookie is used to recognize and distinguish individual users who visit the website, enabling personalized experiences and interactions.   
_ga_Q7GL51X95F |  .n8n.io  |  1 year 1 month  |  This cookie is used by Google Analytics to persist session state.   
brw |  .airtable.com  |  1 year  |  This cookie is used to track user behavior and interaction to improve user experience and service functionality.   
rl_page_init_referrer |  .n8n.io  |  1 year   
rl_page_init_referring_domain |  .n8n.io  |  1 year   
originalClientId |  .n8n.io  |  4 weeks 2 days   
rl_anonymous_id |  .n8n.io  |  1 year  |  This cookie is used to identify anonymously a visitor. It is generally used for tracking and analytics purposes, helping website owners understand how visitors interact with the site.   
n8n_tracking_id |  .n8n.io  |  1 year 1 month   
_ga_1EB8LCPG5B |  .n8n.io  |  1 year 1 month  |  This cookie is used by Google Analytics to persist session state.   
_gat_gtag_UA_146470481_1 |  .n8n.io  |  1 minute  |  This cookie is part of Google Analytics and is used to limit requests (throttle request rate).   
rl_group_id |  .n8n.io  |  1 year  |  This cookie is used to group users for analytical purposes to enhance user experience on the website.   
_gat_gtag_UA_146470481_8 |  .n8n.io  |  51 seconds  |  This cookie is part of Google Analytics and is used to limit requests (throttle request rate).   
_shopify_y |  .n8n.io  |  1 year 6 hours  |  This cookie is associated with Shopify's analytics suite.  Provider address:  151 O'Connor Street, Ground floor, Ottawa, ON, K2P 2L8, Canada   
_ga |  .n8n.io  |  1 year 1 month  |  This cookie name is associated with Google Universal Analytics - which is a significant update to Google's more commonly used analytics service. This cookie is used to distinguish unique users by assigning a randomly generated number as a client identifier. It is included in each page request in a site and used to calculate visitor, session and campaign data for the sites analytics reports.   
_gid |  .n8n.io  |  1 day  |  This cookie is set by Google Analytics. It stores and update a unique value for each page visited and is used to count and track pageviews.   
_ga_0SC4FF2FH9 |  .n8n.io  |  1 year 1 month  |  This cookie is used by Google Analytics to persist session state.   
_shopify_analytics |  merch.n8n.io  |  1 year   
_shopify_s |  .n8n.io  |  30 minutes  |  This cookie is associated with Shopify's analytics suite.   
Targeting cookies are used to identify visitors between different websites, eg. content partners, banner networks. Those cookies may be used by companies to build a profile of visitor interests or show relevant ads on other websites. 
Cookie report Name  |  Provider / Domain |  Expiration  |  Description   
---|---|---|---  
lang |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  Session  |  linkedin.com targeting   
li_sugr |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  3 months  |  linkedin.com targeting   
UserMatchHistory |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  4 weeks 2 days  |  linkedin.com targeting   
AnalyticsSyncHistory |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  4 weeks 2 days  |  linkedin.com targeting   
datr |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  1 year 1 month  |  This cookie identifies the browser connecting to Facebook. It is not directly tied to individual Facebook the user. Facebook reports that it is used to help with security and suspicious login activity, especially around detection of bots trying to access the service. Facebook also say the behavioural profile associated with each datr cookie is deleted after 10 days. This cookie is also read via Like and other Facebook buttons and tags placed on many different websites.   
sb |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  1 year 1 month  |  Facebook browser identification, authentication, marketing, and other Facebook-specific function cookies.   
wd |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  1 week  |  This cookie carries out information about how the end user uses the website and any advertising that the end user may have seen before visiting the said website.   
rdt_uuid |  .n8n.io  |  3 months  |  Identify users who've seen n8n ads on Reddit so that we can run our ads more efficiently.   
csv |  .reddit.com  |  1 year 1 month  |  This cookie is typically used for tracking user behavior and interaction with the website to improve user experience.   
edgebucket |  .reddit.com  |  1 year 1 month  |  Used by Reddit to deliver advertising   
loid |  .reddit.com  |  1 year 1 month  |  This cookie is used to identify a unique visitor's session and preferences.   
pc |  .reddit.com  |  1 year   
reddit_session |  .reddit.com  |  Session   
session_tracker |  .reddit.com  |  Session  |  This cookie is used to track user sessions for improving user experience and ensuring secure browsing sessions. It helps in maintaining an active session for the user without needing to log in multiple times during their visit.   
t2_XXXXX_recentclicks3 |  .reddit.com  |  1 year   
theme |  .reddit.com  |  1 year  |  This cookie is used to store the user's theme preference on the website, allowing for a consistent and personalized visual experience across different pages.   
token_v2 |  .reddit.com  |  1 day   
ps_l |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  1 year 1 month  |  This cookie is associated with user preferences and saving settings to enhance the user experience on the website.   
ps_n |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  1 year 1 month  |  This cookie is used to remember the user's preferences and previous interactions with the website.   
fr |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .facebook.com  |  3 months  |  Contains browser and user unique ID combination, used for targeted advertising.   
csrf_token |  .reddit.com  |  Session  |  This cookie is used by Cloudflare to identify trusted web traffic.   
cfz_facebook-pixel |  [Meta Platform Inc.](https://www.facebook.com/policy.php) .cloudflare.com  |  1 year  |  Cloudflare Zaraz facebook pixel cookie   
rl_trait |  .n8n.io  |  1 year  |  This cookie is used to collect information about user behavior and preferences to optimize the user experience and for targeted advertising.   
__Secure-ROLLOUT_TOKEN |  .youtube.com  |  5 months 4 weeks   
_gcl_au |  .n8n.io  |  3 months  |  Used by Google AdSense for experimenting with advertisement efficiency across websites using their services   
rl_group_trait |  .n8n.io  |  1 year  |  This cookie is used for segmenting audiences based on predefined criteria, aiming to provide more personalized and relevant content to the website users.   
lidc |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  1 day  |  This is a Microsoft MSN 1st party cookie that ensures the proper functioning of this website.   
bcookie |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  1 year  |  This is a Microsoft MSN 1st party cookie for sharing the content of the website via social media.   
IDE |  .doubleclick.net  |  1 year  |  Google Ads targeting   
VISITOR_PRIVACY_METADATA |  .youtube.com  |  5 months 4 weeks  |  This cookie is used to store the user's consent and privacy choices for their interaction with the site. It records data on the visitor's consent regarding various privacy policies and settings, ensuring that their preferences are honored in future sessions.   
li_gc |  [LinkedIn Corporation](https://www.linkedin.com/legal/privacy-policy) .linkedin.com  |  5 months 4 weeks  |  Used to store guest consent to the use of cookies for non-essential purposes   
__Secure-YNID |  .youtube.com  |  5 months 4 weeks   
YSC |  .youtube.com  |  Session  |  This cookie is set by YouTube to track views of embedded videos.   
VISITOR_INFO1_LIVE |  .youtube.com  |  5 months 4 weeks  |  This cookie is set by Youtube to keep track of user preferences for Youtube videos embedded in sites;it can also determine whether the website visitor is using the new or old version of the Youtube interface.   
test_cookie |  .doubleclick.net  |  15 minutes  |  This cookie is set by DoubleClick (which is owned by Google) to determine if the website visitor's browser supports cookies.   
Functionality cookies are used to remember visitor information on the website, eg. language, timezone, enhanced content. 
Cookie report Name  |  Provider / Domain |  Expiration  |  Description   
---|---|---|---  
intercom-device-id-XXXXX |  .hockeystack.com  |  5 months 4 weeks   
intercom-id-XXXXX |  .hockeystack.com  |  5 months 4 weeks   
intercom-session-XXXXX |  .hockeystack.com  |  1 week   
paddle_session |  .paddle.com  |  1 day   
Cookies are small text files that are placed on your computer by websites that you visit. Websites use cookies to help users navigate efficiently and perform certain functions. Cookies that are required for the website to operate properly are allowed to be set without your permission. All other cookies need to be approved before they can be set in the browser. You can change your consent to cookie usage at any time on our Privacy Policy page. 
We also use cookies to collect data for the purpose of personalizing and measuring the effectiveness of our advertising. For more details, visit the [Google Privacy Policy](https://business.safety.google/privacy/). 
Cookies consent ID : 
Cookie [report](https://cookie-script.com/cookie-report?identifier=ed53b7b2bda0a83153e40b6660e65372) created by [CookieScript](https://cookie-script.com "CookieScript Consent Management Platform")
