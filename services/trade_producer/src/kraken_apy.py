import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    URL = 'wss://ws.kraken.com/v2'

    def __init__(
        self,
        product_id: str,
    ):
        self.product_id = product_id

        # establish a connection to the Kraken Websocket Trade API
        self._ws = create_connection(self.URL)
        logger.info('Connected to Kraken Websocket Trade')

        # Subscribe to the trade channel
        self.subscribe(product_id=self.product_id)

    def subscribe(self, product_id: str):
        """
        Subscribe to the Kraken Websocket Trade API
        """

        logger.info(f'Subscribing to {product_id} trades')

        # Subscribe to the trade channel
        msg = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade',
                'symbol': [
                    product_id,
                ],
                'snapshot': False,
            },
        }
        self._ws.send(json.dumps(msg))
        logger.info('Subscription worked')

        # Skip the first two messages, because they are not trade events
        _ = self._ws.recv()
        _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:
        # mock_trades = [
        #     {
        #         "product_id": "BTC-USD",
        #         "price": 10000,
        #         "volume": 0.1,
        #         "time": 1630000000
        #     },
        #     {
        #         "product_id": "BTC-USD",
        #         "price": 59000,
        #         "volume": 0.1,
        #         "time": 1640000000
        #     }
        # ]

        message = self._ws.recv()

        if 'heartbeat' in message:
            return []

        # parse the message string to a dictionary
        message = json.loads(message)

        trades = []
        # extract the trade data from the message
        for trade in message['data']:
            trades.append(
                {
                    'product_id': self.product_id,
                    'price': trade['price'],
                    'volume': trade['qty'],
                    'timestamp': trade['timestamp'],
                }
            )

        return trades
