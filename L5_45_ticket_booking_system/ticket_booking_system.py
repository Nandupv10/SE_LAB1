
"""Movie theater ticket booking and seating management module."""

import hashlib
import secrets
from pathlib import Path

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat and record the booking."""
    if order_history is None:
        order_history = []

    seat = THEATER_SEATS.get(seat_id)
    if seat is None or seat["is_sold"]:
        return False

    seat["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a booking if the specified seat exists."""
    seat = THEATER_SEATS.get(seat_id)
    if seat is None:
        return False

    seat["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True if a seat exists and is available."""
    seat = THEATER_SEATS.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Calculate a seat's price after a valid percentage discount."""
    seat = THEATER_SEATS.get(seat_id)
    if seat is None:
        raise ValueError(f"Unknown seat ID: {seat_id}")

    if not isinstance(discount_rate, (int, float)):
        raise TypeError("Discount rate must be numeric.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    return round(seat["price"] * (1 - discount_rate), 2)


def generate_ticket_hash(ticket_code):
    """Generate a SHA-256 hash for a ticket code."""
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a cryptographically secure four-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Export the current seating information to a text file."""
    output_path = Path(filename)
    output_path.write_text(
        str(THEATER_SEATS) + "\n",
        encoding="utf-8",
    )
    print(f"Seating chart exported to: {output_path}")


def get_theater_summary():
    """Return the number of seats currently sold."""
    return sum(
        seat["is_sold"] for seat in THEATER_SEATS.values()
    )


def main():
    """Demonstrate the ticket booking system."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")

    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())

    export_seating_chart()
    print("Sold count:", get_theater_summary())


if __name__ == "__main__":
    main()
