import redis


def main():
    host = input("Enter your host address: ").strip()
    port = int(input("Enter your port: ").strip())
    r = redis.Redis(host=host, port=port, decode_responses=True)

    while True:
        choice = input("1 - Add to list, 2 - Delete from list, 0 - Exit: ").strip()

        if choice == "0":
            print("Process finished with exit code 0.")
            break

        elif choice == "1":
            lst = input("List name: ").strip()
            vals = input("Values with ',': ").strip().split(',')
            direction = input("1 - Right, 2 - Left, other - Exit: ").strip()

            if direction == "1":
                for v in vals:
                    r.rpush(lst, v)

            elif direction == "2":
                for v in vals:
                    r.lpush(lst, v)

            else:
                continue

            print(f"List after: {r.lrange(lst, 0, -1)}")

        elif choice == "2":
            lst = input("List name: ").strip()
            before = r.lrange(lst, 0, -1)
            print(f"List before: {before}")

            direction = input("1 - Right, 2 - Left, other - Exit: ").strip()

            if direction == "1":
                r.rpop(lst)
            elif direction == "2":
                r.lpop(lst)
            else:
                continue
            print(f"List after: {r.lrange(lst, 0, -1)}")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
