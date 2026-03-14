Finding the right TikTok creators for brand deals is a nightmare.
Most agencies charge $500-5,000 just to compile a list of influencers. They use the same databases everyone else uses. They send you a spreadsheet and call it a day.
In this tutorial, we'll build a **TikTok Creator Analyzer** that:
  1. Pulls any creator's profile and video stats
  2. Calculates real engagement rates (not vanity metrics)
  3. Analyzes their content style and audience demographics


Stop overpaying for influencer lists. Build your own research tool.
##  Why TikTok Creator Data Matters 
TikTok's algorithm is chaotic. A creator with 100K followers can outperform one with 1M.
What matters:
  * **Engagement rate** (not follower count)
  * **View-to-follower ratio** (are their videos actually being shown?)
  * **Audience demographics** (are they reaching YOUR customers?)
  * **Content consistency** (one viral video vs. consistent performer)


You can't get this from their profile page. You need data.
##  The Stack 
  * **Node.js** : Runtime
  * **SociaVault API** : To fetch TikTok data
  * **OpenAI API** : For content analysis


##  Step 1: Setup 
```
mkdir tiktok-creator-analyzer
cd tiktok-creator-analyzer
npm init -y
npm install axios dotenv openai

```

Enter fullscreen mode Exit fullscreen mode
Create `.env`: 
```
SOCIAVAULT_API_KEY=your_sociavault_key
OPENAI_API_KEY=your_openai_key

```

Enter fullscreen mode Exit fullscreen mode
##  Step 2: Fetch Creator Profile 
Let's start by getting a creator's basic info.
Create `index.js`: 
```
require('dotenv').config();
const axios = require('axios');
const OpenAI = require('openai');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const SOCIAVAULT_BASE = 'https://api.sociavault.com';

async function getCreatorProfile(username) {
  console.log(`📥 Fetching profile for @${username}...`);

  try {
    const response = await axios.get(`${SOCIAVAULT_BASE}/v1/scrape/tiktok/profile`, {
      params: { username },
      headers: { 'Authorization': `Bearer ${process.env.SOCIAVAULT_API_KEY}` }
    });

    const profile = response.data.data;

    return {
      username: profile.uniqueId || profile.username,
      nickname: profile.nickname || profile.displayName,
      bio: profile.signature || profile.bio,
      followers: profile.followerCount || profile.followers,
      following: profile.followingCount || profile.following,
      likes: profile.heartCount || profile.likes,
      videos: profile.videoCount || profile.videos,
      verified: profile.verified || false,
      avatar: profile.avatarLarger || profile.avatar
    };
  } catch (error) {
    console.error('Error fetching profile:', error.message);
    return null;
  }
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 3: Get Creator's Videos 
Now let's fetch their recent videos for deeper analysis: 
```
async function getCreatorVideos(username, limit = 30) {
  console.log(`📥 Fetching videos from @${username}...`);

  try {
    const response = await axios.get(`${SOCIAVAULT_BASE}/v1/scrape/tiktok/videos`, {
      params: { username, limit },
      headers: { 'Authorization': `Bearer ${process.env.SOCIAVAULT_API_KEY}` }
    });

    const videos = response.data.data || [];

    return videos.map(v => ({
      id: v.id,
      description: v.desc || v.description,
      views: v.playCount || v.views,
      likes: v.diggCount || v.likes,
      comments: v.commentCount || v.comments,
      shares: v.shareCount || v.shares,
      created: v.createTime || v.created,
      duration: v.duration,
      music: v.music?.title || v.musicTitle
    }));
  } catch (error) {
    console.error('Error fetching videos:', error.message);
    return [];
  }
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 4: Get Video Details 
For deep-diving into specific viral videos: 
```
async function getVideoInfo(videoUrl) {
  console.log('📥 Fetching video details...');

  try {
    const response = await axios.get(`${SOCIAVAULT_BASE}/v1/scrape/tiktok/video-info`, {
      params: { url: videoUrl },
      headers: { 'Authorization': `Bearer ${process.env.SOCIAVAULT_API_KEY}` }
    });

    return response.data.data;
  } catch (error) {
    console.error('Error fetching video info:', error.message);
    return null;
  }
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 5: Get Audience Demographics 
This is the gold—understand WHO is watching: 
```
async function getCreatorDemographics(username) {
  console.log(`📥 Fetching demographics for @${username}...`);

  try {
    const response = await axios.get(`${SOCIAVAULT_BASE}/v1/scrape/tiktok/demographics`, {
      params: { username },
      headers: { 'Authorization': `Bearer ${process.env.SOCIAVAULT_API_KEY}` }
    });

    return response.data.data;
  } catch (error) {
    console.error('Error fetching demographics:', error.message);
    return null;
  }
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 6: Calculate Real Engagement Metrics 
Vanity metrics lie. Let's calculate what actually matters: 
```
function calculateMetrics(profile, videos) {
  if (!videos || videos.length === 0) return null;

  // Total engagement across videos
  const totalViews = videos.reduce((sum, v) => sum + (v.views || 0), 0);
  const totalLikes = videos.reduce((sum, v) => sum + (v.likes || 0), 0);
  const totalComments = videos.reduce((sum, v) => sum + (v.comments || 0), 0);
  const totalShares = videos.reduce((sum, v) => sum + (v.shares || 0), 0);

  // Averages
  const avgViews = totalViews / videos.length;
  const avgLikes = totalLikes / videos.length;
  const avgComments = totalComments / videos.length;
  const avgShares = totalShares / videos.length;

  // Engagement rate (likes + comments + shares) / views
  const avgEngagement = ((avgLikes + avgComments + avgShares) / avgViews * 100);

  // View-to-follower ratio (how well does content reach their audience?)
  const viewToFollowerRatio = (avgViews / profile.followers * 100);

  // Consistency (standard deviation of views)
  const viewVariance = videos.reduce((sum, v) => 
    sum + Math.pow((v.views || 0) - avgViews, 2), 0
  ) / videos.length;
  const viewStdDev = Math.sqrt(viewVariance);
  const consistencyScore = 100 - (viewStdDev / avgViews * 100);

  // Find outliers (viral videos)
  const viralThreshold = avgViews * 3;
  const viralVideos = videos.filter(v => v.views  viralThreshold);

  // Top performing content
  const sortedByViews = [...videos].sort((a, b) => b.views - a.views);
  const topVideos = sortedByViews.slice(0, 5);
  const worstVideos = sortedByViews.slice(-3);

  return {
    summary: {
      totalViews,
      avgViews: Math.round(avgViews),
      avgLikes: Math.round(avgLikes),
      avgComments: Math.round(avgComments),
      avgShares: Math.round(avgShares)
    },
    rates: {
      engagementRate: avgEngagement.toFixed(2) + '%',
      viewToFollowerRatio: viewToFollowerRatio.toFixed(2) + '%',
      consistencyScore: Math.max(0, consistencyScore).toFixed(0) + '/100'
    },
    outliers: {
      viralCount: viralVideos.length,
      viralPercentage: ((viralVideos.length / videos.length) * 100).toFixed(1) + '%'
    },
    topVideos,
    worstVideos
  };
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 7: AI Content Analysis 
Understand their content style and audience fit: 
```
async function analyzeContentStyle(videos, profile) {
  console.log('🤖 Analyzing content style...');

  const prompt = `
    Analyze this TikTok creator's content style based on their recent videos.

    Creator: @${profile.username}
    Bio: ${profile.bio}
    Followers: ${profile.followers}

    Return JSON with:
    {
      "contentStyle": {
        "primaryNiche": "main content category",
        "secondaryNiches": ["other topics they cover"],
        "tone": "funny/educational/inspiring/etc",
        "format": "talking head/skits/tutorials/etc"
      },
      "brandFit": {
        "idealBrands": ["types of brands that would fit well"],
        "avoidBrands": ["types of brands that wouldn't fit"],
        "integrationStyle": "how they typically do sponsored content"
      },
      "audienceProfile": {
        "estimatedAge": "likely age range of audience",
        "interests": ["audience interests"],
        "buyingPower": "low/medium/high"
      },
      "strengthsForBrands": [3 reasons brands should work with them],
      "risksForBrands": [3 potential concerns],
      "recommendedDealTypes": ["product seeding", "paid post", "ambassador", etc]
    }

    Videos:
    ${JSON.stringify(videos.slice(0, 20).map(v => ({
      description: v.description,
      views: v.views,
      likes: v.likes,
      music: v.music
    })))};

  const completion = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [{ role: 'user', content: prompt }],
    response_format: { type: 'json_object' }
  });

  return JSON.parse(completion.choices[0].message.content);
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 8: The Full Creator Report 
```
async function analyzeCreator(username) {
  console.log('\n📊 TikTok Creator Analysis\n');
  console.log('═══════════════════════════════════════\n');

  // 1. Get profile
  const profile = await getCreatorProfile(username);
  if (!profile) {
    console.log('Could not fetch profile.');
    return;
  }

  console.log(`👤 @${profile.username}${profile.verified ? '✓' : ''}`);
  console.log(${profile.nickname}`);
  console.log(`   "${profile.bio?.substring(0, 60) || 'No bio'}..."`);
  console.log(`\n   📊 ${Number(profile.followers).toLocaleString()} followers`);
  console.log(`   ❤️ ${Number(profile.likes).toLocaleString()} total likes`);
  console.log(`   🎬 ${profile.videos} videos`);

  // 2. Get videos
  const videos = await getCreatorVideos(username);
  if (videos.length === 0) {
    console.log('\nNo videos found.');
    return;
  }

  console.log(`\n✅ Analyzed ${videos.length} recent videos\n`);

  // 3. Calculate metrics
  const metrics = calculateMetrics(profile, videos);

  console.log('═══════════════════════════════════════');
  console.log('📈 PERFORMANCE METRICS');
  console.log('═══════════════════════════════════════\n');

  console.log('📊 Averages per Video:');
  console.log(`   👁️ ${metrics.summary.avgViews.toLocaleString()} views`);
  console.log(`   ❤️ ${metrics.summary.avgLikes.toLocaleString()} likes`);
  console.log(`   💬 ${metrics.summary.avgComments.toLocaleString()} comments`);
  console.log(`   🔄 ${metrics.summary.avgShares.toLocaleString()} shares`);

  console.log('\n⚡ Key Rates:');
  console.log(`   Engagement Rate: ${metrics.rates.engagementRate}`);
  console.log(`   View/Follower Ratio: ${metrics.rates.viewToFollowerRatio}`);
  console.log(`   Consistency Score: ${metrics.rates.consistencyScore}`);

  console.log('\n🚀 Viral Performance:');
  console.log(`   Viral videos: ${metrics.outliers.viralCount} (${metrics.outliers.viralPercentage} of content)`);

  // 4. Top/worst videos
  console.log('\n🏆 Top Performing Videos:');
  metrics.topVideos.slice(0, 3).forEach((v, i) => {
    console.log(${i + 1}. ${v.views.toLocaleString()} views - "${v.description?.substring(0, 40) || 'No caption'}..."`);
  });

  // 5. AI Analysis
  const contentAnalysis = await analyzeContentStyle(videos, profile);

  console.log('\n═══════════════════════════════════════');
  console.log('🎯 BRAND FIT ANALYSIS');
  console.log('═══════════════════════════════════════\n');

  console.log(`📌 Primary Niche: ${contentAnalysis.contentStyle.primaryNiche}`);
  console.log(`🎨 Content Style: ${contentAnalysis.contentStyle.tone}${contentAnalysis.contentStyle.format}`);

  console.log('\n✅ Ideal Brand Partners:');
  contentAnalysis.brandFit.idealBrands.forEach(b => console.log(`   • ${b}`));

  console.log('\n❌ Brands to Avoid:');
  contentAnalysis.brandFit.avoidBrands.forEach(b => console.log(`   • ${b}`));

  console.log('\n👥 Estimated Audience:');
  console.log(`   Age: ${contentAnalysis.audienceProfile.estimatedAge}`);
  console.log(`   Interests: ${contentAnalysis.audienceProfile.interests.join(', ')}`);
  console.log(`   Buying Power: ${contentAnalysis.audienceProfile.buyingPower}`);

  console.log('\n💪 Strengths for Brands:');
  contentAnalysis.strengthsForBrands.forEach((s, i) => console.log(${i + 1}. ${s}`));

  console.log('\n⚠️ Potential Risks:');
  contentAnalysis.risksForBrands.forEach((r, i) => console.log(${i + 1}. ${r}`));

  console.log('\n💰 Recommended Deal Types:');
  contentAnalysis.recommendedDealTypes.forEach(d => console.log(`   • ${d}`));

  // 6. Demographics (if available)
  const demographics = await getCreatorDemographics(username);
  if (demographics) {
    console.log('\n═══════════════════════════════════════');
    console.log('👥 AUDIENCE DEMOGRAPHICS');
    console.log('═══════════════════════════════════════\n');
    console.log(JSON.stringify(demographics, null, 2));
  }

  return { profile, videos, metrics, contentAnalysis, demographics };
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 9: Compare Multiple Creators 
When evaluating multiple options: 
```
async function compareCreators(usernames) {
  console.log('\n🏆 CREATOR COMPARISON\n');
  console.log('═══════════════════════════════════════\n');

  const results = [];

  for (const username of usernames) {
    const profile = await getCreatorProfile(username);
    const videos = await getCreatorVideos(username);

    if (profile  videos.length  0) {
      const metrics = calculateMetrics(profile, videos);
      results.push({ username, profile, metrics });
    }

    await new Promise(r => setTimeout(r, 500));
  }

  // Sort by engagement rate
  results.sort((a, b) => 
    parseFloat(b.metrics.rates.engagementRate) - parseFloat(a.metrics.rates.engagementRate)
  );

  console.log('Ranked by Engagement Rate:\n');

  results.forEach((r, i) => {
    console.log(`${i + 1}. @${r.username}`);
    console.log(`   Followers: ${r.profile.followers.toLocaleString()}`);
    console.log(`   Avg Views: ${r.metrics.summary.avgViews.toLocaleString()}`);
    console.log(`   Engagement: ${r.metrics.rates.engagementRate}`);
    console.log(`   View/Follower: ${r.metrics.rates.viewToFollowerRatio}`);
    console.log(`   Consistency: ${r.metrics.rates.consistencyScore}\n`);
  });

  return results;
}

```

Enter fullscreen mode Exit fullscreen mode
##  Step 10: Run It 
```
async function main() {
  // Analyze a single creator
  await analyzeCreator('khaby.lame');

  // Or compare multiple
  // await compareCreators(['creator1', 'creator2', 'creator3']);
}

main();

```

Enter fullscreen mode Exit fullscreen mode
##  Sample Output 
```
📊 TikTok Creator Analysis
═══════════════════════════════════════

👤 @khaby.lame ✓
   Khabane lame
   "If u want to laugh u are in the right place..."

   📊 162,400,000 followers
   ❤️ 2,400,000,000 total likes
   🎬 1,247 videos

✅ Analyzed 30 recent videos

═══════════════════════════════════════
📈 PERFORMANCE METRICS
═══════════════════════════════════════

📊 Averages per Video:
   👁️ 45,234,000 views
   ❤️ 3,245,000 likes
   💬 24,500 comments
   🔄 89,000 shares

⚡ Key Rates:
   Engagement Rate: 7.42%
   View/Follower Ratio: 27.85%
   Consistency Score: 72/100

🚀 Viral Performance:
   Viral videos: 4 (13.3% of content)

═══════════════════════════════════════
🎯 BRAND FIT ANALYSIS
═══════════════════════════════════════

📌 Primary Niche: Comedy/Entertainment
🎨 Content Style: funny reaction skits

✅ Ideal Brand Partners:
   • Consumer tech and apps
   • Lifestyle and fashion brands
   • Gaming companies
   • Food and beverage

❌ Brands to Avoid:
   • B2B software
   • Luxury goods (audience skews younger)
   • Controversial products

👥 Estimated Audience:
   Age: 13-24
   Interests: comedy, memes, social media trends
   Buying Power: medium

💪 Strengths for Brands:
   1. Massive global reach across demographics
   2. Universal humor works in any language
   3. Highly shareable content format

⚠️ Potential Risks:
   1. Very broad audience (less targeted)
   2. Premium pricing due to scale
   3. May overshadow brand message

💰 Recommended Deal Types:
   • Ambassador programs
   • Product integration in skits
   • Multi-platform campaigns

```

Enter fullscreen mode Exit fullscreen mode
##  Why This Matters 
Influencer marketing platforms charge:
  * **Grin** : $25,000+/year
  * **CreatorIQ** : Custom pricing (expensive)
  * **Upfluence** : $2,000+/month


You just built the core research functionality for the cost of API calls.
##  Get Started 
  1. Get your [SociaVault API Key](https://sociavault.com)
  2. Make a list of creators in your niche
  3. Run the analyzer
  4. Stop overpaying agencies for spreadsheets


Build your own creator database. Own your influencer research.
[ MongoDB ](https://dev.to/mongodb) Promoted
Dropdown menu
##  [Build gen AI apps that run anywhere with MongoDB Atlas](https://www.mongodb.com/cloud/atlas/lp/try3?utm_campaign=display_devto-broad_pl_flighted_atlas_tryatlaslp_prosp_gic-null_ww-all_dev_dv-all_eng_leadgen&utm_source=devto&utm_medium=display&utm_content=aipowered-v1&bb=241239)
MongoDB Atlas bundles vector search and a flexible document model so developers can build, scale, and run gen AI apps without juggling multiple databases. From LLM to semantic search, Atlas streamlines AI architecture. Start free today.
Read More 
For further actions, you may consider blocking this person and/or [reporting abuse](https://dev.to/report-abuse)
[ MongoDB ](https://dev.to/mongodb) Promoted
Dropdown menu
##  [Build gen AI apps that run anywhere with MongoDB Atlas](https://www.mongodb.com/cloud/atlas/lp/try3?utm_campaign=display_devto-broad_pl_flighted_atlas_tryatlaslp_prosp_gic-null_ww-all_dev_dv-all_eng_leadgen&utm_source=devto&utm_medium=display&utm_content=aipowered-v1&bb=241238)
MongoDB Atlas bundles vector search and a flexible document model so developers can build, scale, and run gen AI apps without juggling multiple databases. From LLM to semantic search, Atlas streamlines AI architecture. Start free today.
👋 Kindness is contagious
Dropdown menu
Dive into this thoughtful piece, beloved in the supportive DEV Community. **Coders of every background** are invited to share and elevate our collective know-how.
A sincere "thank you" can brighten someone's day—leave your appreciation below!
On DEV, **sharing knowledge smooths our journey** and tightens our community bonds. Enjoyed this? A quick thank you to the author is hugely appreciated.
