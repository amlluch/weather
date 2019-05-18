# -*- coding: utf-8 -*-

# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from core.models import DataWeather, Station


class MeteoPipeline(object):

    def process_item(self, item, spider):

        station = Station.objects.filter(latlon=item['latlon']).first()
        if not station:
            station = Station.objects.create(
                latlon=item['latlon'],
                region=item['region'],
                province=item['province'],
                locality=item['locality'],
                altitude=item['altitude']
            )

        try:
            DataWeather.objects.create(
                station=station,
                unique_id=str(station.pk) + item['timestamp'],  # avoids duplicated data
                timestamp=item['timestamp'],
                temperature=item['temp'],
                humidity=item['humidity'],
                wind_address=item['wind_address'],
                wind_speed=item['wind_speed'],
                pressure=item['pressure'],
                sun=item['sun'],
                rain=item['rain'],
            )
        except Exception:
            pass

        return item
