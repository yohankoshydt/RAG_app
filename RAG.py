import json
import regex as re
import os

class Config:

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    #MONGO_URI = "mongodb+srv://new:VtMVDPqAtfUqkDS0@resume-data.1ueh5w9.mongodb.net/?appName=resume-data"
    #DB_NAME = 'vectors'
    #COLLECTION_NAME = 'test'
    #AWS_KEY = 'AKIAQO5H23OL36W7OZEF'
    #AWS_SECRET_KEY = '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'
    #AWS_REGION = 'us-east-1'

class GenerationHandler:
    def __init__(self):
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def llm_response(self, prompt):
        completion = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

class QueryHandler:
    def __init__(self):
        self.generation_handler = GenerationHandler()

    @staticmethod
    def parse_response(response):
        json_pattern = r"\{(?:[^{}]|(?R))*\}"
        match = re.search(json_pattern, response)
        first_json_str = match.group(0) if match else None
        if first_json_str:
            try:
                summary_data = json.loads(first_json_str)
                return summary_data
            except json.JSONDecodeError:
                print(first_json_str)
                return "Failed to Parse JSON"
        else:
            return None

    def summarize_page(self, context):
        prompt = f'''
            You are a webpage summarizer.
            Instructions:
            You will be given the text from a website of a company (Context).
            Generate a json object in the following format summarizing the services provided by the company and other information
            about the company that would be relevant to be used by sales teams(Description). 
            Note that Industry of the company means it's high level sector. Choose the appropriate one from the following list:
            ['Construction', 'Manufacturing', 'Information Technology', 'Healthcare', 'Media', 'Travel', 'Insurance', 'Consulting', 'Other']
           

            Response Format:
                  
                    {{"Industry" : "",  "Description": ""}},
                    
                  

            Context: {context}
            Your Response:'''
        response = self.generation_handler.llm_response(prompt)
        print(response)
        return self.parse_response(response)  # Using the parse_response function

    def generate_email(self, presets, context, print_context=False):
        if print_context:
            print(f'context: {context} \n presets: {presets}')
        
        prompt = f'''
          You are a {context['Sender_Designation']} named- {context['Sender_Name']} of company- {context['Sender_Company']} 
          and you have been tasked to write a cold sales email to the {presets['Recipient_Designation']} 
          {presets['Recipient']} of {presets['Recipient_Company']} you will be given information relating to what services we ({context['Sender_Company']}) can
          provide them ({presets['Recipient_Company']}) in the next section named Context.

          #Context: 
          Industry of Recipient Company: {context['Industry']}
          Summary of Recipient Company: {context['Rec_summary']}
          Profile of the Recipient : {presets['Recipient_Function']}
          
          #Subset of our portfolio that is relevant to them:
          {'Relevant Case Studies' if context['case_studies'] else None } {context['case_studies']}
          {'Relevant Dashboards' if context['dashboards'] else None } {context['dashboards']}
          {'Clients Served' if context['clients'] else None }  {context['clients']}

          #Instructions: 
          Create a subject line that captures attention, using personalization with either the recipient’s name or company. Keep it brief and relevant to the industry.
          Begin with a warm, personalized greeting that includes the recipient's name and role. 
          
          Use an attention-grabbing opening line by referencing the recipient company’s work or industry challenges, showing a clear understanding of their goals. Acknowledge a specific challenge in their industry or refer to a recent achievement or expansion as described in the context.
          Introduce how the sender’s company can address their specific needs, focusing on outcomes rather than features. Use the provided portfolio subset to highlight specific services, dashboards, or case studies that demonstrate success with similar clients.
          
          Add social proof by referencing relevant case studies or dashboards that showcase credibility and experience. Use any key metrics or results provided, showing clear, measurable success with previous clients.
          
          Offer a clear call to action, suggesting a low-commitment next step, like a brief meeting to explore further. Keep it open and considerate of the recipient’s time.
          
          End with a polite thank-you and an optimistic closing.
          Use this structured approach to ensure the email is personalized, relevant, and presents the sender’s company as a valuable partner for the recipient’s company in their industry.

          ################


            
          

          Response Format: {{"email_content": """ """}}

          
          Your Response:'''
        print(prompt)
        response = self.generation_handler.llm_response(prompt)
        return response
