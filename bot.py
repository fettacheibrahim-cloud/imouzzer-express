import os
import requests
import feedparser
import random

# قراءة الرمز من Secret بأمان
PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_TOKEN')
PAGE_ID = '110232817345910'
SITE_URL = 'https://fettacheibrahim-cloud.github.io/imouzzer-express/'

RSS_SOURCES = [
    'https://www.hespress.com/feed',
    'https://www.Hespress.com/tag/إفران/feed'
]

def fetch_random_news():
    print("🔍 جاري تفقد مصادر الأخبار...")
    all_entries = []
    for url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                all_entries.extend(feed.entries)
        except Exception as e:
            print(f"⚠️ تعذر القراءة من {url}: {e}")
            
    if all_entries:
        chosen = random.choice(all_entries[:10])
        return chosen.title, SITE_URL
    
    return "مستجدات وتغطيات مستمرة لجهة إيموزار كندر وإقليم إفران", SITE_URL

def format_moroccan_style(title):
    moroccan_intro = "🇲🇦 #إيموزار_إكسبريس | متابعات وجهوية:\n\n"
    body = f"📢 في التفاصيل: {title}\n\nللاطلاع على باقي التفاصيل، تجدون المقال كاملًا عبر موقعنا أسفله. 👇"
    return moroccan_intro + body

def publish_to_facebook(message, link):
    url = f"https://graph.facebook.com/v26.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'link': link.strip(),
        'access_token': PAGE_ACCESS_TOKEN
    }
    try:
        response = requests.post(url, data=payload)
        res_data = response.json()
        if 'id' in res_data:
            print(f"✅ تم النشر بنجاح سحابياً! المعرّف: {res_data['id']}")
        else:
            print(f"❌ خطأ من فيسبوك: {res_data}")
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")

if __name__ == "__main__":
    print("🤖 تشغيل البوت عبر GitHub Actions...")
    title, link = fetch_random_news()
    if title and link:
        msg = format_moroccan_style(title)
        publish_to_facebook(msg, link)
