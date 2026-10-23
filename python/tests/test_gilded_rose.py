# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
ORDINARY_ITEM = "+5 Dexterity Vest"


def update_item(name, sell_in, quality, days=1):
    item = Item(name, sell_in, quality)
    gilded_rose = GildedRose([item])
    for _ in range(days):
        gilded_rose.update_quality()
    return item


class GildedRoseTest(unittest.TestCase):
    def assert_item(self, item, sell_in, quality):
        self.assertEqual((sell_in, quality), (item.sell_in, item.quality))

    # Ordinary items

    def test_ordinary_item_degrades_by_one_before_sell_by_date(self):
        self.assert_item(update_item(ORDINARY_ITEM, 10, 20), 9, 19)

    def test_ordinary_item_degrades_by_one_on_last_day_before_sell_by_date(self):
        self.assert_item(update_item(ORDINARY_ITEM, 1, 20), 0, 19)

    def test_ordinary_item_degrades_by_two_on_sell_by_date(self):
        self.assert_item(update_item(ORDINARY_ITEM, 0, 20), -1, 18)

    def test_ordinary_item_quality_is_never_negative(self):
        self.assert_item(update_item(ORDINARY_ITEM, 5, 0), 4, 0)

    def test_expired_ordinary_item_with_quality_one_stops_at_zero(self):
        self.assert_item(update_item(ORDINARY_ITEM, 0, 1), -1, 0)

    # Aged Brie

    def test_aged_brie_increases_by_one(self):
        self.assert_item(update_item(AGED_BRIE, 10, 20), 9, 21)

    def test_aged_brie_increases_by_two_after_sell_by_date(self):
        self.assert_item(update_item(AGED_BRIE, 0, 20), -1, 22)

    def test_aged_brie_quality_never_exceeds_fifty(self):
        self.assert_item(update_item(AGED_BRIE, 5, 50), 4, 50)

    def test_expired_aged_brie_at_forty_nine_stops_at_fifty(self):
        self.assert_item(update_item(AGED_BRIE, 0, 49), -1, 50)

    def test_quality_above_fifty_is_not_reduced(self):
        self.assert_item(update_item(AGED_BRIE, 5, 55), 4, 55)

    # Backstage passes

    def test_backstage_passes_increase_by_one_with_eleven_days_left(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 11, 20), 10, 21)

    def test_backstage_passes_increase_by_two_with_ten_days_left(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 10, 20), 9, 22)

    def test_backstage_passes_increase_by_two_with_six_days_left(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 6, 20), 5, 22)

    def test_backstage_passes_increase_by_three_with_five_days_left(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 5, 20), 4, 23)

    def test_backstage_passes_increase_by_three_on_last_day_before_concert(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 1, 20), 0, 23)

    def test_backstage_passes_drop_to_zero_after_concert(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 0, 20), -1, 0)

    def test_backstage_passes_increase_is_capped_at_fifty(self):
        self.assert_item(update_item(BACKSTAGE_PASSES, 5, 48), 4, 50)

    # Sulfuras

    def test_sulfuras_never_changes(self):
        self.assert_item(update_item(SULFURAS, 10, 80), 10, 80)

    def test_sulfuras_past_sell_by_date_never_changes(self):
        self.assert_item(update_item(SULFURAS, -1, 80), -1, 80)

    # Inventory

    def test_every_item_in_inventory_is_updated(self):
        items = [Item(ORDINARY_ITEM, 10, 20), Item(AGED_BRIE, 2, 0)]
        GildedRose(items).update_quality()
        self.assert_item(items[0], 9, 19)
        self.assert_item(items[1], 1, 1)


if __name__ == '__main__':
    unittest.main()
