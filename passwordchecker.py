import requests
import hashlib
import sys


def request_api_data(querry_char):

    url = "https://api.pwnedpasswords.com/range/", querry_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, try again")

    return res


def get_password_leaks_count(hashes, hash_to_check):

    hashes = (line.splitLine(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):

    sha1password = hashlib.sha1(password.encode('utf-8')).hexdiges().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return read_res(response, tail)

    return sha1password


def main(args):
    for password in args:
        count = pwned_api_check(password)

        if count:
            print(
                f"{password} was found {count} times.... You should probably change it")

        else:
            print(f"{password} was not found. Continue with the same password")

        return "done"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
