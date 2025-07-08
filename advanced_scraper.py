#!/usr/bin/env python3
"""
Advanced Web Scraper with Selenium and Playwright Support
========================================================

Enhanced scraping capabilities for JavaScript-heavy websites and complex
healthcare startup discovery with browser automation.
"""

import asyncio
import time
import random
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
from datetime import datetime
import json

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# Playwright imports
from playwright.async_api import async_playwright, Browser, Page

# Other imports
from bs4 import BeautifulSoup
from loguru import logger
from fake_useragent import UserAgent

@dataclass
class ScrapingResult:
    """Result from advanced scraping operations."""
    url: str
    title: str
    content: str
    links: List[str]
    metadata: Dict[str, Any]
    timestamp: str

class SeleniumScraper:
    """Selenium-based scraper for JavaScript-heavy websites."""
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.ua = UserAgent()
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        
        # Additional options for better performance
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")  # For faster loading
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            return True
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def close_driver(self):
        """Close the browser driver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None
    
    def scrape_with_selenium(self, url: str) -> Optional[ScrapingResult]:
        """
        Scrape a website using Selenium.
        
        Args:
            url: URL to scrape
            
        Returns:
            ScrapingResult or None if failed
        """
        if not self.setup_driver():
            return None
        
        try:
            logger.info(f"Scraping with Selenium: {url}")
            
            # Navigate to URL
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page content
            title = self.driver.title
            content = self.driver.page_source
            
            # Extract links
            links = []
            try:
                link_elements = self.driver.find_elements(By.TAG_NAME, "a")
                for link in link_elements:
                    href = link.get_attribute("href")
                    if href:
                        links.append(href)
            except Exception as e:
                logger.warning(f"Error extracting links: {e}")
            
            # Extract metadata
            metadata = {
                "url": url,
                "title": title,
                "links_count": len(links),
                "user_agent": self.driver.execute_script("return navigator.userAgent;")
            }
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                links=links,
                metadata=metadata,
                timestamp=datetime.now().isoformat()
            )
            
        except TimeoutException:
            logger.warning(f"Timeout scraping {url}")
            return None
        except WebDriverException as e:
            logger.error(f"WebDriver error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
        finally:
            self.close_driver()

class PlaywrightScraper:
    """Playwright-based scraper for modern web applications."""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser = None
        self.page = None
        self.playwright = None
    
    async def setup_browser(self):
        """Setup Playwright browser."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions"
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Failed to setup Playwright browser: {e}")
            return False
    
    async def close_browser(self):
        """Close the browser."""
        if self.page:
            try:
                await self.page.close()
            except Exception:
                pass
            self.page = None
        
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
            self.browser = None
        
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception:
                pass
            self.playwright = None
    
    async def scrape_with_playwright(self, url: str) -> Optional[ScrapingResult]:
        """
        Scrape a website using Playwright.
        
        Args:
            url: URL to scrape
            
        Returns:
            ScrapingResult or None if failed
        """
        if not await self.setup_browser():
            return None
        
        try:
            logger.info(f"Scraping with Playwright: {url}")
            
            # Create new page
            self.page = await self.browser.new_page()
            
            # Set user agent
            await self.page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            # Navigate to URL
            await self.page.goto(url, wait_until="networkidle", timeout=self.timeout)
            
            # Wait for content to load
            await self.page.wait_for_load_state("domcontentloaded")
            
            # Get page content
            title = await self.page.title()
            content = await self.page.content()
            
            # Extract links
            links = await self.page.eval_on_selector_all(
                "a[href]", "elements => elements.map(el => el.href)"
            )
            
            # Extract metadata
            metadata = {
                "url": url,
                "title": title,
                "links_count": len(links),
                "viewport": await self.page.viewport_size(),
                "user_agent": await self.page.evaluate("navigator.userAgent")
            }
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                links=links,
                metadata=metadata,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error scraping {url} with Playwright: {e}")
            return None
        finally:
            await self.close_browser()

class AdvancedHealthcareScraper:
    """Advanced scraper specifically for healthcare websites."""
    
    def __init__(self):
        self.selenium_scraper = SeleniumScraper()
        self.playwright_scraper = PlaywrightScraper()
        
        # Healthcare-specific websites that require JavaScript
        self.js_heavy_sites = [
            "https://www.crunchbase.com",
            "https://angel.co",
            "https://www.startupblink.com",
            "https://www.pitchbook.com",
            "https://www.linkedin.com/company"
        ]
    
    def needs_javascript(self, url: str) -> bool:
        """Determine if a URL requires JavaScript rendering."""
        domain = urlparse(url).netloc.lower()
        return any(site in url for site in self.js_heavy_sites)
    
    async def scrape_healthcare_site(self, url: str) -> Optional[ScrapingResult]:
        """
        Scrape a healthcare website using appropriate method.
        
        Args:
            url: URL to scrape
            
        Returns:
            ScrapingResult or None if failed
        """
        if self.needs_javascript(url):
            # Try Playwright first (more modern)
            result = await self.playwright_scraper.scrape_with_playwright(url)
            if result:
                return result
            
            # Fallback to Selenium
            return self.selenium_scraper.scrape_with_selenium(url)
        else:
            # Use regular aiohttp for simple sites
            # This would integrate with the main scraper
            logger.info(f"Simple site detected: {url}")
            return None
    
    async def scrape_healthcare_directories(self) -> List[ScrapingResult]:
        """Scrape major healthcare startup directories."""
        directories = [
            "https://www.crunchbase.com/search/organizations/field/organizations/categories/healthcare",
            "https://angel.co/companies?markets[]=Healthcare",
            "https://www.startupblink.com/startups/healthcare",
            "https://www.pitchbook.com/profiles/company-search?filters=industry%3AHealthcare",
            "https://www.linkedin.com/search/results/companies/?keywords=healthcare%20startup"
        ]
        
        results = []
        
        for directory in directories:
            try:
                result = await self.scrape_healthcare_site(directory)
                if result:
                    results.append(result)
                    logger.info(f"Successfully scraped {directory}")
                
                # Rate limiting
                await asyncio.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.error(f"Error scraping directory {directory}: {e}")
        
        return results
    
    def extract_companies_from_result(self, result: ScrapingResult) -> List[Dict[str, str]]:
        """Extract company information from scraping result."""
        companies = []
        
        try:
            soup = BeautifulSoup(result.content, 'html.parser')
            
            # Look for company links and information
            # This is a simplified extraction - in practice, you'd need
            # site-specific selectors for each directory
            
            # Common patterns for company links
            company_selectors = [
                "a[href*='company']",
                "a[href*='startup']",
                ".company-link",
                ".startup-link",
                "[data-company]"
            ]
            
            for selector in company_selectors:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href')
                    text = element.get_text(strip=True)
                    
                    if href and text and len(text) > 2:
                        # Convert to absolute URL
                        if href.startswith('/'):
                            href = urljoin(result.url, href)
                        elif not href.startswith('http'):
                            continue
                        
                        companies.append({
                            'name': text[:100],
                            'url': href,
                            'source': result.url,
                            'extracted_at': result.timestamp
                        })
            
            # Remove duplicates
            seen_urls = set()
            unique_companies = []
            for company in companies:
                if company['url'] not in seen_urls:
                    seen_urls.add(company['url'])
                    unique_companies.append(company)
            
            return unique_companies
            
        except Exception as e:
            logger.error(f"Error extracting companies from {result.url}: {e}")
            return []

async def main():
    """Test the advanced scraper."""
    scraper = AdvancedHealthcareScraper()
    
    # Test with a simple site first
    test_url = "https://www.digital-health-summit.de/"
    
    try:
        result = await scraper.scrape_healthcare_site(test_url)
        if result:
            print(f"Successfully scraped: {result.title}")
            print(f"Found {len(result.links)} links")
            
            # Extract companies
            companies = scraper.extract_companies_from_result(result)
            print(f"Extracted {len(companies)} companies")
            
            for company in companies[:5]:  # Show first 5
                print(f"- {company['name']}: {company['url']}")
        else:
            print("Failed to scrape test URL")
    
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())