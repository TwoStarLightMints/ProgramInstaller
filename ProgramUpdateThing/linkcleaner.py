import requests
from urllib.parse import urlparse, urlunparse
from difflib import SequenceMatcher

# Implement something to guard against accidentally downloading an html page instead of the actual binary executable


# Find a link, given the given link, which will be sustainable to use for future updates
class LinkCleaner:
    def __init__ (self, link: str):
        print("Link is currently being checked...")
        self._raw_link = link
        self.versioned = self._is_versioned(link)

        if self.versioned:
            print("Link is not clean, cleaning to commence\nThis process can take a few seconds...")
            # The unversioned link is by definition ready to find a download link that is versioned to be used in downloading the up to date exe.
            # Because I have back tracked through the link's path, I need to find a way forward s.t. I find the download link with a new version
            # or find a page where I can find the download link
            self.unversioned_link = self._recur_handle_versioned(self._raw_link)
            
            if len(self.find_all_case_sensitive(urlparse(self.unversioned_link).netloc, ".")) > 1:
                self.unversioned_link = self._handle_404(self._remove_special_netloc_info(self.unversioned_link))
            self.clean_link = self.find_link_from_unversioned(self.unversioned_link)
            print("Link has been cleaned, processing will continue")
        
        else:
            print("Link is clean, processing will continue")
            self.clean_link = self._raw_link

# -------------------------------------------------------------- HANDLE VERSIONED LINKS --------------------------------------------------------------

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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ HANDLE VERSIONED LINKS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ----------------------------------------------------------- FIND LINK WITHIN THE WEBPAGE -----------------------------------------------------------
    
    def find_element_by_tag (self, html: str, tag: str, start_index: int) -> str:
        """Assumes that the start index will be inside of the element (could start in attributes area, content area, etc.).
        Tag is given as the ***CSS ELEMENT SELECTOR***, for example, "a", "div", "h1", etc.
        Returns the element as a string."""
        start_of_opening_tag = "<" + tag
        end_of_closing_tag = "</" + tag + ">"
        start = self.find_beginning_of_tag(html, start_of_opening_tag, start_index)
        if start != -1:
            end = self.find_ending_of_tag(html, end_of_closing_tag, start_index)
            return html[start: end]
        else:
            return ""

    def find_beginning_of_tag (self, html: str, start_tag: str, start_index: int) -> int:
        """Finds the index of the beginning of an element and returns it as an integer.
        The start index is assumed to be inside of the element.
        The start tag will be given in the format of "<a" or "<div"."""
        while html[start_index - len(start_tag): start_index] != start_tag:
            start_index -= 1
            if start_index < 0:
                return -1
        return start_index - len(start_tag)

    def find_ending_of_tag (self, html: str, end_tag: str, start_index: int) -> int:
        """Finds the index of the ending of an element and returns it as an integer.
        The start index is assumed to be inside of the element.
        The end tag will be given in the normal html format of "</[insert valid html element here]>"."""
        while html[start_index: start_index + len(end_tag)] != end_tag:
                start_index += 1
                if start_index > len(html):
                    return -1
        return start_index + len(end_tag)
    
    def find_all_case_sensitive (self, string: str, sub_str: str) -> list[int]:
        """Finds all the indexes at which the given sub string occurs within the given string and returns the indexes in a list of integers."""
        found_indeces: list[int] = []
        start = 0

        while string.find(sub_str, start) != -1:
            found_indeces.append(string.find(sub_str, start))
            start = string.find(sub_str, start) + 1
        
        return found_indeces
    
    def get_href_data (self, element: str) -> str:
        href_index = element.find("href")

        start_for_search = href_index + len("href=") # This will be the index inside the element where the href data will start either as a " or the data

        # From where the href attribute text begins, the actual link data is 5 characters away
        end_data = 0

        if element[start_for_search] == '"':
            for char in element[start_for_search + 1:]:
                if char == '"' or char == " " or char == ">":
                    break
                end_data += 1
            start_for_search += 1

        else:
            for char in element[start_for_search:]:
                if char == " " or char == ">":
                    break
                end_data += 1

        return element[start_for_search: start_for_search + end_data]
    
    def get_list_of_download_links (self, link: str) -> set[str]:
        html = requests.get(link).text

        links: set[str] = set()

        for index in self.find_all_case_sensitive(html, "download"):
            element = self.find_element_by_tag(html, "a", index)
            if element:
                generated_link = self.get_valid_urls(self.get_href_data(element), link)

                if generated_link != None and "download" in generated_link.lower() and urlparse(link).netloc in urlparse(generated_link).netloc:
                    links.add(generated_link)

        return links
    
    def check_is_url (self, link) -> bool:
        parsed_link = urlparse(link)
        return ((parsed_link.scheme != "" and (parsed_link.scheme == "https" or parsed_link.scheme == "http")) and parsed_link.netloc != "" and parsed_link.path != "")
    
    def build_url (self, href, link) -> str:
        original_link = urlparse(link)
        return urlunparse((original_link.scheme, original_link.netloc, href, '', '', ''))
    
    def get_valid_urls (self, href: str, link: str) -> str:
        if self.check_is_url(href):
            return href
        elif href.strip() != "" or not href is None:
            return self.build_url(href, link)
    
    def compare_links_to_original (self, original: str, links: list[str]) -> list[str]:
        to_order = []
        for link in links:
            original_parsed = urlparse(original)
            compare_stuff_original = original_parsed.path + original_parsed.params + original_parsed.query + original_parsed.fragment
            link_parsed = urlparse(link)
            compare_stuff_link = link_parsed.path + link_parsed.params + link_parsed.query + link_parsed.fragment
            compare = SequenceMatcher(None, original, link_parsed.query)
            to_order.append([link, compare.ratio()])
        
        length = len(to_order)

        for i in range(0, length):
            for j in range(0, length-i-1):
                if to_order[j][1] > to_order[j + 1][1]:
                    temp = to_order[j]
                    to_order[j] = to_order[j + 1]
                    to_order[j + 1] = temp
        
        ordered = []

        for comparison in to_order:
            ordered.append(comparison[0])
            
        ordered.reverse()

        return ordered

    def find_link_from_unversioned (self, unversioned_link: str) -> str:
        """This function will retrieve a link from a "versioned" link by recursively searching a webpage for a new link that could go to a download page, an exe specifically, or so on.
        Here, a versioned link refers to any download link which contains versioning information such as "11.28" inside of it.
        Given that this class is to be used with the updater program, it would make no sense to store a versioned download link, as this would nullify the usefulness of this app"""

        placeholder_webpage_link: str = ""
        priority_webpage_link: str = ""

        links = self.get_list_of_download_links(unversioned_link)
        sorted_links = self.compare_links_to_original(self._raw_link, links)

        for link in sorted_links:
            url_path = urlparse(link).path

            if ".exe" in url_path or ".zip" in url_path:
                if "mac" in url_path or "linux" in url_path:
                    continue
                else:
                    return link
            
            contents = requests.get(link).text

            if "DOCTYPE" in contents:
                if "thank" in link:
                    return self.find_link_from_unversioned(link)
                placeholder_webpage_link = link
        
        if priority_webpage_link:
            return self.find_link_from_unversioned(priority_webpage_link)
        return self.find_link_from_unversioned(placeholder_webpage_link)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ FIND LINK WITHIN THE WEBPAGE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





if __name__ == "__main__":
    freefilesync = "https://freefilesync.org/download/FreeFileSync_11.28_Windows_Setup.exe"
    someotherthing = "https://macroplant.com/adapter/download/pc/complete/2.1.2"
    videodownloader = "https://dl.4kdownload.com/app/4kvideodownloader_4.22.2_online.exe?source=website"

    cleaner = LinkCleaner(someotherthing)

    print(f"CLEANED LINK: {cleaner.clean_link}")
    