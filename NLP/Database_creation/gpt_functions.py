#This is the code from the previous project and its purpose here is for future usecase


from pydantic import BaseModel, Field
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function
)
from typing import List

class job_offer(BaseModel):
    """Extracting details from job offer"""
    required_skills: List[str] = Field(description="While extracting required skills take into account only those skills/abilities that were explicitly mentioned as required. Do not include additional assets. If not provided, return blank space " )
    nice_to_have: List[str] = Field(description="Extract All advantages (that are not required but would be appreciated) like additional: skills, certificates and others. If not provided, return blank space ")
    required_work_experience: List[str] = Field(description="Extract Work experience that is required in job offer. If not provided, return blank space ")
    languages: List[str] = Field(description="Extract Languages that are required in job offer. If not provided, return blank space ")
    workplace_mode: List[str] = Field(description="Extract Prefered workplace mode: Remote, Hybrid, In office. If not provided, return blank space ")
    required_education: List[str] = Field(description="Extract Education required in job offer. If not provided, return blank space ")

class CV_evaluation(BaseModel):
    "numerical/bollean evaluation of a candidate's CV"
    description_1: str = Field(description="Description that summarize only candidate's 'nice to have', languages, workplace mode, and education")
    languages: bool = Field(description="Bollean value that determinates whether candidate have desired languages on a proper level of proficiency.")
    workplace_mode: bool = Field(description="Bollean value that determines whether a given workplace mode - (Remote, Hybrid, In office) mode  is suitable for the candidate.")
    required_education: bool = Field(description="Bollean value that determinates whether candidate have desired edunation. If no education is required in a job offer, always return true")

class Nice(BaseModel):
    "Analysis of additional advantages of the candidate"
    description_2: str = Field(description="Short description that summarizes whether candidate possesses nice to have advantages. Up to 50 words")
    nice_to_have: int = Field(description="The number of 'nice to have' advantages that the candidate meets")

"""Based on a description calculate the nubmer of nice to have that the candidate meets. While searching for nice to have pay attetntion to search whole CV to provide the most accurete number"""

class skills(BaseModel):
    "Analysis of candidates skills"
    description_3: str = Field(description="Short description that summarizes whether candidate possesses the required skills. Up to 50 words")
    required_skills: int = Field(description="The number of skills requirements that the candidate meets")

class Wrk(BaseModel):
    "Analysis of candidates work experience"
    description_4: str = Field(description="Short description that summarizes whether candidate possesses the desired work experience. Up to 50 words.")
    required_work_experience: int = Field(description="The number of work experience requirements that the candidate meets")


job_offr = convert_pydantic_to_openai_function(job_offer)
cv_eval = convert_pydantic_to_openai_function(CV_evaluation)
sks = convert_pydantic_to_openai_function(skills)
wrk = convert_pydantic_to_openai_function(Wrk)
nice = convert_pydantic_to_openai_function(Nice)

with open("./file.txt" , 'w', encoding="UTF-8") as f:
    f.write(str(job_offr))
    f.write("\n")
    f.write(str(cv_eval))
    f.write("\n")
    f.write(str(sks))
    f.write("\n")
    f.write(str(wrk))
    f.write("\n")
    f.write(str(nice))


