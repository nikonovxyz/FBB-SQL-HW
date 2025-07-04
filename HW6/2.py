import redis


def main():
    host = input("Enter your host address: ").strip()
    port = int(input("Enter your port: ").strip())
    r = redis.Redis(host=host, port=port, decode_responses=True)

    while True:
        choice = input("1 - Set key and value, 2 - Get value by key, 0 - Exit: ").strip()

        if choice == "0":
            print("Process finished with exit code 0.")
            break

        elif choice == "1":
            key = input("Key: ").strip()
            value = input("value: ").strip()
            storage_time = input("Storage time in seconds, nothing for endless: ").strip()

            if storage_time:
                try:
                    r.set(key, value, ex=int(storage_time))
                except valueError:
                    r.set(key, value)

            else:
                r.set(key, value)

        elif choice == "2":
            key = input("Key: ").strip()
            value = r.get(key)
            print(f"Your value is: {value}")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
