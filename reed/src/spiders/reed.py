from urllib.parse import urljoin

import scrapy
from apify import Actor
import random

# Scrapes titles pages and enqueues all links it finds on the page
class reed(scrapy.Spider):
    name = 'reed'

    custom_settings = {
        # 'JOBDIR': f'./crawls/{name}', # for resuming of crawlers or to save the scraped state
        'CONCURRENT_REQUESTS': 1,
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY':0.5,
        'RETRY_TIMES':5,
        'RETRY_HTTP_CODES' : [500, 502, 503, 504, 400, 403, 404, 408, 416]

    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.irishjobs.ie/jobs/in-armagh",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Brave\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    cookies = {
        "s_ppvl": "%5B%5BB%5D%5D",
        "s_ppv": "%2FJobSearch%2FJobDetails.aspx%2C9%2C9%2C360%2C1536%2C360%2C1537%2C458%2C1.25%2CP",
        "_abck": "B5DF798D8965E95A5BA617483DE873FA~-1~YAAQVV3SFyREPqqLAQAAu7YUtwoenghR4QLGME/GEevAABy17jfDSuxpxErOWlJt46FIyleEjZVBHuZJ25++O1CT6DMM/SydyAnMRjjjHHndSh6MKe1mddrM9Yms+Tui/ANH8z4OiSptChgJanU7B+Pwdp2Q8zBdhko13cpgViRgIafy9hFWT/fakBKPYRM0AJzteHUiql+oU+eJLRmp8LYqrOWUEeWXXIo0aGG12zSJ6bkxL6JYbPKcRFeknmzn7drBFp0A5qXRFLee19TFZtWerBDmVWm+t2t3nkL3ROh4xjtdwHAkSP08fJhaGLqCQlQ1WL7R4y1XEqX9655FMqoFUQz8LRkU+w8bIjpv4veveYcMOt3JcBO6DNfK9A==~-1~-1~-1",
        "bm_sz": "AC36CED994F2477BFAF26C7981D26E63~YAAQVV3SFyVEPqqLAQAAu7YUtxUhPKDfvaCAzLb8w3AL8wv8dmA2bGqbSTkuw82X7UIVG/W7yTGKfk6UfeVqUNsiWUQWq6wPKOsyKLDlLLyIBwk1vtfNS6Z9bPsSk4T29KjwV/TVcxpmrLG0PlERDgWJw1KEkqMMFUCUsHv1yNte4m9vvBOMs5qwWMibv+DhO23s+nmR9XYDbu9PsO+WlElez3knPiga67Bdllg53wuUzDdBzKY2Vw7V0oxxPUJxAtq5BXoP+w7kAK9TA3LKqnVWp9jOL7kdv+NHWtjGaRWEC3wO9w==~4473913~4408887",
        "VISITOR_ID": "18505badb2c92f8d51a19b6681aeb0bb",
        "AKA_A2": "A",
        "ak_bmsc": "402C29C839DF42830693296B5BC02829~000000000000000000000000000000~YAAQVV3SF2JEPqqLAQAA0b4UtxXE1ktzzEVKGq0DGHTFfjhVmoHRZdXxb1dpsMfMCR+nhdrNsR5fTrNmH+liwHFSaIgqSzUnF2Jq8YxvEvnSO7peEps4F4y+H6aeyaMkmb2g6NSPAdsEwg1WvpK/ksjCdqyJFBUcsFwWWN6Mf60XD+AVt/R+CWqKRfg+p1TmvD3ZpBfTmv0msVurye5IEdpekKpxIT1XyS/7sJIvVcPg6aR+LzE+OrrHXf2TwvGWCuEmyz5fLNDSr/WHAOpjKIsg0IAVtkRBmK84LMZUf0MRMzZLgj5vJHJdMgHETSsUVJHIzpGT2FTS4Xw6p4pHP8Hj3HKLhEQ8IXZYQy1do3Ra4BCv+ExXAlY6KQkJFIZKwXrezwknnMKZ1Xm+2BKjI3sJlurd8OA4vftO7jfGRZImA5+Qo9WnVOzuZ3GWirnqa57YwW2w4IjHA/QplLzlsId9t/V90ovWdgxvC9i8vF89uy88kdin7VUp"
    }
    

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.irishjobs.ie/jobs/in-armagh',
            callback=self.parse,
            # body = body ,
            headers=self.headers,  # uncomment this if you want to use custom headers
            cookies = self.cookies,
            # headers=header.generate(),
            # use fake random headers whenever possible as this will help you avoid getting blocked
            # cookies=self.cookies,
            meta={
                'key': 'value',
                # 'proxy': config('ROTATING_PROXY_URL'),  # cheaper proxy (webshare)
                # 'proxy': config('PROXY'), # packetstream proxy,
                # 'playwright' : True
            }
        )

    def parse(self, response):
        jobs = response.xpath('//article[@data-at = "job-item"]//a[@data-at="job-item-title"]/@href').getall()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://www.irishjobs.ie/job/electrical-estimator/mtm-engineering-ltd-job101373465",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Brave\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }


        for job in jobs:
            new_url = 'https://www.irishjobs.ie' + job
            cookies = {
                "bm_sz": "AC36CED994F2477BFAF26C7981D26E63~YAAQVV3SFyVEPqqLAQAAu7YUtxUhPKDfvaCAzLb8w3AL8wv8dmA2bGqbSTkuw82X7UIVG/W7yTGKfk6UfeVqUNsiWUQWq6wPKOsyKLDlLLyIBwk1vtfNS6Z9bPsSk4T29KjwV/TVcxpmrLG0PlERDgWJw1KEkqMMFUCUsHv1yNte4m9vvBOMs5qwWMibv+DhO23s+nmR9XYDbu9PsO+WlElez3knPiga67Bdllg53wuUzDdBzKY2Vw7V0oxxPUJxAtq5BXoP+w7kAK9TA3LKqnVWp9jOL7kdv+NHWtjGaRWEC3wO9w==~4473913~4408887",
                "VISITOR_ID": "18505badb2c92f8d51a19b6681aeb0bb",
                "AKA_A2": "A",
                "ak_bmsc": "402C29C839DF42830693296B5BC02829~000000000000000000000000000000~YAAQVV3SF3JEPqqLAQAAScEUtxVfYtojea88ha2vvJqN2GjA2LMJZMMODJ7t2e7cMw9BE32i8WGmt698pIPD+tjxliaGpUPS7WFdZuFbNV7UVU2qfrFgIszhiFgwY6q5iSixbUlbOJhs6/3Ym3uqixAHUCHT/FuS6IzrrmMF7wbAVYA78VCrrxMdNv1uWBAdmY5eap7jTtW8WKYggr23IcMB46Bi9U/73G4+MGgsRcZJCfFNArI6EKPNZ/kOOTM8wGgjly7LMte9paltN67ZqEJ/bc+BC+HXjn9/Y3w3eAuH0nNyJiH9cVUT1c+XoeMSBeUz+aRGBD2Mcf/lD50vFhJtqp4dHZWMrwrC1Km64cKLC7d4/sv0aFtAJKyPEFHLpHCaRrhDyEJn6lDC4EbLbm3DbSm+zvmlSYNzk+sUytq2aaWYlxMM4Im6DviNAGv7",
                "sc_vid": "d9eb5c38554769c675750474fbb368e3",
                "s_fid": "6ce944714dd79658-c1d8c3d4adb5bf84",
                "AnonymousUser": "MemberId=7f565900-f612-4ee7-8a4c-aede16aa4021&IsAnonymous=True",
                "SessionCookie": "607bba46-2c02-47de-b8c4-e8f43fee86f0",
                "SsaSessionCookie": "31b18a75-3c92-4185-8cd5-3bf051215fc3",
                "EntryUrl": "/jobs/in-armagh",
                "_abck": "B5DF798D8965E95A5BA617483DE873FA~0~YAAQVV3SF/1EPqqLAQAA5tYUtwoLEpOM1YOG5UHN+JUZHYu3xBeAebQM+HeCeXnalC3bwhqXeeL6JheZ99ltGVZ834r7dt/NyMxQJk+aO17NHBd75lZN5TDY3xMwoMPiD1oNRNyorduYhKiNQ4WEyO3MovmpaPeJnoeMtoNhMX2TdnFAMGmepC2DrAbI698b/+Ycx4Zp13RQR6KHDrhDH57J8tANm50CElDH1d6lt8XizAAO/VlzkTFqFjAdyhpRjV01FyIwNditaNoJUWagamoqUNfZJHShjshdcgFigCdqzjww1CKzH7dnhXawSCxf8wktxVnxOoWAYbgNIVwkVFEZ95hIvC0ZSkz7E1NaVKAEd5y1QoNpMUVkFZ4S3pN62C5K+ld8iPLekHrxK1x/8xje/bPXhjy4Vlk=~-1~||-1||~-1",
                "isMobile": "0",
                "NONEU": "1",
                "PJBJOBSEEKER": "0",
                "LOCATIONJOBTYPEID": "null",
                "FreshUserTemp": f"{new_url}",
                "listing_page__qualtrics": "empty",
                "utag_main": "v_id:018bb7205aeb002344ee73057b880406f00520670090f$_sn:1$_se:2$_ss:0$_st:1699586234679$ses_id:1699584432879%3Bexp-session$_pn:2%3Bexp-session$PersistedClusterId:IJ--13%3Bexp-session$PersistedFreshUserValue:0.1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session",
                "gpv_pn": "%2FJobSearch%2FJobDetails.aspx",
                "s_cc": "true",
                "s_ppvl": "%2FJobSearch%2FJobDetails.aspx%2C21%2C21%2C750%2C1536%2C750%2C1537%2C758%2C1.25%2CP",
                "s_ppv": "%2FJobSearch%2FJobDetails.aspx%2C21%2C21%2C750%2C1536%2C360%2C1537%2C458%2C1.25%2CP"
            }
            yield scrapy.Request(
            url=new_url,
            callback=self.parse_details,
            headers=headers,
            cookies= cookies,  # uncomment this if you want to use custom headers
            # headers=header.generate(),
            # use fake random headers whenever possible as this will help you avoid getting blocked
            # cookies=self.cookies,
            meta={
                'key': 'value',
                # 'proxy': config('ROTATING_PROXY_URL'),  # cheaper proxy (webshare)
                # 'proxy': config('PROXY'), # packetstream proxy
                # 'playwright' : True

            }
        )
    
        next_btn = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_btn:
            yield scrapy.Request(
                url=next_btn,
                callback=self.parse,
                headers=self.headers,  # uncomment this if you want to use custom headers
                # headers=header.generate(),
                # use fake random headers whenever possible as this will help you avoid getting blocked
                cookies=self.cookies,
                meta={
                    'key': 'value',
                    # 'proxy': config('ROTATING_PROXY_URL'),  # cheaper proxy (webshare)
                    # 'proxy': config('PROXY'), # packetstream proxy
                }
            )
    def parse_details(self, response):
        title = response.xpath('//h1[@id="job-title"]/text()').get(default="").strip()
        id = response.xpath('//input[@id="jobId"]/@value').get()
        salary =  response.xpath('//li[@class="salary icon"]/div/text()').get()
        location = ", ".join((response.xpath('//li[@class="location icon"]/div/*/text()').getall()))
        job_type = response.xpath('//li[@class="job-type icon"]/div/text()').get()
        date_posted = response.xpath('//li[@class="date-posted icon"]/div/*/text()').get()
        recruiter = response.xpath('//a[@id="companyJobsLink"]/text()').get()
        # breakpoint()
        description = response.xpath('//div[@class="job-description"]//*')
        new_description = ""
        for tags in description:
            if tags.root.tag == "strong":
                new_description += tags.xpath('./text()').get()
                continue
            new_description = new_description + "\n" + tags.xpath('./text()').get(default= "")
        apply_link = ''
        if id:
            apply_link = 'https://www.irishjobs.ie/job/' + id + '/apply'

        
        info_dict = response.xpath('//script[@id="jobPostingSchema"]/text()').get(default='{}').strip()
        info = json.loads(info_dict)

        def extract_date_string(date_str):
            # Parse the date and time from the string
            date_time_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M%z")

            # Extract the year, month, and day and format them as a string
            return date_time_obj.strftime("%Y-%m-%d")
        


        data_dict = {
            'url' : response.url , 
            'job_title' : title,
            'ID' : id,
            'salary' : salary,
            'location' : location ,
            'contract_type' : '',
            'job_type' : job_type ,
            'posted_on_refreshed_on' : extract_date_string(info['datePosted']),
            'Recruiter' : recruiter,
            'job_description' : new_description,
            'application_link' : apply_link,
            'closing_date' : extract_date_string(info['validThrough']),
            'job_poster' :None
            

        }
        yield data_dict