import base64
import json
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
        finish_time = datetime.now(tz=timezone.utc)
        start_time = self.crawler.stats.get_value("start_time")
        duration = finish_time - start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

        with open("proxies.json", "w", encoding="utf-8") as f:
            json.dump(self.proxies, f, ensure_ascii=False, indent=2)

        with open("time.txt", "w", encoding="utf-8") as f:
            f.write(time_str)
