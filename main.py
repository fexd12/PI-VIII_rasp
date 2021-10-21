from pubsub import PubSub

def main():
    publisher = PubSub('projects/southern-waters-328922/topics/Sensor')

    # stub = publisher.create_pubsub_stub()
    message = {"valor":"gabriel23","tipo_sensor":"camera23"}
    publisher.publish_message(message)

if __name__ == '__main__':
    main()