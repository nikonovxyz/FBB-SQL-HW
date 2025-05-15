import json
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint


def main():
    host = input("Enter MongoDB host address: ").strip()
    client = MongoClient(host)
    db = client["test"]
    collection = db["docs"]

    while True:
        choice = input("1 - Insert, 2 - Search document, 3 - Change collection, 0 - Exit: ").strip()

        if choice == "0":
            print("Process finished with exit code 0.")
            break

        elif choice == "1":
            while True:
                filename = input("Enter file name (or press Enter to stop): ").strip()

                if not filename:
                    break

                if not os.path.isfile(filename):
                    print(f"File '{filename}' not found.")
                    continue

                link_id = input("Enter linked document ID (or press Enter to skip): ").strip()

                with open(filename) as infile:
                    doc = json.load(infile)

                if link_id:
                    try:
                        _ = ObjectId(link_id)
                        doc["link_doc_id"] = link_id
                    except Exception:
                        print("Invalid related document ID format; skipping link.")

                result = collection.insert_one(doc)
                print(f"Document added to MongoDB with ID: {result.inserted_id}")

        elif choice == "2":
            key = input("Enter search key: ").strip()
            value = input("Enter search value: ").strip()
            query = {key: value}

            for doc in collection.find(query):
                print("Document retrieved from MongoDB:")
                pprint(doc)

        elif choice == "3":
            name = input("Enter new collection name: ").strip()
            collection = db[name]

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
