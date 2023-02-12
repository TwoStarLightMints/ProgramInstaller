import re
import requests
from urllib.parse import urlparse, urlunparse
from difflib import SequenceMatcher

class LinkFinder:
    def __init__(self, link: str):
        self._raw_link
        self.versioned = self._is_versioned(link)

        if self.versioned:
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

    def find_link_from_unversioned(self, link: str):
        resp = requests.get(link)
        html = resp.content

        links = re.findall('(https|http):\/\/[a-zA-Z0-9_]*?\.[a-zA-Z0-9_]*[^"]*', html) # This funky dude selects any valid link within a website because of regex magic and the fact that no matter where the link is we will hope and pray to god that the link will end with a double quote