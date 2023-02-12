import re
import requests
from urllib.parse import urlparse, urlunparse
from difflib import SequenceMatcher

class LinkFinder:
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