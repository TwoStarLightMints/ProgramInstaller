import re
import requests
from urllib.parse import urlparse, urlunparse
from difflib import SequenceMatcher

class LinkFinder:
    def __init__(self, link: str):
        self._raw_link = link
        self.versioned = self._is_versioned(link)

        if "github" in urlparse(self._raw_link).netloc:
            url_path = urlparse(self._raw_link).path.split("/")
            
            input("Link points to a github repo, the returned link will point to all future releases, please do not change it. Press enter to continue...")
            self.clean_link = f"https://api.github.com/repos/{url_path[1]}/{url_path[2]}/releases/latest"
        
        elif self.versioned:
            print("Link is not clean, cleaning to commence\nThis process can take a few seconds...")
            self.unversioned_link = self._recur_handle_versioned(self._raw_link)
            
            # Remove the information that appears after http/https but before domain name
            # https://netloc.domain.com/something_else
            #          /\ This here
            if len(re.findall("\.", urlparse(self.unversioned_link).netloc)) > 1:
                self.unversioned_link = self._handle_404(self._remove_special_netloc_info(self.unversioned_link))
            self.clean_link = self.find_link_from_unversioned(self.unversioned_link)
            print("Link has been cleaned, processing will continue")
        
        else:
            print("Link is clean, processing will continue")
            self.clean_link = self._raw_link

    def _is_versioned (self, link: str) -> bool:
        path = urlparse(link).path
        coincidence = 0
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for char in path:
            if char in nums or char == '.':
                coincidence += 1
        
        if coincidence > 3:
            return True
        
        return False

    def _recur_handle_versioned (self, link: str) -> str:
        last_forward_index = link.rfind("/")

        if last_forward_index != -1:
            shortened_link = link[:last_forward_index]
            r = requests.get(shortened_link)

            if r.status_code == 404:
                return self._recur_handle_versioned(shortened_link)
            
            else:
                return shortened_link

    def _remove_special_netloc_info (self, link: str) -> str:
        parsed = urlparse(link)
        return urlunparse(parsed._replace(netloc=parsed.netloc[parsed.netloc.find(".") + 1: len(parsed.netloc)]))
    
    def _handle_404 (self, link: str) -> str:
        status = requests.get(link).status_code

        if status == 404:
            last_forward_index = link.rfind("/")

            return self._handle_404(link[: last_forward_index])
        return link

    def check_is_url (self, link) -> bool:
        parsed_link = urlparse(link)
        return ((parsed_link.scheme != "" and (parsed_link.scheme == "https" or parsed_link.scheme == "http")) and parsed_link.netloc != "" and parsed_link.path != "")

    def find_link_from_unversioned(self, link: str):
        resp = requests.get(link)
        html = resp.content.decode()

        links: list = re.findall('(?:https|http):\/\/[a-zA-Z0-9_]*?\.[a-zA-Z0-9_]*[^ "*<]*', html) # This funky dude selects any valid link within a website because of regex magic and the fact that no matter where the link is we will hope and pray to god that the link will end with a double quote

        partial_links: list[tuple[str]] = re.findall('(href=")([^ <]*)(")', html)
        for partial_link in partial_links:
            if not partial_link[1].startswith("http") and self.check_is_url(link + partial_link[1]):
                links.append(link + partial_link[1])
        
        promising_links = list()

        for link in links:
            # Found the goal, return early here
            if re.search("\.exe|installer", link, re.IGNORECASE):
                return link
            # Bruh, just keep going, this one is more likely the goal
            elif re.search("download", link):
                promising_links.append(link)
            # Just keep going, maybe the next round will work
            else:
                continue
        
        print(promising_links)

        if len(promising_links) != 0:
            return self.find_link_from_unversioned(promising_links[0])

if __name__ == "__main__":
    finder = LinkFinder("https://github.com/FireFox2000000/Moonscraper-Chart-Editor/releases")
    print(finder.clean_link)