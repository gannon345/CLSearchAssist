from bs4 import BeautifulSoup
import urllib2
import re
import time
import os


def try_url(url):
    """For testing if the URL is a valid page"""
    try:
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urllib2.urlopen(req)
        return True
    except urllib2.URLError:
        return False


def get_listings(soup):
    """Pulls all html links for apartment listings from the Craigslist RSS, then returns them as a list"""
    url_list = soup.items
    list_string = str(url_list)
    listings = re.findall('http://' + '\w+.\w+.\w+.\w+.\w+.\w+', list_string)
    return listings


def url_soup(url):
    """Gets the BeautifulSoup "soup" for the URL requested and returns it"""
    valid_url = try_url(url)
    time.sleep(1)
    if valid_url:
        bs_req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib2.urlopen(bs_req).read()
        soup = BeautifulSoup(html)
        return soup

    else:
        print("Invalid URL")


def create_exclusion_list(user_exclusions):
    """Takes a predefined list of words in a string, splits to a list on comma and strips extra white space.
       Then returns the list."""
    exclusions = user_exclusions.split(',')
    exclusions = [s.strip() for s in exclusions]
    return exclusions


def remove_exclusions(listings, exclusions):
    """Takes in list of URLs for apartments and the list of words for excluding items. Iterates through the URLs,
       running url_soup() and parsing through for the excluded words. If an exclusion is found, the url is removed from
       the list. After all items are iterated, the new list is returned"""
    updated_listings = listings
    for url in updated_listings:
        html_string = str(url_soup(url)).lower()
        time.sleep(1)
        print("checking " + url)
        for exclusion in exclusions:
            if exclusion in html_string:
                print ("Search exclusion found, removing " + url + " from the list")
                updated_listings.remove(url)
                time.sleep(1)
                break
    return updated_listings


def write_to_file(address_url):
    """Writes the site page from address_url to a file, in a separate folder called "listings" and if the "listings"
       folder does not exist, creates it."""

    if not os.path.isdir('listings'):
        os.mkdir('listings')

    filename = address_url
    filename = filename[33:]
    if os.name == 'nt':
        f = open('listings/' + filename, 'wb')
    else:
        f = open('listings/' + filename, 'w+')
    write_req = urllib2.Request(address_url, headers={'User-Agent': 'Mozilla/5.0'})
    site = urllib2.urlopen(write_req)
    print("writing file: " + address_url + " to local disk...")
    f.write(site.read())
    f.close()


def main():

    search_mod = {'titlesOnly': 'srchType=T&', 'hasImage': 'hasPic=1&', 'postedToday': 'postedToday=1&',
                  'catsAllowed': 'pets_cat=1&', 'dogsAllowed': 'pets_dog=1&', 'privateBath': 'private_bath=1&',
                  'minPrice': 'minAsk=', 'maxPrice': 'maxAsk=', 'bedrooms': 'bedrooms=', 'bathrooms': 'bathrooms=',
                  'minSqft': 'minSqft=', 'maxSqft': 'maxSqft='
                  }

    city = raw_input("City?: ")
    url = "http://" + city + ".craigslist.org/search/apa?"
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

    url += "format=rss"

    excluded_terms = raw_input("What terms to exclude from listings (please separate with commas, lower case only)?: ")
    excluded_terms = create_exclusion_list(excluded_terms)
    print excluded_terms

    print("search path: " + url)
    raw_soup = url_soup(url)
    listings = get_listings(raw_soup)

    print("number of listings: " + str(len(listings)))
    print("Removing listings with excluded terms now...\n This may take a while, please be patient.")

    listings = remove_exclusions(listings, excluded_terms)
    print(str(len(listings)) + " listings found after removing exclusions. Writing to file...")

    for item in listings:
        print("Saving " + item + " to file.")
        write_to_file(item)
        time.sleep(1)


if __name__ == "__main__":
    main()