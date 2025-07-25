# Applyfy

**Applyfy** is an automated job digest generator. It fetches job listings (e.g., from LinkedIn), parses them from CSV, and generates a professional HTML digest suitable for email delivery.

## 🚀 Features
- Parses raw CSV job data from APIs
- Generates clean HTML job summaries
- Sends job digests via email
- Fully Dockerized for easy deployment

## 📦 Requirements
- Docker & Docker Compose

## 🛠 Getting Started

First, pull the latest applyfy container using docker compose:

```yaml
services:

  applyfy:
    image: techblog/applyfy
    container_name: applyfy
    restart: always
    networks:
     - infrastructure
    ports:
      - "8111:80"
```

And run the following command to run it:
```bash
sudo docker-compose up -d
```

Create a new n8n workflow, and paste the following json in the canvas:

```json
{
  "name": "Job Finder",
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        -520,
        -160
      ],
      "id": "de683bec-3fa0-4cb4-b45f-b39dbe04ad35",
      "name": "When clicking ‘Test workflow’"
    },
    {
      "parameters": {
        "fromEmail": "example@gmail.com",
        "toEmail": "example@gmail.com",
        "subject": "=📌 Top Job Opportunities — Updated  {{ $json.subjectDate }}",
        "html": "={{ $json.html }}",
        "options": {}
      },
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2.1,
      "position": [
        120,
        -160
      ],
      "id": "ea44caab-4042-4716-a05f-56dc401d3a50",
      "name": "Send Email",
      "webhookId": "9e8056a2-ee4b-44ed-b568-a92e3b503d87",
      "credentials": {
        "smtp": {
          "id": "cTa1cY2qr9SqODB0",
          "name": "Gmail account"
        }
      }
    },
    {
      "parameters": {
        "url": "[server_url]/scrape_jobs",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {
              "name": "search_term",
              "value": "Senior Devops"
            },
            {
              "name": "location",
              "value": "Raanana, Israel"
            },
            {
              "name": "results_wanted",
              "value": "40"
            },
            {
              "name": "hours_old",
              "value": "72"
            },
            {
              "name": "country_indeed",
              "value": "ISRAEL"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        -300,
        -160
      ],
      "id": "0dab0f2b-f187-43d1-aa06-5070b7de7348",
      "name": "Search for open jobs"
    },
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "weeks"
            }
          ]
        }
      },
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [
        -540,
        60
      ],
      "id": "7e652305-fde8-467a-b202-0d535dfc9a8e",
      "name": "Schedule Trigger"
    },
    {
      "parameters": {
        "jsCode": "const rawCsv = items[0].json.data;\n\n// Parse CSV\nconst lines = rawCsv.trim().split('\\n');\nconst headers = lines[0].replace(/^\"|\"$/g, '').split('\",\"');\nconst jobs = lines.slice(1).map(line => {\n  const cols = line.replace(/^\"|\"$/g, '').split('\",\"');\n  const obj = {};\n  headers.forEach((h, i) => obj[h] = cols[i] || '');\n  return obj;\n});\n\n// Friendly title date\nconst options = { year: 'numeric', month: 'long', day: 'numeric' };\nconst currentDate = new Date().toLocaleDateString('en-US', options);\n\n// Build job rows\nconst htmlRows = jobs.map(job => `\n  <tr>\n    <td>${job.company}</td>\n    <td>${job.title}</td>\n    <td>${job.location}</td>\n    <td>${job.date_posted}</td>\n    <td><a href=\"${job.job_url}\" target=\"_blank\">View Job</a></td>\n\n  </tr>\n`).join('');\n\n// Final HTML\nconst html = `\n<html>\n  <head>\n<style>\n  body {\n    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n    background-color: #f7f9fc;\n    color: #333;\n    margin: 0;\n    padding: 0;\n  }\n  .container {\n    max-width: 1200px;\n    margin: auto;\n    background: #ffffff;\n    padding: 30px;\n    border-radius: 10px;\n    box-shadow: 0 2px 12px rgba(0,0,0,0.06);\n  }\n  h2 {\n    text-align: center;\n    color: #1a73e8;\n    margin-top: 0;\n    font-size: 24px;\n  }\n  table {\n    width: 100%;\n    border-collapse: separate;\n    border-spacing: 0;\n    margin-top: 25px;\n    font-size: 14px;\n  }\n  th {\n    background-color: #e6f2ff;\n    color: #333;\n    padding: 14px 12px;\n    border: 1px solid #ccc;\n    text-align: left;\n  }\n  td {\n    padding: 12px;\n    border: 1px solid #ddd;\n    background-color: #fff;\n    vertical-align: top;\n  }\n  tr:hover td {\n    background-color: #f0f8ff;\n  }\n  tr:first-child th:first-child {\n    border-top-left-radius: 8px;\n  }\n  tr:first-child th:last-child {\n    border-top-right-radius: 8px;\n  }\n  tr:last-child td:first-child {\n    border-bottom-left-radius: 8px;\n  }\n  tr:last-child td:last-child {\n    border-bottom-right-radius: 8px;\n  }\n  a {\n    color: #1a73e8;\n    text-decoration: none;\n  }\n  a:hover {\n    text-decoration: underline;\n  }\n  .footer {\n    margin-top: 35px;\n    text-align: center;\n    font-size: 12px;\n    color: #777;\n  }\n</style>\n  </head>\n  <body>\n    <div class=\"container\">\n      <h2>📌 Top Job Opportunities — Updated ${currentDate}</h2>\n      <table>\n        <thead>\n          <tr>\n            <th>Company</th>\n            <th>Title</th>\n            <th>Location</th>\n            <th>Posted</th>\n            <th>Job URL</th>\n\n          </tr>\n        </thead>\n        <tbody>\n          ${htmlRows}\n        </tbody>\n      </table>\n      <div class=\"footer\">\n        This summary was generated automatically. Stay sharp and happy job hunting!\n      </div>\n    </div>\n  </body>\n</html>\n`;\n\n\n// (add to final return)\nreturn [{\n  json: {\n    html: html,\n    subjectDate: currentDate  // ← this is new\n  }\n}];"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -80,
        -160
      ],
      "id": "fa76d1f8-b4a2-4a6d-9a50-1206c0dcd7ee",
      "name": "Code"
    }
  ],
  "pinData": {},
  "connections": {
    "When clicking ‘Test workflow’": {
      "main": [
        [
          {
            "node": "Search for open jobs",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Search for open jobs": {
      "main": [
        [
          {
            "node": "Code",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Search for open jobs",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Code": {
      "main": [
        [
          {
            "node": "Send Email",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "ce8735c2-574e-4802-938a-38d01b827199",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "ee0b1e6cae70ad46e056ec4fd2977de5edc839fb7e2c0e493527d90ecdb65056"
  },
  "id": "oCzjHb3K1XaBGew7",
  "tags": []
}
```
### Edit the folloing parameters in the HTTP node:
* Set the URL to you containr address: *http://server_url/scrape_jobs*
* Set the search_term to you desired job.
* Set the location.
* Set the hours_old to fit you desired posted jobs Date and Time.
* Set the number of results to return.

### Edit the email node:
* Set the *From Email*
* Set the *To Email*
* Set the account credentials.

#### Not that if you would like to use Gmail account, you must activate the 2FA and set app password.

Run the flow and you should get an email looks like the following:
![Email](screenshots/email.png)
