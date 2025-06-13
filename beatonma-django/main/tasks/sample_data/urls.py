import random
from urllib.parse import urljoin

# ChatGPT
HOMEPAGES = [
    "https://www.foodielifestyleblog.com/",
    "https://www.traveladventurespost.com/",
    "https://www.diyhomedecorhub.com/",
    "https://www.petcareandtrainingtips.net/",
    "https://www.healthyfitlifestyle.com/",
    "https://www.bookloversguide.net/",
    "https://www.fashionandbeautyzone.com/",
    "https://www.mindfulmeditationjourney.com/",
    "https://www.sportsfanaticsarena.com/",
    "https://www.dailyfinanceguide.net/",
    "https://www.wineanddineblog.com/",
    "https://www.thecreativewritershub.com/",
    "https://www.travelcultureblog.net/",
    "https://www.techreviewhub.com/",
    "https://www.parentingtipsandtricks.com/",
    "https://www.adventurousoutdoorsman.com/",
    "https://www.popculturejunkies.com/",
    "https://www.homeschoolingmadeeasy.com/",
    "https://www.businessinsightsdaily.com/",
    "https://www.humanitiesandartsblog.com/",
    "https://www.gardeninggreenthumb.com/",
    "https://www.mentalwellnesscorner.com/",
    "https://www.craftycreationscentral.com/",
    "https://www.luxurytravelspotlight.com/",
    "https://www.petsandtheirpeople.com/",
]


PATHS = [
    "/product/electronics/smartphones",
    "/category/home-garden/kitchen-dining",
    "/blog/post/10-tips-for-healthy-eating",
    "/page/about-us",
    "/contact",
    "/blog/category/travel",
    "/product/clothing/womens/tops",
    "/category/electronics/accessories",
    "/blog/tag/fitness",
    "/blog/post/the-ultimate-guide-to-diy-home-decor",
    "/product/toys-kids/baby-toys",
    "/category/beauty/makeup",
    "/blog/category/finance",
    "/page/faqs",
    "/product/sports-outdoors/camping-hiking",
    "/category/books/mystery",
    "/blog/post/how-to-plan-your-dream-vacation",
    "/product/home-garden/furniture",
    "/blog/tag/pets",
    "/category/food-drink/recipes",
    "/page/terms-of-service",
    "/product/health-wellness/supplements",
    "/blog/category/music",
    "/product/office-supplies/desk-accessories",
    "/category/cars-motorcycles/car-parts-accessories",
]


def any_homepage():
    return random.choice(HOMEPAGES)


def any_urlpath():
    return random.choice(PATHS)


def any_url():
    return urljoin(any_homepage(), any_urlpath())
