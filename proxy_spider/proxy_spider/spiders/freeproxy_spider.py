import base64
import json
import requests
from scrapy import Spider
from datetime import datetime, timezone

total = 150


class FreeproxySpider(Spider):
    name = "freeproxy_spider"
    allowed_domains = ["advanced.name"]
    start_urls = ["https://advanced.name/freeproxy", "https://advanced.name/freeproxy?page=2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxies = []

    def parse(self, response):
        rows_to_take = total - len(self.proxies)
        rows = response.xpath('//*[@id="table_proxies"]/tbody/tr')
        for row in rows[:rows_to_take]:
            ip_encoded = row.xpath('./td[2]/@data-ip').get()
            port_encoded = row.xpath('./td[3]/@data-port').get()
            protocols = row.xpath('./td[4]/a/text()').getall()

            ip = base64.b64decode(ip_encoded).decode('utf-8')
            port = int(base64.b64decode(port_encoded).decode('utf-8'))

            self.proxies.append({
                "ip": ip,
                "port": port,
                "protocols": protocols
            })

    def closed(self, reason):
        with open("proxies.json", "w", encoding="utf-8") as f:
            json.dump(self.proxies, f, ensure_ascii=False, indent=2)

        results = {}
        batch_size = 29
        for i in range(0, len(self.proxies), batch_size):
            proxies_slice = self.proxies[i:i + batch_size]
            proxies_list = list(map(lambda p: f"{p['ip']}:{p['port']}", proxies_slice))
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                "user_id": "t_f5c3f1d8",
                "len": len(proxies_slice),
                "proxies": ', '.join(proxies_list)
            }

            session = requests.Session()
            session.get("https://test-rg8.ddns.net/api/get_token")

            response = session.post("https://test-rg8.ddns.net/api/post_proxies", headers=headers, json=payload)
            if response.ok:
                data = response.json()
                save_id = data['save_id']
                results[save_id] = proxies_list
                print(response.json())
            else:
                print('ERROR', response.status_code, response.text)

        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        finish_time = datetime.now(tz=timezone.utc)
        start_time = self.crawler.stats.get_value("start_time")
        duration = finish_time - start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

        with open("time.txt", "w", encoding="utf-8") as f:
            f.write(time_str)
