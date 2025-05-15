from neo4j import GraphDatabase


def get_connection():
    host = input("Enter your host address: ").strip()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    uri = f"bolt://{host}:7687"

    return GraphDatabase.driver(uri, auth=(username, password))


def fetch_first_node(session, label, condition):
    cypher = (
        f"MATCH (node:{label}) WHERE {condition} "
        "RETURN node LIMIT 1"
    )
    record = session.run(cypher).single()

    return record.get("node") if record else None


def main():
    driver = get_connection()
    db = input("Enter your database name: ").strip()
    label = input("Enter your database label: ").strip()
    condition = input("Enter your condition: ").strip()

    with driver.session(database=db) as session:
        node = fetch_first_node(session, label, condition)
        print("Your data is:")

        if node:
            print(" ".join([f"{key}='{value}'" for key, value in node.items()]))

    print("Process finished with exit code 0")


if __name__ == "__main__":
    main()
