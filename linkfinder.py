import re

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