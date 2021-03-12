import a1chemy.data_source as data_source
from a1chemy.common import Tag

import pandas as pd


class TradingViewClient(object):

    def __init__(self) -> None:
        super().__init__()
        self.mongo_ticks_client = data_source.ticks_client()
        self.mongo_tag_client = data_source.tags_client()

    def update_sectors(self, path):
        sector_data_frame = pd.read_csv(path)
        sectors_root_tag = Tag(id='tradingview_sectors',
                               parent=None, values={})
        self.mongo_tag_client.delete_by_parent(parent=sectors_root_tag.id)
        trading_view_tree = self.mongo_tag_client.tree(id=sectors_root_tag.id)
        for sectors, stocks in trading_view_tree.root.children.items():
            for key, value in stocks.children.items():
                self.mongo_tag_client.delete_by_parent(key)
        self.mongo_tag_client.insert(tag=sectors_root_tag)
        for index, row in sector_data_frame.iterrows():
            exchange = 'SZ' if row['Exchange'] == 'SZSE' else 'SH'
            symbol = exchange + '{:06d}'.format(row['Ticker'])
            sector = row['Sector']

            sector_tag = Tag(id=sector, parent=sectors_root_tag.id, values={})
            self.mongo_tag_client.insert(tag=sector_tag)

            id = exchange + '_' + symbol
            parent = sector_tag.id
            values = {'exchange': exchange, 'symbol': symbol}
            stock_tag = Tag(id=id, parent=parent, values=values)
            self.mongo_tag_client.insert(tag=stock_tag)
