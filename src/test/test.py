import argparse
import requests
import time

parser = argparse.ArgumentParser(description="A test")

parser.add_argument(
    "-u", "--url", type=str, default="http://localhost:3099", help="Base url of api"
)
parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")

# https://stackoverflow.com/a/287944
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def test_status():
    start = time.time()
    url = f"{base_url}/api/status"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.get(url)
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True


def test_whisper():
    start = time.time()
    url = f"{base_url}/api/whisper/transcribe"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_pyannote_diorization():
    start = time.time()
    url = f"{base_url}/api/pyannote/diorize"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_pyannote_embed():
    start = time.time()
    url = f"{base_url}/api/pyannote/embed"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_pyannote():
    test_pyannote_diorization()
    test_pyannote_embed()

def test_text_embed():
    start = time.time()
    url = f"{base_url}/api/embed"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={"text": ["test"]})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_info():
    start = time.time()
    url = f"{base_url}/api/weaviate/getInfo"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.get(url)
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_get_collections():
    start = time.time()
    url = f"{base_url}/api/weaviate/getCollections"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.get(url)
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_create_collection():
    start = time.time()
    url = f"{base_url}/api/weaviate/createCollection"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={"name": "TestCollection", "vector_index_hnsw": True, "distance_config": "cosine", "properties": [{"name": "testField", "data_type": "text"}]})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_get_collection():
    start = time.time()
    url = f"{base_url}/api/weaviate/getCollection"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={"collection": "TestCollection"})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_insert():
    start = time.time()
    url = f"{base_url}/api/weaviate/insert"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(
        url,
        json={
            "collection": "TestCollection",
            "objects": [
                {"object": {"testField": "dit is een test"}, "vector": [0.1] * 10}
            ],
        },
    )
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_search_hybrid():
    start = time.time()
    url = f"{base_url}/api/weaviate/searchHybrid"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(
        url,
        json={
            "collection": "TestCollection",
            "query": "test",
            "vector": [0.1, 0.08, 0.11, -0.3, 0.17, 0.3, 0.43, 0.11, 0.1234, 0.5],
            "limit": 1,
            "alpha": 0.2,
            "query_properties": ["testField"],
        },
    )
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_search_bm25():
    start = time.time()
    url = f"{base_url}/api/weaviate/searchBM25"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(
        url,
        json={
            "collection": "TestCollection",
            "query": "test",
            "limit": 1,
            "query_properties": ["testField"],
        },
    )
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")


    return True

def test_weaviate_search_vector():
    start = time.time()
    url = f"{base_url}/api/weaviate/searchVector"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(
        url, json={"collection": "TestCollection", "vector": [0.1, 0.08, 0.11, -0.3, 0.17, 0.3, 0.43, 0.11, 0.1234, 0.5], "limit": 1}
    )
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_delete():
    start = time.time()
    url = f"{base_url}/api/weaviate/deleteEntry"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate_delete_collection():
    start = time.time()
    url = f"{base_url}/api/weaviate/deleteCollection"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={"collection": "TestCollection"})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True

def test_weaviate():
    test_weaviate_info()
    test_weaviate_get_collections()
    test_weaviate_create_collection()
    test_weaviate_get_collection()
    test_weaviate_insert()
    test_weaviate_search_hybrid()
    test_weaviate_search_bm25()
    test_weaviate_search_vector()
    test_weaviate_delete()
    test_weaviate_delete_collection()

def test_llm():
    start = time.time()
    url = f"{base_url}/api/chat"
    if verbose:
        print(f"\nTesting {url}")
    r = requests.post(url, json={})
    if verbose:
        print(f"Took {round(time.time()-start, 3)} seconds")
    if r.status_code != 200:
        print(
            f"{bcolors.FAIL}{url} failed{bcolors.ENDC}"
        )
        if verbose:
            print(f"{bcolors.WARNING}status code: {r.status_code}, detail: {r.json().get('detail')}{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.OKGREEN}{url} passed{bcolors.ENDC}")

    return True


if __name__ == "__main__":
    args = parser.parse_args()
    # global verbose
    verbose = args.verbose
    base_url = args.url

    test_status()
    # test_whisper()
    # test_pyannote()
    test_text_embed()
    test_weaviate()
    # test_llm()
