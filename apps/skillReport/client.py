import httpx
import json

class SkillReportClient:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_summary(
            self,
            skill_id: int,
            start_date: str,
            end_date: str
    ):
        url = (
            "https://api-na1.niceincontact.com"
            f"/incontactapi/services/v34.0/skills/{skill_id}/summary"
        )

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "startDate": start_date,
            "endDate": end_date
        }

        response = httpx.get(
            url,
            headers=headers,
            params=params,
            timeout=120
        )

        if response.status_code >= 400:
            print(f"Skill ID: {skill_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

        response.raise_for_status()

        return response.json()

    def get_skillData(self, result):
        data = {
            "skillName": result[0]["skillName"],
            "contactsOffered": result[0]["contactsOffered"],
            "contactsQueued": result[0]["contactsQueued"],
            "contactsHandled": result[0]["contactsHandled"]
        }

        return data