# Monyemoratho Breyden

import threading
import time
import xml.etree.ElementTree as ET
from orders import  OrderBook
from order import Order
from Side import Side
import queue
import threading


start_time = time.time()
tree = ET.parse('orders.xml') # Use The ElementTree XML API module  API for parsing XML data.

root = tree.getroot()
# assuming the are 3 order books
unprocessed_ordersBook1 = []  
unprocessed_ordersBook2 = []
unprocessed_ordersBook3 = []

for child in root:
    bookID=child.get('book')
    if (bookID=="book-1"):
        unprocessed_ordersBook1.append(child)
    elif (bookID=="book-2"):
        unprocessed_ordersBook2.append(child)
    elif (bookID=="book-3"):
        unprocessed_ordersBook3.append(child)
print("--- %s seconds ---" % (time.time() - start_time))

class myThread (threading.Thread):
   def __init__(self, BookID, unprocessed_ordersBook):
      threading.Thread.__init__(self)
      self.BookID = BookID
      self.unprocessedElements= unprocessed_ordersBook
      self.ob = OrderBook()
   def run(self):
       for child in self.unprocessedElements:
           if (child.tag==("AddOrder")):
               operation=child.get('operation')
               if (operation=="SELL"):
                   order = Order(Side.SELL,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   self.ob.unprocessed_orders.put(order)
               else:
                   order = Order(Side.BUY,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   self.ob.unprocessed_orders.put(order)
           else:
               # <DeleteOrder book="book-2" orderId="125" />
               orderId=child.get('orderId')
               # create a new copy of the queue
               temp = queue.Queue()
               while not self.ob.unprocessed_orders.empty():
                   order=self.ob.unprocessed_orders.get()
                   if not (order.getID()==int(orderId)): # if not the order to be deleted
                         temp.put(order)

                       
                   
                     
               self.ob.unprocessed_orders=temp

       while not self.ob.unprocessed_orders.empty():
           self.ob.process_order(self.ob.unprocessed_orders.get())
            
    
        


threads = []

# Create new threads
thread1 = myThread(1, unprocessed_ordersBook1)
thread2 = myThread(2, unprocessed_ordersBook2)
thread3 = myThread(3, unprocessed_ordersBook3)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

# Wait for all threads to complete
for t in threads:
    t.join()
# display a book 
for t in threads:
    t.ob.show_book()
