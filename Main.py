# Monyemoratho Bredyen
import xml.etree.ElementTree as ET
from orders import  OrderBook
from order import Order
from Side import Side
import queue



booksDict = {} 
tree = ET.parse('orders.xml') # Use The ElementTree XML API module  API for parsing XML data.

root = tree.getroot()
for child in root:
    if (child.tag==("AddOrder")):
           
           bookID=child.get('book')
           if bookID in booksDict:   
               #print('book already exist'+bookID)
               ob= booksDict.get(bookID)
               operation=child.get('operation')
               if (operation=="SELL"):
                   order = Order(Side.SELL,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   ob.unprocessed_orders.put(order)
               else:
                   order = Order(Side.BUY,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   ob.unprocessed_orders.put(order)
           else:
               
               ob = OrderBook()
               booksDict[bookID]=ob
            #    print(child.tag, child.attrib)
               
               operation=child.get('operation')
               if (operation=="SELL"):
                   order = Order(Side.SELL,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   ob.unprocessed_orders.put(order)
               else:
                   order = Order(Side.BUY,child.get('price') ,int(child.get('volume')),int(child.get('orderId')))
                   ob.unprocessed_orders.put(order)
    else:
        
        # <DeleteOrder book="book-2" orderId="125" />
        bookID=child.get('book')
        orderId=child.get('orderId')
        ob= booksDict.get(bookID)
        # create a new copy of the queue
        temp = queue.Queue()
        while not ob.unprocessed_orders.empty():
            order=ob.unprocessed_orders.get()
            if not (order.getID()==int(orderId)): # if not the order to be deleted
                temp.put(order)
            
        ob.unprocessed_orders=temp
               


       


# #  iterate through the books, process and show the books

 
for bookID in booksDict :
    ob=booksDict[bookID]
    while not ob.unprocessed_orders.empty():

        ob.process_order(ob.unprocessed_orders.get())
    print('book: '+bookID)
    
   
    ob.show_book()
    
