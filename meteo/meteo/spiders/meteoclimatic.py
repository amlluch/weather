# -*- coding: utf-8 -*-
import scrapy
from ..items import MeteoItem
import datetime


class MeteoSpider(scrapy.Spider):
    name = 'meteoclimatic'
    allowed_domains = ['meteoclimatic.net']
    start_urls = ['https://www.meteoclimatic.net/',]

    def parse(self, response):

        hrefs = response.xpath('//fieldset[@id="stlist"]/a/@href').getall()
        names = response.xpath('//fieldset[@id="stlist"]/a/text()').getall()

        if hrefs:
            for href, name in zip(hrefs, names):
                request = response.follow(href, callback=self.parse_next)
                request.meta['region'] = name
                yield request

    def parse_next(self, response):

        links = response.xpath('//a[contains(@href, "/perfil/")]/@href').extract()
        if links is not None:
            for link in links:
                request = response.follow(link, callback=self.parse_temp)
                request.meta['region'] = response.meta['region']
                yield request

    def parse_temp(self, response):
        est_datos = response.xpath('//*[@class="est_dades"]/text()').extract()
        datos_generales = response.xpath('//*[@class="titolseccio"]/text()').extract()
        titulos = response.xpath('//*[@class="titolet"]/text()').extract()
        datos = response.xpath('//*[@class="dadesactuals"]/text()').extract()

        position_raw = est_datos[0]
        position = position_raw.replace('º', ' ').replace("'", " ").replace('&nbsp', ' ').replace('°', ' ')
        pos = " ".join(position.split()).split()

        lat = pos[0] + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3]
        lon = pos[4] + ' ' + pos[5] + ' ' + pos[6] + ' ' + pos[7]
        altitud = position_raw.split()[-2]
        localidad = datos_generales[0]
        hora_raw = datos_generales[1][37:].strip()
        temperatura = humedad = wind = pressure = sunny = rain = wind_address = None

        for titulo, dato in zip(titulos, datos):
            if titulo == 'Temperatura':
                temperatura = float(dato.split()[0].strip())
            if titulo == 'Humedad':
                humedad = float(dato.split()[0].strip())
            if titulo == 'Viento':
                wind_address = dato.split()[0]
                wind = float(dato.split()[1])
            if titulo == 'Presión':
                pressure = int(dato.split()[0])
            if titulo == 'Radiación solar':
                sunny = float(dato.split()[0])
            if titulo == 'Precip.':
                rain = float(dato.split()[0])
        if datos:
            item = MeteoItem()

            item['latlon'] = self._degree_to_float(lat) + ',' + self._degree_to_float(lon)
            item['region'] = response.meta['region']
            item['province'] = est_datos[1].split(',')[1].strip()
            item['locality'] = localidad
            item['altitude'] = int(altitud)
            item['timestamp'] = datetime.datetime.strptime(hora_raw, '%d-%m-%Y %H:%M UTC').strftime('%Y-%m-%d %H:%M')
            item['temp'] = temperatura
            item['humidity'] = humedad
            item['wind_address'] = wind_address
            item['wind_speed'] = wind
            item['pressure'] = pressure
            item['sun'] = sunny
            item['rain'] = rain

            yield item

    @staticmethod
    def _degree_to_float(singlepoint):
        sp = singlepoint.split()
        dd = float(sp[0]) + float(sp[1])/60 + float(sp[2]) / (60*60)
        if sp[3] in ['S', 'W']:
            dd *= -1
        return f'{dd:.15f}'

