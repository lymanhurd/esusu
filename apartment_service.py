from esusu_db import last_row_inserted, create_apartment_db


# Ordinarily I would be using a real ORM, but here I have hacked together a quick and dirty substitute.
class ApartmentService(object):
    def __init__(self, conn):
        self.conn = conn

    @classmethod
    def get_dev_service(cls):
        conn = create_apartment_db(":memory:")
        return cls(conn)

    # Methods implementing Create, Read and Update commands for Apartments, Properties and Tenants
    def add_apartment(self, apartment):
        self.conn.execute(
            'INSERT INTO Apartment (Property_ID, unit) VALUES (:Property_ID, :Unit)', apartment)
        return last_row_inserted(self.conn)

    def add_property(self, property_data):
        self.conn.execute(
            'INSERT INTO Property (Manager_ID, Name, Address) VALUES (:Manager_ID, :Name, :Address)',
            property_data)
        return last_row_inserted(self.conn)

    def add_tenant(self, tenant):
        self.conn.execute(
            'INSERT INTO Tenant (Apartment_ID, Name, DateOfBirth, EncryptedSSN, IsPrimary) '
            'VALUES (:Apartment_ID, :Name, :DateOfBirth, :EncryptedSSN, :IsPrimary)',
            tenant)
        return last_row_inserted(self.conn)

    def get_apartment(self, apartment_id):
        res = self.conn.execute("SELECT * FROM Apartment WHERE Apartment_ID=:Apartment_ID",
                                {"Apartment_ID": apartment_id})
        row = res.fetchone()
        return {"Apartment_ID": row[0], "Property_ID": row[1], "Unit": row[2]}

    def get_property(self, property_id):
        res = self.conn.execute("SELECT * FROM Property WHERE Property_ID=:Property_ID",
                                {"Property_ID": property_id})
        row = res.fetchone()
        return {"Property_ID": row[0], "Manager_ID": row[1], "Name": row[2], "Address": row[3]}

    def get_tenant(self, tenant_id):
        res = self.conn.execute("SELECT * FROM Tenant WHERE Tenant_ID=:Tenant_ID", {"Tenant_ID": tenant_id})
        row = res.fetchone()
        return {"Tenant_ID": row[0], "Apartment_ID": row[1], "Name": row[2], "DateOfBirth": row[3],
                "EncryptedSSN": row[4], "IsPrimary": row[5]}

    def update_apartment(self, apartment):
        self.conn.execute(
            'UPDATE Apartment SET Property_ID=:Property_ID, Unit=:Unit WHERE '
            'Apartment_ID = :Apartment_ID', apartment)

    def update_property(self, property_data):
        self.conn.execute(
            'UPDATE Property SET Manager_ID=:Manager_ID, Name=:Name, '
            'Address=:Address WHERE Property_ID = :Property_ID', property_data)

    def update_tenant(self, tenant):
        self.conn.execute(
            'UPDATE Tenant SET Apartment_ID=:Apartment_ID, Name=:Name, DateOfBirth=:DateOfBirth, '
            'EncryptedSSN=:EncryptedSSN, IsPrimary=:IsPrimary WHERE ' 
            'Tenant_ID = :Tenant_ID', tenant)
