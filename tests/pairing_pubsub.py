import shoopack
import time
def test_pairing_pubsub():
    a = shoopack.create_pairing_pubsub("zmq",
                                        target_address="localhost",
                                        target_port=5555,
                                        source_address="localhost",
                                        source_port=5556,
                                        source_timeout=500,
                                        protocol="tcp",
                                        topic_name="test_topic")
    b = shoopack.create_pairing_pubsub("zmq",
                                        target_address="localhost",
                                        target_port=5556,
                                        source_address="localhost",
                                        source_port=5555,
                                        source_timeout=500,
                                        protocol="tcp",
                                        topic_name="test_topic")

    a.listen()
    b.listen()
    i = 0
    # await a, b is listened
    while not (a._listen_loop and b._listen_loop):
        print("Waiting for both A and B to start listening...")
        time.sleep(0.1)

    try:
        while True:
            a.publish({"message": f"Hello from A {i}"})
            b.publish({"message": f"Hello from B {i}"})
            i += 1
            print(f"A gets: {a.get()}")
            print(f"B gets: {b.get()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Test interrupted by user.")
    finally:
        a.close()
        b.close()
        print("Pairing Pub/Sub test completed and resources cleaned up.")

if __name__ == "__main__":
    test_pairing_pubsub()
