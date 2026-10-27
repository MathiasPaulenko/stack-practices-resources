# acl/database_acl.py — translate legacy database tables to domain repositories
from typing import Optional, List
from domain.customer import Customer, CustomerStatus, CustomerRepository

class LegacyCustomerRepository(CustomerRepository):
    """Implements the domain repository interface using legacy tables.
    The domain sees a clean repository; this class does the translation."""

    def __init__(self, db_connection):
        self._db = db_connection

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        # Query legacy table with legacy column names
        row = self._db.execute_one(
            "SELECT cust_id, email_addr, first_nm, last_nm, stat_cd, create_dt "
            "FROM LEGACY.CUSTOMERS WHERE cust_id = :id",
            {"id": customer_id}
        )
        if row is None:
            return None

        # Translate legacy row to domain entity
        status_map = {"1": "active", "2": "suspended", "3": "churned"}
        return Customer(
            id=row["cust_id"],
            email=row["email_addr"].lower(),
            full_name=f"{row['first_nm']} {row['last_nm']}".strip(),
            status=CustomerStatus(status_map.get(row["stat_cd"], "active")),
            created_at=str(row["create_dt"])
        )

    def save(self, customer: Customer) -> Customer:
        # Translate domain entity to legacy columns
        parts = customer.full_name.split(" ", 1)
        status_map = {"active": "1", "suspended": "2", "churned": "3"}

        self._db.execute(
            "MERGE INTO LEGACY.CUSTOMERS "
            "USING (SELECT :id AS cust_id FROM dual) src "
            "ON (CUSTOMERS.cust_id = src.cust_id) "
            "WHEN MATCHED THEN UPDATE SET "
            "  email_addr = :email, first_nm = :first, last_nm = :last, stat_cd = :status "
            "WHEN NOT MATCHED THEN INSERT "
            "  (cust_id, email_addr, first_nm, last_nm, stat_cd, create_dt) "
            "  VALUES (:id, :email, :first, :last, :status, SYSDATE)",
            {
                "id": customer.id,
                "email": customer.email,
                "first": parts[0],
                "last": parts[1] if len(parts) > 1 else "",
                "status": status_map.get(customer.status.value, "1")
            }
        )
        return self.find_by_id(customer.id)

    def find_by_status(self, status: CustomerStatus) -> List[Customer]:
        status_map = {"active": "1", "suspended": "2", "churned": "3"}
        rows = self._db.execute_all(
            "SELECT cust_id, email_addr, first_nm, last_nm, stat_cd, create_dt "
            "FROM LEGACY.CUSTOMERS WHERE stat_cd = :status",
            {"status": status_map.get(status.value, "1")}
        )
        return [self._row_to_customer(row) for row in rows]
