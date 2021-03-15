import requests
import os
import datetime.datetime
from bs4 import BeautifulSoup

# Website class for handling the links


class LinkManager:
    def __init__(self, page_url, prefix_url, query):
        self.prefix_url = prefix_url
        self.page_url = page_url
        self.webpage = requests.get(page_url)
        self.soup = BeautifulSoup(self.webpage.text, 'html.parser')
        self.links = []
        app_links = self.soup.find_all("a", query)

        for el in app_links:
            self.links.append(self.prefix_url + el.attrs['href'])

    def delete_old_persistance(self):
        """
        Delete the file from last week, if it exists
        """
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        seven_days_ago_day = seven_days_ago.strftime("%d")
        filename = f"persistence/links_{seven_days_ago_day}"
        try:
            os.remove(filename)
        except OSError:
            pass

    def persist(self):
        """
        Persist links to local file. All LinkManagers append to same file at same day.
        Use compress_persistence method to remove duplicates
        """
        day = datetime.datetime.now().strftime("%d")
        filename = f"persistence/links_{day}"
        
        # append file with current links
        with open(filename, 'a+') as f:
            f.write("\n".join(self.links))

        # delete file if 7 days old
        self.delete_old_persistance()

    def compress_persistence(self):
        """
        Removes all duplicates from all files in persistence/
        """
        for filename in os.scandir("persistence/"):
            content = [] 
            with open(filename) as f:
                content = f.readlines()
                content = [x.strip() for x in content]
                # remove duplicates
                content = list(dict.fromkeys(content))
                content.sort()
            with open(filename, 'w') as f: 
                f.writelines(content)
