import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My script with default arguments")
    parser.add_argument("-n", default=10, help="Loop size")
    n = parser.parse_args().n
    print("n:", n)

    for i in range(int(n)):
        print("This is step {}.".format(i), flush=True)
        time.sleep(1)
    print("Script has ended!")