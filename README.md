# ChatPathways

The code and data repository of "A biologist-oriented research assistant for system-level data analysis with substantially mitigated hallucinations".

The three Alzheimer's disease datasets, *GSE5281*, *GSE61196*, and *GSE153873*, were downloaded from NCBI GEO and used as example datasets in this study. Users can access these datasets, along with example data generated in this work by unzipping the file `unzip-me.zip`.

# 🚀 QUICK START

Below, we reproduce the results for the evaluation tasks presented in this study

Users should make sure they have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed already.

**Step 1:** Clone this repository and save it to a folder on your local machine
```
# If you are users with a Linux/MAC computer, open your terminal
# If you are users with a Windows computer, open your Windows Powershell
cd Desktop                              
git clone https://github.com/huynguyen250896/chatpathways_comparison
cd chatpathways_comparison
```

**Step 2:** Create a hidden `.env` file with the following content, replacing **[YOUR OPEN API KEY]** with your actual key. ChatPathways utilizes the `gpt-3.5-turbo-0125` version for evaluation tasks.
```
# API key for OpenAI's ChatGPT
OPENAI_API_KEY= [YOUR OPEN API KEY]
```
⚠️Warning: avoid sharing your API key with others or uploading it to public spaces.

**Step 3:** To build the Docker image for ChatPathways, run the following command:
```
# build the ChatPathways image
docker-compose up --build
```

**Step 4:** Users must pull large language models to their local machine. For each model, open a new terminal, run the respective command, and KEEP the terminals open while running comparisons:
```
# pull Phi3.5 to the local machine
docker exec -it ollama ollama run phi3.5

# pull Mistral to the local machine
docker exec -it ollama ollama run mistral

# pull Llama3.1 to the local machine
docker exec -it ollama ollama run llama3.1
```
Note: To explore other large language models, visit the [official Ollama website](https://ollama.com/search)

**Step 5:**  Open a new terminal and users can access the ChatPathways container using: 
```
docker exec -it chatpathways_container bash
``` 
Then, run the evaluation tasks with:
```
python3 llm_comparison.py
``` 

# License

ChatPathways is distributed under an MIT License.

# Citation

TBD

# Contact

Corresponding Authors: Duc-Hau Le (hauldhut@gmail.com).

Report bugs and provide suggestions by sending email to the maintainer Quang-Huy Nguyen (huynguyen96.dnu@gmail.com) or open a new issue on this Github page.
