#! /usr/bin/python

#import libraries required
import urllib, json, smtplib

#Static varibles
url = 'http://127.0.0.1:9200/_cluster/health'
nodeCount = 37
dataNodes = 32
expectedStatus = "green"
issue = False
issuetxt = ""

#Get Data
response = urllib.urlopen(url)
data = json.loads(response.read())

if data["status"] != expectedStatus:
  issue = True
  issuetxt = "Cluster Status : " + data["status"] + " "

if data["number_of_nodes"] != nodeCount:
  issue = True
  issuetxt += "Node Count Mismatch "

if data["initializing_shards"] != 0:
  issuetxt += "Initializing Shards "

if data["unassigned_shards"] != 0:
  issuetxt += "Unassigned Shards "

if data["relocating_shards"] != 0:
  issuetxt += "Relocating Shards "

if issue:

  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText

  # From / To Addresses
  fromEmail = "ElasticCluster@somewhere.com"
  toEmail = "MonirotingTeam@somewhere.com"

  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = "Elastic Cluster Alert: " + issuetxt
  msg['From'] = fromEmail
  msg['To'] = toEmail

  # Create the body of the message (a plain-text and an HTML version).
  text = "Hi!\ncluster Issue Detected?\nGo Have a look\n\n" + issuetxt
  html = str("""\
  <html>
    <body>
      <p><h1> Cluster Issue Detected</h1></p>
      <p><h2>""" + issuetxt + """</p>
      <table border='1' bgcolor='"""+data["status"]+ """' >
        <tr>
          <th>Field</th>
          <th>Status</th>
          <th>Expected</th>
        </tr>
       <tr>
         <td>Status</td>
         <td>""") + str(data["status"]) + str("""</td>
         <td>""") + str(expectedStatus) + str("""</td>
       </tr>
       <tr>
         <td>Cluster Name</td>
         <td>""") + str(data["cluster_name"]) + str("""</td>
         <td>Graylog</td>
       </tr>
       <tr>
         <td>Total Nodes</td>
         <td>""") + str(data["number_of_nodes"]) + str("""</td>
         <td>""") + str(nodeCount) + str("""</td>
       </tr>
       <tr>
         <td>Data Nodes</td>
         <td>""") + str(data["number_of_data_nodes"]) + str("""</td>
         <td>""") + str(dataNodes) + str("""</td>
       </tr>
       <tr>
         <td>Relocating Shards</td>
         <td>""") + str(data["relocating_shards"]) + str("""</td>
         <td>0</td>
       </tr>
       <tr>
         <td>Initializing Shards</td>
         <td>""") + str(data["initializing_shards"]) + str("""</td>
         <td>0</td>
       </tr>
       <tr>
         <td>Unassigned Shards</td>
         <td>""") + str(data["unassigned_shards"]) + str("""</td>
         <td>0</td>
       </tr>
       <tr>
         <td>Active Shards</td>
         <td>""") + str(data["active_shards"]) + str("""</td>
         <td>n/a</td>
       </tr>
    </body>
  </html>""")

  # Record the MIME types of both parts - text/plain and text/html.
  part1 = MIMEText(text, 'plain')
  part2 = MIMEText(html, 'html')
  # Attach parts into message container.
  # According to RFC 2046, the last part of a multipart message, in this case
  # the HTML message, is best and preferred.
  msg.attach(part1)
  msg.attach(part2)

  # Send the message via local SMTP server. Edit to use your SMTP server
  s = smtplib.SMTP('127.0.0.1')
  # sendmail function takes 3 arguments: sender's address, recipient's address
  # and message to send - here it is sent as one string.
  s.sendmail(fromEmail, toEmail, msg.as_string())
  s.quit()

