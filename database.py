#conexion a momgoDb

from pymongo import MongoClient

class Database:
    def __init__(self, database_name="hash_benchmark"):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[database_name]
        self.parallel_collection = self.db["parallel_results"]
        self.concurrent_collection = self.db["concurrent_results"]

    def insert_result(self, algorithm, execution_type, metrics):
        document = {
            "algorithm": algorithm,
            "time": metrics["time"],
            "memory": metrics["memory"],
            "cpu": metrics["cpu"],
            "disk": metrics["disk"],
            "wait_time": metrics["wait_time"],
            "result": metrics["result"]
        }
        if execution_type == "parallel":
            return self.parallel_collection.insert_one(document)
        elif execution_type == "concurrent":
            return self.concurrent_collection.insert_one(document)

    def get_all_results(self):
        parallel_results = list(self.parallel_collection.find())
        concurrent_results = list(self.concurrent_collection.find())
        return {"parallel": parallel_results, "concurrent": concurrent_results}

    def close(self):
        self.client.close()