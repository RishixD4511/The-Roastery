import mysql.connector

con = mysql.connector.connect(
    host="localhost", user="root", passwd="your_password", database="roastery_db"
)
cur = con.cursor()

while True:
  print("\n============================================")
  print("   COFFEE ROASTERY & WHOLESALE SYSTEM")
  print("============================================")
  print("1. View All Coffee Batches")
  print("2. Place New Wholesale Order")
  print("3. View All Wholesale Orders")
  print("4. Restock Coffee Batch (Add kg)")
  print("5. Cancel an Order")
  print("6. Exit")

  ch = int(input("\nEnter your choice (1-6): "))

  if ch == 1:
    print("\n--- AVAILABLE COFFEE BATCHES ---")
    cur.execute("SELECT * FROM batches")
    data = cur.fetchall()
    for row in data:
      print(
          "Batch ID:",
          row[0],
          "| Estate:",
          row[1],
          "| Process:",
          row[2],
          "| Roast:",
          row[3],
          "| Stock:",
          row[4],
          "kg | Price: Rs.",
          row[5],
      )

  elif ch == 2:
    o_id = int(input("Enter New Order ID (e.g. 505): "))
    b_id = int(input("Enter Batch ID to buy (101-105): "))
    cafe = input("Enter Buyer Cafe Name: ")
    kg = int(input("Enter Quantity in kg: "))
    rate = int(input("Enter Price per kg of that Batch: "))

    gross = kg * rate
    if kg >= 25:
      disc = gross * 0.15
    elif kg >= 10:
      disc = gross * 0.10
    else:
      disc = 0

    final_bill = gross - disc

    q1 = "INSERT INTO orders VALUES ({}, {}, '{}', {}, {}, {})".format(
        o_id, b_id, cafe, kg, disc, final_bill
    )
    cur.execute(q1)

    q2 = "UPDATE batches SET stock_kg = stock_kg - {} WHERE batch_id = {}".format(
        kg, b_id
    )
    cur.execute(q2)
    con.commit()

    print("\n--- WHOLESALE BILL GENERATED ---")
    print("Cafe Name     :", cafe)
    print("Gross Amount  : Rs.", gross)
    print("Bulk Discount : Rs.", disc)
    print("Final Bill    : Rs.", final_bill)

  elif ch == 3:
    print("\n--- ALL WHOLESALE ORDERS ---")
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()
    for row in data:
      print(
          "Order ID:",
          row[0],
          "| Batch ID:",
          row[1],
          "| Cafe:",
          row[2],
          "| Qty:",
          row[3],
          "kg | Discount: Rs.",
          row[4],
          "| Total: Rs.",
          row[5],
      )

  elif ch == 4:
    b_id = int(input("Enter Batch ID to restock: "))
    add_kg = int(input("Enter newly roasted kg to add: "))

    q = "UPDATE batches SET stock_kg = stock_kg + {} WHERE batch_id = {}".format(
        add_kg, b_id
    )
    cur.execute(q)
    con.commit()
    print("Stock updated successfully!")

  elif ch == 5:
    o_id = int(input("Enter Order ID to cancel: "))

    q = "DELETE FROM orders WHERE order_id = {}".format(o_id)
    cur.execute(q)
    con.commit()
    print("Order cancelled and deleted from records!")

  elif ch == 6:
    print("Thank you! Closing system.")
    break

  else:
    print("Invalid choice! Please enter 1 to 6.")
