import yaml
import os

with open("resume/template/resume_template.tex", "r") as f:
    resume_template = f.read()


with open("_pages/projects.yml", "r") as f:
    data = yaml.safe_load(f)

s = ""
s += "\\section{Papers}\n\\resumeSubHeadingListStart\n"
for p in data["projects"]:
    s += f"  \\resumeSubItem{{{p['title']}}}{{{p['description']}}}\n"
s += "\\resumeSubHeadingListEnd\n"

# resume_template = resume_template.replace("##PROJECTS##", s)

with open("resume/resume.tex", "w") as f:
    f.write(resume_template)