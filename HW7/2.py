from neo4j import GraphDatabase


def get_connection():
    host = input("Enter your host address: ").strip()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    uri = f"bolt://{host}:7687"

    return GraphDatabase.driver(uri, auth=(username, password))


def fetch_gender_ratio(session, label):
    cypher = (
        f"MATCH (node:{label}) "
        "WITH count(CASE WHEN node.gender = '1' THEN 1 END) AS female, "
        "     count(CASE WHEN node.gender = '0' THEN 1 END) AS male "
        "RETURN toFloat(female) / male AS ratio"
    )
    result = session.run(cypher)

    return result.single().get("ratio")


def main():
    driver = get_connection()
    db = input("Enter your database name: ").strip()
    label = input("Enter your database label: ").strip()

    with driver.session(database=db) as session:
        ratio = fetch_gender_ratio(session, label)
        print(f"Relationship men to woman is: {ratio}")

    print("Process finished with exit code 0.")


if __name__ == "__main__":
    main()
