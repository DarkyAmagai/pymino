from typing import TextIO
from re import search, sub
from os import listdir, makedirs, path, remove
from ujson import load, dump, JSONDecodeError

class LiteCache:
    def __init__(self, url: str, method: str=None, data: dict=None, response: dict=None):
        self.url:       str = url
        self.method:    str = method
        self.data:      dict = data
        self.response:  dict = response
        file_dir:       str = path.dirname(path.abspath(__file__))        
        url:            str = self.url.replace("http://service.aminoapps.com/api/v1/g/", "")

        if any(char in url for char in ["?", "&"]):
            url = url[:url.find("?")]

        if not path.exists(path.join(file_dir, "cache")):
            makedirs(path.join(file_dir, "cache"))

        self.cache_file = path.join(
            file_dir,
            "cache",
            f"{sub('https?://', '', url).replace('/', '_')}.json"
            )
        
        if not path.exists(self.cache_file):
            with open(self.cache_file, "w") as f:
                f.write("")

    def is_link_resolution(self) -> bool:
        return search("link-resolution", self.url) is not None

    def prepare_data(self) -> dict:
        data = None

        if self.is_link_resolution():
            data = {"url": self.url, "data": self.data, "response": self.response}     

        return data

    def save(self) -> None:
        data = self.prepare_data()
        if any((data is None, self.already_exists(data))):
            return None
        with open(self.cache_file, "a+") as file:
            self.save_helper(file, data)

    def save_helper(self, file: TextIO, data: dict) -> None:
        file.seek(0)

        try:
            cached_data = load(file)
        except JSONDecodeError:
            cached_data = []

        cached_data.append(data)
        file.seek(0)
        file.truncate()
        dump(cached_data, file, indent=4)

    def already_exists(self, data: dict) -> bool:
        if path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return data in load(f)
            except JSONDecodeError:
                return False
            
        return False
    
    def get(self) -> dict:
        if path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return self.get_helper(f)
        return None
    
    def get_helper(self, file: TextIO) -> dict:
        file.seek(0)
        try:
            cached_data = load(file)
        except JSONDecodeError:
            return None
        
        if self.is_link_resolution():
            try:
                return next((cache_data["response"] for cache_data in cached_data if cache_data["url"] == self.url), None)
            except KeyError:
                with open(self.cache_file, "w") as f:
                    f.write("")
        return None
    
    def clear() -> None:
        for file in listdir(path.join(path.dirname(path.abspath(__file__)), "cache")):
            if file != "login_cache.json":
                remove(path.join(path.dirname(path.abspath(__file__)), "cache", file))