import requests
import hashlib
import sys
from getpass import getpass
import stdiomask


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}, check the api and try again"
        )
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    paswrd = stdiomask.getpass("password: ", "*")
    for password in [paswrd]:
        count = pwned_api_check(password)
        if count:
            print(f"{password} was fount {count} times .. you should change it now!!")
        elif len(paswrd) == 0:
            print(f"{password} please write the password!!")
        else:
            print(f"{password} was Not found. All clear!!")
    return "Done!"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
