import faust

address = 'bravenw.info'
brokerAddress = "kafka://{}:9092".format(address)
print("Broker address: ", brokerAddress)
app = faust.App(
    "kafker",
    version=1,
    autodiscover=True,
    origin="kafker",
    broker=brokerAddress
)


def main():
    app.main()
