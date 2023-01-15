from datetime import date
from esusu_db import last_row_inserted, create_payment_db


class PaymentService(object):
    def __init__(self, conn):
        self.conn = conn

    @classmethod
    def get_dev_service(cls):
        conn = create_payment_db(":memory:")
        return cls(conn)

    # Methods implementing payments
    def add_payment(self, tenant_id, amount, date_str):
        if amount <= 0:
            raise ValueError(f"Amount {amount} must be a positive number")
        payment_amount = round(amount * 100)  # express in an integral number of cents
        payment_date = date.fromisoformat(date_str)
        if payment_date > date.today():
            raise ValueError(f"Date {date_str} must occur in the past")
        self.conn.execute(
            'INSERT INTO Payment (Tenant_ID, Year, Month, Day, Amount) '
            'VALUES (:Tenant_ID, :Year, :Month, :Day, :Amount)',
            {"Tenant_ID": tenant_id, "Year": payment_date.year, "Month": payment_date.month, "Day": payment_date.day,
             "Amount": payment_amount})
        return last_row_inserted(self.conn)

    def get_payment(self, payment_id):
        res = self.conn.execute("SELECT * FROM Payment WHERE Payment_ID=:Payment_ID",
                                {"Payment_ID": payment_id})
        row = res.fetchone()
        return {"Payment_ID": row[0], "Tenant_ID": row[1], "Year": row[2], "Month": row[3], "Day": row[4],
                "Amount": row[5]}

    def get_payment_history(self, tenant_id):
        res = []
        for row in self.conn.execute("SELECT SUM(Amount), Year, Month, MIN(Day) FROM Payment "
                                     "WHERE Tenant_ID=:Tenant_ID GROUP BY Year, Month ORDER BY Year, Month",
                                     {"Tenant_ID": tenant_id}):
            res.append((row[0] / 100, date(row[1], row[2], row[3]).isoformat()))
        return res
