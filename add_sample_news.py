import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import News
from django.utils.text import slugify

def create_sample_news():
    # Sample news article 1
    news1 = News.objects.create(
        title="New Summer Collection Arriving Soon!",
        slug=slugify("New Summer Collection Arriving Soon"),
        content="""Get ready for the hottest styles of the season! Our new summer collection is about to drop, 
        featuring breathtaking designs, vibrant colors, and the latest fashion trends.

        What to expect:
        - Exclusive designer pieces
        - Sustainable fashion items
        - Limited edition accessories
        - Special launch day discounts

        Stay tuned for the official launch date and be the first to shop these amazing new arrivals!""",
        status='published'
    )

    # Sample news article 2
    news2 = News.objects.create(
        title="Special Holiday Season Discounts",
        slug=slugify("Special Holiday Season Discounts"),
        content="""🎉 Celebrate the holiday season with incredible savings across our entire store!

        🎁 Special Offers:
        - Up to 50% off on selected items
        - Buy 2 Get 1 Free on accessories
        - Free shipping on orders over $50
        - Extra 10% off for loyalty members

        Don't miss out on these amazing deals. Sale starts this Friday!

        Terms and conditions apply. Visit our store for more details.""",
        status='published'
    )

    print("Sample news articles created successfully!")

if __name__ == '__main__':
    create_sample_news()
