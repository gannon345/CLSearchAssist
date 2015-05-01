from bs4 import BeautifulSoup
import urllib2
import re


def try_url(url):
    """For testing if the URL is a valid page"""
    try:
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urllib2.urlopen(req)
        return True
    except urllib2.URLError:
        return False


def get_listings(soup):
    maptags = soup.findAll(class_="maptag")
    list_string = str(maptags)
    tag_list = re.findall('\d+', list_string)
    return tag_list

def url_soup(url):
    valid_url = try_url(url)
    if valid_url:
        bs_req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib2.urlopen(bs_req).read()
        soup = BeautifulSoup(html)
        return soup

    else:
        print("Invalid URL")

def tags_to_urls(tags, base_url):
    listing_urls = []
    for item in tags:
        listing_urls.append(base_url + item + ".html")

    return listing_urls



def exclusion_list():
    pass


def main():

    search_mod = {'titlesOnly': 'srchType=T&', 'hasImage': 'hasPic=1&', 'postedToday': 'postedToday=1&',
        'catsAllowed': 'pets_cat=1&', 'dogsAllowed': 'pets_dog=1&', 'privateBath': 'private_bath=1&',
        'minPrice': 'minAsk=', 'maxPrice': 'maxAsk=', 'bedrooms': 'bedrooms=','bathrooms': 'bathrooms=',
        'minSqft': 'minSqft=', 'maxSqft': 'maxSqft='
        }


    city = raw_input("City?: ")
    url = "http://" + city + ".craigslist.org/search/apa?"
    base_listing_url = "http://" + city + ".craigslist.org/apa/"
    if raw_input("Search titles only? (y/n): ") == "y":
        url += search_mod['titlesOnly']

    if raw_input("Search only listings with pictures (y/n): ") == "y":
        url += search_mod['hasImage']

    if raw_input("Search only items posted today? (y/n): ") == "y":
        url += search_mod['postedToday']

    if raw_input("Cats allowed? (y/n): ") == "y":
        url += search_mod['catsAllowed']

    if raw_input("Dogs allowed? (y/n): ") == "y":
        url += search_mod['dogsAllowed']

    if raw_input("Private bath? (y/n): ") == "y":
        url += search_mod['privateBath']

    num_str = raw_input("Minimum price (leave blank if you don't care): ")
    if num_str is not '':
        url += search_mod['minPrice'] + num_str + '&'

    num_str = raw_input("Maximum price: ")
    if num_str is not '':
        url += search_mod['maxPrice'] + num_str + '&'

    num_str = raw_input("Number of bedrooms (leave blank if you don't care): ")
    if num_str is not '':
        url += search_mod['bedrooms'] + num_str + '&'

    num_str = raw_input("number of bathrooms (leave blank if you don't care): ")
    if num_str is not '':
        url += search_mod['bathrooms'] + num_str + '&'

    num_str = raw_input("Minimum square feet (leave blank if you don't care): ")
    if num_str is not '':
        url += search_mod['minSqft'] + num_str + '&'

    num_str = raw_input("Maximum square feet (leave blank if you don't care): ")
    if num_str is not'':
        url += search_mod['maxSqft'] + num_str + '&'

    num_str = raw_input("Select a specific open house date? (FORMAT: YYYY-MM-DD). Leave blank if you don't care: ")
    if num_str is not '':
        url += 'sale_date=' + num_str

    print(url)
    raw_soup = url_soup(url)
    maptag_list = get_listings(raw_soup)
    listings = tags_to_urls(maptag_list, base_listing_url)
    print("number of listings: " + str(len(listings)))

    for urls in listings:
        print urls

if __name__ == "__main__":
    main()