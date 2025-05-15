import json
import os
import redis


def main():
    host = input("Enter your host address: ").strip()
    port = int(input("Enter your port: ").strip())
    r = redis.Redis(host=host, port=port, decode_responses=True)

    while True:
        choice = input("1 - Add hash, 2 - Get hash, 0 - Exit: ").strip()

        if choice == "0":
            print("Process finished with exit code 0.")
            break

        elif choice == "1":
            name = input("Enter hash name: ").strip()
            filename = input("Enter file name: ").strip()

            if not os.path.isfile(filename):
                print(f"File '{filename}' not found.")
                continue

            with open(filename) as f:
                data = json.load(f)

            result = r.hset(name, mapping={k: json.dumps(v) if not isinstance(v, str) else v
                                           for k, v in data.items()})
            print(result > 0)

        elif choice == "2":
            name = input("Enter hash name: ").strip()
            h = r.hgetall(name)
            print(f"Your hash is: {h}")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
