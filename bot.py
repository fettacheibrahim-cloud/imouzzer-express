import os
import requests
import feedparser

# قراءة رمز المصادقة الخاص بصفحة فيسبوك من متغيرات البيئة
PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
# يمكنك استبدال هذا الرابط برابط مصدر الأخبار (RSS Feed) الخاص بموقعك أو صفحتك
RSS_FEED_URL = "https://example.com/rss" # ضع رابط الـ RSS الخاص بك هنا

def post_to_facebook(message):
    """دالة لنشر المحتوى على صفحة فيسبوك باستخدام Facebook Graph API"""
    if not PAGE_TOKEN:
        print("Error: FB_PAGE_TOKEN is not set in repository secrets.")
        return False

    url = f"https://graph.facebook.com/v17.0/me/feed"
    payload = {
        'message': message,
        'access_token': PAGE_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        
        if 'id' in result:
            print("Post published successfully with ID:", result['id'])
            return True
        else:
            print("Failed to publish post:", result)
            return False
    except Exception as e:
        print("An error occurred during posting:", e)
        return False

def main():
    print("Starting bot execution...")
    
    # مثال توضيحي لجلب أحدث خبر من مصدر RSS والنشر تلقائياً
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        if feed.entries:
            latest_entry = feed.entries[0]
            post_message = f"{latest_entry.title}\n\n{latest_entry.link}"
            print("Found new article, publishing to Facebook...")
            post_to_facebook(post_message)
        else:
            print("No entries found in the RSS feed.")
    except Exception as e:
        print("Error parsing RSS feed or running bot:", e)

if __name__ == "__main__":
    main()
