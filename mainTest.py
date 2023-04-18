from pyresparser import ResumeParser
import json
data = ResumeParser('Alicia_Rapelye_Resume.pdf', skills_file='skills.csv').get_extracted_data()

print(data)

# Output save in a json file with the name resume.json:

finalData = json.dumps(data, indent=4)
with open(f'{data["name"]}.json', 'w') as f:
    f.write(finalData)

