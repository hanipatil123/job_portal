from django.core.management.base import BaseCommand
from job_seeker.models import Job
class Command(BaseCommand):
 help='Create sample jobs for local testing'
 def handle(self,*args,**kwargs):
  entries=[('Frontend Developer','PixelCraft Labs','Pune','Full-time','₹5–9 LPA','Build modern React interfaces and reusable UI components.','React, JavaScript, CSS'),('Python Django Developer','CodeSphere','Bengaluru','Full-time','₹6–12 LPA','Develop scalable Django applications and REST APIs.','Python, Django, SQL'),('Data Analyst Intern','InsightWorks','Mumbai','Internship','₹20k/month','Build dashboards and analyze business data.','Excel, SQL, Power BI'),('UI/UX Designer','Studio Nova','Remote','Remote','₹4–8 LPA','Create delightful product experiences and design systems.','Figma, User research'),('Backend Engineer','CloudNest','Hyderabad','Full-time','₹8–16 LPA','Build secure backend services and data pipelines.','Python, APIs, PostgreSQL'),('Junior Full Stack Developer','BrightStack','Pune','Full-time','₹4–7 LPA','Work on frontend and backend product features.','HTML, CSS, Django, JavaScript'),('QA Automation Intern','TestPilot','Chennai','Internship','₹18k/month','Create automated tests and improve quality.','Python, Selenium'),('Business Analyst','DataBridge','Delhi','Contract','₹6–10 LPA','Translate business needs into product requirements.','SQL, Communication')]
  n=0
  for title,company,location,kind,salary,description,requirements in entries:
   _,created=Job.objects.get_or_create(title=title,company=company,defaults={'location':location,'job_type':kind,'salary':salary,'description':description,'requirements':requirements})
   n+=created
  self.stdout.write(self.style.SUCCESS(f'Created {n} sample jobs.'))
