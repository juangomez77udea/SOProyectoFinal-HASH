from pymongo import MongoClient
import json
import os

class Database:
    def __init__(self, version):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[f"dataset-{version}"]

    def insert_result(self, algorithm, execution_type, input_type, input_size, metrics):
        collection_name = f"hash_benchmark-{execution_type}_{input_type}_results-{input_size}"
        collection = self.db[collection_name]
        collection.insert_one(metrics)

    def save_to_json(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for collection_name in self.db.list_collection_names():
            file_path = os.path.join(output_dir, f"{collection_name}.json")
            with open(file_path, 'w') as f:
                json.dump(list(self.db[collection_name].find({}, {'_id': 0})), f, indent=2)

    def close(self):
        self.client.close()