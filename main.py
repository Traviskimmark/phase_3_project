import datetime
import sqlite3


conn = sqlite3.connect('train_booking.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        early_bird BOOLEAN NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (train_id) REFERENCES trains (id),
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
''')
conn.commit()


trains = [
    {"id": 1, "name": "Express Train", "departure_time": "08:00 AM"},
    {"id": 2, "name": "Local Train", "departure_time": "09:30 AM"},
]

schedules = [
    {"id": 1, "train_id": 1, "route": "A to B"},
    {"id": 2, "train_id": 2, "route": "X to Y"},
]

def list_trains():
    print("Available Trains:")
    for train in trains:
        print(f"{train['id']}. {train['name']} - Departure Time: {train['departure_time']}")

def list_schedules():
    print("Train Schedules:")
    for schedule in schedules:
        train = next((t for t in trains if t["id"] == schedule["train_id"]), None)
        if train:
            print(f"Schedule ID: {schedule['id']} - Train: {train['name']} - Route: {schedule['route']}")

def book_ticket():
    list_trains()
    train_id = int(input("Enter the ID of the train you want to book a ticket for: "))
    early_bird = False

    current_time = datetime.datetime.now().time()
    if datetime.time(6, 0) <= current_time <= datetime.time(8, 0):
        early_bird = True

    ticket_price = 1000 if early_bird else 2000

    
    name = input("Enter your name: ")
    email = input("Enter your email: ")

   
    cursor.execute("SELECT id FROM customers WHERE email=?", (email,))
    customer = cursor.fetchone()

    if customer is None:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        customer_id = cursor.lastrowid
    else:
        customer_id = customer[0]

   
    cursor.execute("INSERT INTO bookings (train_id, customer_id, early_bird, price) VALUES (?, ?, ?, ?)",
                   (train_id, customer_id, early_bird, ticket_price))
    conn.commit()

    print(f"Ticket booked successfully! {'Early Bird' if early_bird else 'Normal'} Ticket - Price: {ticket_price}")

def update_booking():
   
    email = input("Enter your email to update booking: ")

    cursor.execute("SELECT id FROM customers WHERE email=?", (email,))
    customer = cursor.fetchone()

    if customer is None:
        print("Customer not found. Please check your email.")
        return

    customer_id = customer[0]

    cursor.execute("SELECT b.id, t.name, b.early_bird FROM bookings b JOIN trains t ON b.train_id = t.id WHERE customer_id=?", (customer_id,))
    bookings = cursor.fetchall()

    if not bookings:
        print("You have no bookings.")
        return

    print("Your Bookings:")
    for booking in bookings:
        ticket_type = 'Early Bird' if booking[2] else 'Normal'
        print(f"Booking ID: {booking[0]} - Train: {booking[1]} - Ticket Type: {ticket_type}")

    booking_id = int(input("Enter the ID of the booking you want to update: "))
    new_ticket_type = input("Enter 'E' for Early Bird or 'N' for Normal: ").strip().upper()

    if new_ticket_type == 'E':
        new_early_bird = True
        new_price = 1000
    elif new_ticket_type == 'N':
        new_early_bird = False
        new_price = 2000
    else:
        print("Invalid choice. Booking not updated.")
        return

    cursor.execute("UPDATE bookings SET early_bird=?, price=? WHERE id=?", (new_early_bird, new_price, booking_id))
    conn.commit()
    print("Booking updated successfully!")
def search_tickets():
    train_id = int(input("Enter the ID of the train to search for tickets: "))

    cursor.execute("SELECT name FROM trains WHERE id=?", (train_id,))
    train_name = cursor.fetchone()

    if train_name is None:
        print("Train not found.")
        return

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE train_id=? AND early_bird=?", (train_id, True))
    early_bird_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE train_id=? AND early_bird=?", (train_id, False))
    normal_tickets = cursor.fetchone()[0]

    print(f"Train: {train_name[0]}")
    print(f"Available Early Bird Tickets: {early_bird_tickets}")
    print(f"Available Normal Tickets: {normal_tickets}")

def main():
    while True:
        print("\nTrain Booking System")
        print("1. List Trains")
        print("2. List Schedules")
        print("3. Book Ticket")
        print("4. Update Booking Details")
        print("5. Search Tickets")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_trains()
        elif choice == "2":
            list_schedules()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            update_booking()
        elif choice == "5":
            search_tickets()
        elif choice == "6":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
