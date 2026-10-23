# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"

MIN_QUALITY = 0
MAX_QUALITY = 50


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._update_item(item)

    def _update_item(self, item):
        if item.name == SULFURAS:
            return
        self._update_item_quality(item)
        item.sell_in -= 1

    def _update_item_quality(self, item):
        # Quality changes twice as fast once the sell-by date has passed.
        rate = 2 if item.sell_in <= 0 else 1

        if item.name == AGED_BRIE:
            self._increase_quality(item, rate)
        elif item.name == BACKSTAGE_PASSES:
            self._update_backstage_pass_quality(item)
        else:
            self._decrease_quality(item, rate)

    def _update_backstage_pass_quality(self, item):
        if item.sell_in <= 0:
            item.quality = MIN_QUALITY
        elif item.sell_in <= 5:
            self._increase_quality(item, 3)
        elif item.sell_in <= 10:
            self._increase_quality(item, 2)
        else:
            self._increase_quality(item, 1)

    @staticmethod
    def _increase_quality(item, amount):
        if item.quality < MAX_QUALITY:
            item.quality = min(item.quality + amount, MAX_QUALITY)

    @staticmethod
    def _decrease_quality(item, amount):
        if item.quality > MIN_QUALITY:
            item.quality = max(item.quality - amount, MIN_QUALITY)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
