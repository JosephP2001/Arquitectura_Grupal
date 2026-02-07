from src.infrastructure.database.mongo_client import mongo_db

class ReportDAOMongo:

    def __init__(self):
        self.db = mongo_db.get_database()
        self.collection = self.db["reports"]

    def create(self, report: dict):
        return self.collection.insert_one(report)

    def get_by_patient(self, patient_id: str):
        return list(self.collection.find({"patient_id": patient_id}))
