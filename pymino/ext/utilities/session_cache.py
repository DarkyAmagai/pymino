from os import path, mkdir
from typing import TextIO
from ujson import load, dump, JSONDecodeError

class SessionCache:
    def __init__(self, email: str, sid: str=None, response: dict=None):
        self.email:     str = email
        self.sid:       str = sid
        self.response:  dict = response

        file_dir:       str = path.dirname(path.abspath(__file__))
        
        if not path.exists(path.join(file_dir, "cache")):
            mkdir(path.join(file_dir, "cache"))

        if not path.exists(path.join(file_dir, "cache", "login_cache.json")):
            with open(path.join(file_dir, "cache", "login_cache.json"), "w") as f:
                f.write("")

        self.cache_file: str = path.join(file_dir, "cache", "login_cache.json")

    def save(self, force_update: bool = False) -> None:
        if all([self.already_exists(), not force_update]):
            return self.get()

        with open(self.cache_file, "a+") as file:
            self.save_helper(file, {"email": self.email, "sid": self.sid}, force_update)

    def save_helper(self, file: TextIO, data: dict, force_update: bool) -> None:
        file.seek(0)

        try:
            cached_data = load(file)
        except JSONDecodeError:
            cached_data = []

        if not force_update:
            cached_data.append(data)
        else:
            try:
                cached_data = list(filter(lambda x: x["email"] != self.email, cached_data))
                cached_data.append(data)
            except KeyError:
                with open(self.cache_file, "w") as f:
                    f.write("")

        file.seek(0)
        file.truncate()
        dump(cached_data, file, indent=4)
    
    def get(self) -> tuple:
        if path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return self.get_helper(f)
        return None
    
    def get_helper(self, file: TextIO) -> tuple:
        file.seek(0)
        try:
            cached_data = load(file)
        except JSONDecodeError:
            return None
        
        try:
            return next((
                cache_data["sid"]
                for cache_data in cached_data
                if cache_data["email"] == self.email
            ), None)
            
        except KeyError:
            with open(self.cache_file, "w") as f:
                f.write("")
        
        return None
    
    def already_exists(self) -> bool:
        if path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return self.already_exists_helper(f)
            except JSONDecodeError:
                return False
            
        return False
    
    def already_exists_helper(self, file: TextIO) -> bool:
        file.seek(0)
        try:
            cached_data = load(file)
        except JSONDecodeError:
            return False
        
        try:
            return any(
                cache_data["email"] == self.email
                for cache_data in cached_data
            )
        except KeyError:
            with open(self.cache_file, "w") as f:
                f.write("")
        
        return False
    
    def clear(self) -> None:
        if path.exists(self.cache_file):
            with open(self.cache_file, "w") as f:
                f.write("")