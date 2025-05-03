from apify_client import ApifyClient
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LinkedInScraper:
    def __init__(self):
        self.client = ApifyClient(os.getenv('APIFY_API_KEY'))

    async def search_person(self, name: str, company: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for a person on LinkedIn using Apify's LinkedIn Profile Scraper
        """
        run_input = {
            "searchTerms": name,
            "maxProfiles": 1,
            "companyFilter": company if company else "",
            "searchType": "person"
        }

        # Start the actor
        run = self.client.actor("apify/linkedin-profile-scraper").call(run_input=run_input)
        
        # Get the results
        results = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
        
        if not results:
            return {}
            
        return self._process_profile(results[0])

    def _process_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and clean the LinkedIn profile data
        """
        return {
            "name": profile.get("fullName", ""),
            "headline": profile.get("headline", ""),
            "summary": profile.get("summary", ""),
            "experience": [
                {
                    "title": exp.get("title", ""),
                    "company": exp.get("companyName", ""),
                    "duration": exp.get("dateRange", ""),
                    "description": exp.get("description", "")
                }
                for exp in profile.get("experiences", [])
            ],
            "education": [
                {
                    "school": edu.get("schoolName", ""),
                    "degree": edu.get("degreeName", ""),
                    "field": edu.get("fieldOfStudy", ""),
                    "duration": edu.get("dateRange", "")
                }
                for edu in profile.get("education", [])
            ],
            "skills": [skill.get("name", "") for skill in profile.get("skills", [])],
            "languages": [lang.get("name", "") for lang in profile.get("languages", [])],
            "url": profile.get("profileUrl", "")
        }

    async def get_company_info(self, company_name: str) -> Dict[str, Any]:
        """
        Get company information using Apify's LinkedIn Company Scraper
        """
        run_input = {
            "searchTerms": company_name,
            "maxCompanies": 1,
            "searchType": "company"
        }

        # Start the actor
        run = self.client.actor("apify/linkedin-company-scraper").call(run_input=run_input)
        
        # Get the results
        results = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
        
        if not results:
            return {}
            
        return self._process_company(results[0])

    def _process_company(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and clean the company data
        """
        return {
            "name": company.get("name", ""),
            "description": company.get("description", ""),
            "website": company.get("website", ""),
            "industry": company.get("industry", ""),
            "company_size": company.get("companySize", ""),
            "headquarters": company.get("headquarters", ""),
            "founded": company.get("founded", ""),
            "specialties": company.get("specialties", []),
            "url": company.get("linkedinUrl", "")
        } 