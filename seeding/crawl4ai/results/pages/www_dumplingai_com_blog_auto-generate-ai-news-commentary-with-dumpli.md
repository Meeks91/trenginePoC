June 27, 2025
# Auto-Generate AI News Commentary with Dumpling AI and GPT-4o
## **Introduction**
Writing consistent and insightful commentary on AI news is crucial for anyone trying to stand out on platforms like LinkedIn. But the effort it takes to find relevant articles, analyze the content, and write meaningful posts can be overwhelming and time-consuming. This is where automation becomes powerful.
This automation workflow is designed to help you generate thought-provoking, human-like commentary from live news sources—automatically. It uses a combination of Dumpling AI and GPT-4o to search news based on your input topics, extract the full content, and generate commentary that you can post right away.
Whether you’re a startup founder, a marketing strategist, or just someone trying to grow a personal brand in AI, this will help you save time while staying visible and valuable.
## **Step-by-Step Breakdown**
### **⏰ 1. Schedule Trigger**
  * **Node Type:** Schedule Trigger
  * **Purpose:** This is the starting point of the workflow. It runs daily at your set time to check for new AI topics and generate commentary.
  * **Why It Matters:** Ensures your system stays active daily without any manual trigger, keeping your commentary stream consistent.


### **2. Fetch Topics from Google Sheets**
  * **Node Type:** Google Sheets
  * **Function:** Pulls rows from your sheet where the topic is defined, but the commentary cell is still empty.
  * **How it Works:** The workflow looks at the Topic column and checks if the Generated Commentary column is blank.
  * **Why It Matters:** Prevents the workflow from repeating tasks or duplicating existing content.


### **3. Loop Through Topics**
  * **Node Type:** SplitInBatches
  * **Function:** Breaks the pulled topics into individual items and processes them one by one.
  * **Why It Matters:** This step allows sequential processing for each topic, which is essential when dealing with API limits and article scraping.


### **4. Wait Node**
  * **Node Type:** Wait
  * **Function:** Adds a 1-second delay before hitting Dumpling AI’s API.
  * **Why It Matters:** Helps to manage rate limits when processing many topics at once.


### **5. Search News via Dumpling AI**
  * **Node Type:** HTTP Request
  * **Function:** Calls the /search-news endpoint from Dumpling AI to fetch the most recent news related to the topic.
  * **Example Payload:**


{
“query”: “{{ $json.Topic }}”,
“country”: “US”,
“page”: 3,
“language”: “en”
}
  * **Output:** Returns an array of news articles with metadata (titles, descriptions, links).


### **6. Split Articles**
  * **Node Type:** Split Out
  * **Function:** Breaks the returned array of articles into individual entries.
  * **Why It Matters:** Prepares each article URL for content scraping by Dumpling AI.


### **7. Scrape Article Content**
  * **Node Type:** HTTP Request
  * **Function:** Sends the article URL to Dumpling AI’s /scrape endpoint to fetch the full HTML content and convert it to plain text.
  * **Why It Matters:** We need the full body of the article (not just the preview) for GPT-4o to generate thoughtful commentary.


### **8. Aggregate Article Content**
  * **Node Type:** Aggregate
  * **Function:** Combines the cleaned-up content of all scraped articles into one large body of text.
  * **Why It Matters:** Having multiple perspectives or headlines around the same topic gives GPT-4o more material to work with, improving commentary quality.


### **9. Clean Text Content**
  * **Node Type:** Code
  * **Function:** Runs a JavaScript function to remove leftover formatting like HTML tags, links, or broken lines.
  * **Why It Matters:** Ensures that the prompt sent to GPT-4o is clean and free from distractions, which helps the AI generate better output.


### **10. Generate Commentary with GPT-4o**
  * **Node Type:** OpenAI Chat Model
  * **Prompt Design:**


You are a LinkedIn thought leader writing a short, engaging commentary on the following topic. Keep the tone human and confident. The commentary should be insightful, based on the article content, and no longer than 3 paragraphs. Conclude with a relevant question or bold statement to invite discussion.
Topic: {{ $json.Topic }}
Content:
{{ cleanedArticleContent }}
  * **What It Does:** Uses GPT-4o to create first-person, expert-sounding commentary based on aggregated insights.


### **11. Save to Google Sheets**
  * **Node Type:** Google Sheets
  * **Function:** Writes the original topic and generated commentary back to the Google Sheet in the correct row.
  * **Why It Matters:** You now have content you can immediately review and post.


## **Conclusion**
This workflow automates more than just writing. It gives you back your time while still maintaining your presence as a voice of authority in AI. From scraping trending articles to turning them into insightful posts, each part of the process is streamlined and optimized for engagement.
If you’re looking to build thought leadership on LinkedIn, this workflow is your silent writing assistant, fast, consistent, and always relevant.
You can enhance it further by connecting it to tools like Buffer or Hootsuite for auto-posting, Slack for team review, or Airtable for content tagging.
**Download the blueprint used in this blog post**
Click [here](https://substack.com/redirect/66a38b71-96c1-4a71-9e95-f7fe385571c4?j=eyJ1IjoiMnB1NG5hIn0.YoVEPUme7qisXqbsxKduWZD1Wn1DgcAyGyVt8xdWOas) to access the blueprint.
Keep Learning
## Related articles
### [Qualify TikTok Influencers from Username using Dumpling AI and GPT-4](https://www.dumplingai.com/blog/qualify-tiktok-influencers-from-username-using-dumpling-ai-and-gpt-4)### [n8n SEO Automation Workflow Using Dumpling AI](https://www.dumplingai.com/blog/n8n-seo-automation-workflow-using-dumpling-ai)### [Find TikTok Video Questions from Keywords Using Dumpling AI and GPT-4](https://www.dumplingai.com/blog/find-tiktok-video-questions-from-keywords-using-dumpling-ai-and-gpt-4)### [How to Translate Make Scenarios into n8n Workflows](https://www.dumplingai.com/blog/how-to-translate-make-scenarios-into-n8n-workflows)### [Turn TikTok Comments into AI Avatar Videos with Dumpling AI, GPT-4 & Captions.ai](https://www.dumplingai.com/blog/turn-tiktok-comments-into-ai-avatar-videos-with-dumpling-ai-gpt-4-captions-ai)### [Automate Blog Post Creation from a Single Keyword with Dumpling AI](https://www.dumplingai.com/blog/automate-blog-post-creation-from-a-single-keyword-with-dumpling-ai)
