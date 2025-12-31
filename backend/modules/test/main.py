import json

# Custom Message
def command(event, message):
  print(json.dumps({ "es-event": event, "es-message": message }))

