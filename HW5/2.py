import json
import os
from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId


def main():
    host = input("Enter your MongoDB host address: ").strip()
    client = MongoClient(host)
    db = client["test"]
    collection = db.get_collection("docs")

    while True:
        choice = input("1 - Insert, 2 - Get document, 0 - Exit: ").strip()

        if choice == "0":
            print("Process finished with exit code 0.")
            break

        elif choice == "1":
            filename = input("Enter file name: ").strip()

            if not os.path.isfile(filename):
                print(f"File '{filename}' not found.")
                continue

            with open(filename) as infile:
                doc = json.load(infile)

            result = collection.insert_one(doc)
            print(f"Document added to MongoDB with ID: {result.inserted_id}")

        elif choice == "2":
            id_str = input("Enter document id: ").strip()

            try:
                oid = ObjectId(id_str)
            except Exception:
                print("Invalid ObjectId format.")
                continue

            doc = collection.find_one({"_id": oid})

            if doc:
                print("Document retrieved from MongoDB:")
                pprint(doc)
            else:
                print("No document found with that ID.")
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
