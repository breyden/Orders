# Monyemoratho Bredyen
import queue
import time
from collections import defaultdict
from order import Order
from Side import Side

def get_timestamp():
    """ return  the number of seconds elapsed since the epoch in Microseconds """
    return int(1e6 * time.time())


class OrderBook(object):
    def __init__(self):
        """ Orders stored as two defaultdicts of {price:[orders at price]}
            Orders sent to OrderBook through OrderBook.unprocessed_orders queue
            Public methods:  process_order(), show_book()
        """
        self.bid_prices = []
        self.bid_sizes = []
        self.offer_prices = []
        self.offer_sizes = []
        self.bids = defaultdict(list)
        self.offers = defaultdict(list)
        self.unprocessed_orders = queue.Queue()
        self.trades = queue.Queue()
        self.order_id = 0

    # def new_order_id(self):
    #     self.order_id += 1
    #     return self.order_id

    @property
    def max_bid(self):
        if self.bids:
            return max(self.bids.keys())
        else:
            return 0.

    @property
    def min_offer(self):
        if self.offers:
            return min(self.offers.keys())
        else:
            return float('inf')

    def process_order(self, incoming_order):
        """ Main processing function. If incoming_order matches delegate to process_match."""
        incoming_order.timestamp = get_timestamp()
       # incoming_order.order_id = self.new_order_id()
        if incoming_order.side == Side.BUY:
            if incoming_order.price >= self.min_offer and self.offers:
                self.process_match(incoming_order)
            else:
                self.bids[incoming_order.price].append(incoming_order)
        else:
            if incoming_order.price <= self.max_bid and self.bids:
                self.process_match(incoming_order)
            else:
                self.offers[incoming_order.price].append(incoming_order)

    def process_match(self, incoming_order):
        """ Match an incoming order against orders on the other side of the book, in price-time priority."""
        levels = self.bids if incoming_order.side == Side.SELL else self.offers
        prices = sorted(levels.keys(), reverse=(incoming_order.side == Side.SELL))
        def price_doesnt_match(book_price):
            if incoming_order.side == Side.BUY:
                return incoming_order.price < book_price
            else:
                return incoming_order.price > book_price
        for (i, price) in enumerate(prices):
            if (incoming_order.size == 0) or (price_doesnt_match(price)):
                break
            orders_at_level = levels[price]
            for (j, book_order) in enumerate(orders_at_level):
                if incoming_order.size == 0:
                    break
                trade = self.execute_match(incoming_order, book_order)
                incoming_order.size = max(0, incoming_order.size-trade.size)
                book_order.size = max(0, book_order.size-trade.size)
                self.trades.put(trade)
            levels[price] = [o for o in orders_at_level if o.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)
        # If the incoming order has not been completely matched, add the remainder to the order book
        if incoming_order.size > 0:
            same_side = self.bids if incoming_order.side == Side.BUY else self.offers
            same_side[incoming_order.price].append(incoming_order)

    def execute_match(self, incoming_order, book_order):
        trade_size = min(incoming_order.size, book_order.size)
        return Trade(incoming_order.side, book_order.price, trade_size, incoming_order.order_id, book_order.order_id)

    def book_summary(self):
        self.bid_prices = sorted(self.bids.keys())
        self.offer_prices = sorted(self.offers.keys())
        self.bid_sizes = [sum(o.size for o in self.bids[p]) for p in self.bid_prices]
        self.offer_sizes = [sum(o.size for o in self.offers[p]) for p in self.offer_prices]

    def show_book(self):
        #4@99,90 -- 29@100,10 
        # print('           {0} -- {1}'.format("BUY", 'SELL'))    
        self.book_summary()
        print('Sell side:')
        if len(self.offer_prices) == 0:
            print('EMPTY')
        for i, price in reversed(list(enumerate(self.offer_prices))):
            print('{0}) Price={1}, Total units={2}'.format(i+1, self.offer_prices[i], self.offer_sizes[i]))
        print('Buy side:')
        if len(self.bid_prices) == 0:
            print('EMPTY')
        for i, price in enumerate(self.bid_prices):
            print('{0}) Price={1}, Total units={2}'.format(i+1, self.bid_prices[i], self.bid_sizes[i]))
        #print()


    
class Trade(object):
    def __init__(self, incoming_side, incoming_price, trade_size, incoming_order_id, book_order_id):
        self.side = incoming_side
        self.price = incoming_price
        self.size = trade_size
        self.incoming_order_id = incoming_order_id
        self.book_order_id = book_order_id

    def __repr__(self):
        return 'Executed: {0} {1} units at {2}'.format(self.side, self.size, self.price)
