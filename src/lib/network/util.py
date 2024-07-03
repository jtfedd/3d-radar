from typing import Dict

import requests


def makeRequest(
    url: str,
    params: Dict[str, str],
    timeout: float,
) -> requests.Response | None:
    try:
        headers = {
            "User-Agent": "Stormfront3DRadar/0.0.0",
        }

        response = requests.get(
            url,
            params=params,
            timeout=timeout,
            headers=headers,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None

    return response
