from bs4 import BeautifulSoup
import urllib3

base = "https://www.youtube.com/results?q="
http = urllib3.PoolManager()

def youtube_websearch(search_query):
    url = base + search_query

    r = http.request('GET', url)
    html = r.data

    soup = BeautifulSoup(html, features="html.parser")

    results = soup.find(id="results")
    results = results.find(class_="item-section")
    a = list(results)
    return_items = []
    for item in results:
        if item == "\n":
            continue
        if "Searches related to" in item.text:
            continue

        content = item.find(class_="yt-lockup-content")
        # get type (video, channel or playlist)
        content_type = content.find(class_="accessible-description").text[3:].lower()

        if content_type not in ["channel", "playlist"]:
            content_type = "video"
        content_type = f"youtube#{content_type}"

        # get name and id
        title = content.find(class_="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link")
        if content_type == "youtube#playlist" \
                or content_type == "youtube#video":
            id = title.get("href").split("v=")[-1]
        else:
            id = title.get("href").split("/")[-1]
        name = title.get("title")

        if content_type == "youtube#video":
            dur = content.find(class_="accessible-description").text.split(" ")[-1]

            return_items.append({
                    'kind': content_type,
                    'id': id,
                    'title': name,
                    'dur': dur
            })
        else:
            return_items.append({
                    'kind': content_type,
                    'id': id,
                    'title': name
            })

    return return_items