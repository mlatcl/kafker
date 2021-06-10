import faust

app = faust.App(
    "kafker",
    version=1,
    autodiscover=True,
    origin="kafker",
    broker="kafka://localhost:9092",
)


def main():
    app.main()
