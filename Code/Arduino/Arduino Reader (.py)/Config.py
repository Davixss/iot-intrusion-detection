# Client MQTT configuration

class Config:
    # Config AWS
    endpoint = "apv9omwb522qd-ats.iot.eu-central-1.amazonaws.com"
    client_id = "ArduinoUnoR3"
    root_ca = "keys/AWS-Root-RSA.pem"
    private_key = "keys/AWS-private.pem.key"
    certificate = "keys/AWS-certificate.pem.crt"

    # Config InfluxDB
    token_influx = "H4cem9xbCj-7rT165wBxmHEDNebCg2Fq1bZ0LGY9cDlGGSP7zwKsTsEeb8Em7eNcPX6RD6VdgqXU9dwUCnx3-Q=="
    org_influx = "University of Messina"
    host_influx = "https://eu-central-1-1.aws.cloud2.influxdata.com"
    bucket = "ArduinoData"

    # Config emails
    emails = ["davide.allegra@studenti.unime.it", "cateno.dali@studenti.unime.it"]
    subject = "Intrusion Notification"
