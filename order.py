# Monyemoratho Breyden
class Order(object):
    """ 
   

	side, specifies whatever the order is a BUY or SELL order.
	price, specifies the price to which the order could be sold if a SELL order or bought if a BUY order.
	size, specifies the amount of units to be sold or bought.
	order_id, unique identification of the order .

  
    """
    def __init__(self, side, price, size,order_id, timestamp=None):
        self.side = side
        self.price = price
        self.size = size
        self.timestamp = timestamp
        self.order_id = order_id

    def __repr__(self):
        return '{0} {1} units at {2}'.format(self.side, self.size, self.price)
    def getID(self):
        return self.order_id
