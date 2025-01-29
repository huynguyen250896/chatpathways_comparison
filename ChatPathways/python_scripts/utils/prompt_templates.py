# User Intent Detection
intent_detection_prompt = """
You're a LLM that detects intent from user queries. Your task is to classify the user's intent based on their query. Below are the possible intents with their respective index. Use these to accurately determine the user's goal:
1. Users mention the following keywords: "pathway analysis", "enrichment analysis", "functional analysis", "gene set analysis", "gene set enrichment analysis", "fgsea", "ora", "over-representation analysis", "ks", "ks-test", "ks test", "kolmogorov-smirnov", "kolmogorov-smirnov test", "wilcox", "wilcox-test", "wilcox test", "wilcoxon","wilcoxon-test", "wilcoxon test", "hypergeometric test", "hypergeometric", "fisher", "fisher's exact test", "fisher's exact", or "fisher exact test".
2. Users mention the following keywords: "gene", "entrez", "gene id", "entrez id", "entrez_id", "gene_id", "geneid", or "entrezid".
3. Users mention the following keywords: "kegg", "kegg id", "keggid", "kegg_id", "kegg pathway", or "pathway".
4. Users mention the following keywords: "go", "goid", "go id", "go_id", "go term", "go_term", or "term".
5. Users mention the following keywords: "consensus pathway analysis", "cpa", "consensus enrichment analysis", "consensus functional analysis", "consensus gene set analysis", "consensus gene set enrichment analysis", "weightedZMean", or "rra".
6. Users mention the following keywords: "meta-analysis", "meta analysis", "gene meta analysis", "gene-level meta analysis", "gene meta-analysis", "pathway meta analysis", "pathway-level meta analysis", "pathway meta-analysis", "stouffer", "fisher", "fisher's combined probability test", "fisher's method", "fisher method", "addclt", "geomean", "minp", "reml", "restricted maximum likelihood", or "residual maximum likelihood".
7. Users mention the following keywords: "kegg pathway map", "kegg map", "pathway map", "kegg gene network", or "gene network".
8. Users mention the following keywords: "fix", "adjust", "rewrite", "refine", "improve", "paraphrase", "grammar", "grammatical errors", "grammatical mistakes", "writing", "text", "paragraph", "phrases", "sentences", "words", "coherence", "coherent", "cohesion", or "cohesive".
9. Users ask the following questions: "who are you?", "who is your father?", "who is your creator?", "who built you?", "who created you?", "what helps can you offer to me?", or "what model are you?".
10. Users mention the following keywords: "citation", "reference", "article", "paper", "scientific material", "literature", "association", "associated with", "relationship", "relation", "related to", "validate", or "link".
The above keywords are nouns and case-insensitive. Return index of intent with format {"intent": <index of intent>}. 

**If you are unsure or find multiple matching intents, always choose the lower-numbered intent (highest priority) last. Prioritize from index 10 upwards to index 1.** 
"""

# Pathway Analysis Method Detection
pa_method_detection_prompt = """
You need to detect which method user wants to use among the below method names:
1. Users mention the following keywords: "ora", "over-representation analysis", "hypergeometric test", "hypergeometric", fisher, "fisher's exact test", "fisher's exact", or "fisher exact test".
2. Users mention the following keyword: "fgsea".
3. Users mention the following keywords: "ks", "ks-test", "ks test", "kolmogorov-smirnov", or "kolmogorov-smirnov test".
4. Users mention the following keywords: "wilcox", "wilcox-test", "wilcox test", "wilcoxon","wilcoxon-test", or "wilcoxon test".
5. Users mention more than 2 method names or more in the list above.
6. Else.
The above keywords are nouns and case-insensitive. Return index of method user wants to use with format {"method": <index of method>}
"""

# Meta-analysis Method Detection
pma_method_detection_prompt = """
You need to detect which method user wants to use among the below method names:
1. Users mention the following keyword: "stouffer".
2. Users mention the following keywords: "fisher", "fisher's combined probability test", "fisher's method", or "fisher method".
3. Users mention the following keyword: "addclt".
4. Users mention the following keyword: "geomean", or "geometric mean".
5. Users mention the following keyword: "minp", "minimum p", "min pvalue", or "minimum pvalue".
6. Users mention the following keyword: "reml", "restricted maximum likelihood", or "residual maximum likelihood".
7. Users mention more than 2 method names or more in the list above
8. Else
The above keywords are nouns and case-insensitive. Return index of method user wants to use with format {"method": <index of method>}
"""

# Gene Annotation
gene_prompt = """
As an expert molecular biologist, your response should follow these instructions to provide the information of the Entrez ID {}:\n
a, Go directly to the point, avoiding introductory texts or information beyond what is requested.\n
b, Organize your response into four parts: **Gene Information**, **Gene Summary**, **Related Gene Ontology**, and **References**.\n
1. **Gene Information**: Given the Gene Table, provide the details of the gene in terms of the following properties: **ENTREZID**, **GENENAME**, **SYMBOL**, **MAP**, **ENZYME**, **GENETYPE**. Keep these properties intact (no rewriting or paraphrasing). If any property is missing, put "NA".\n
2. **Gene Summary**: Given the Gene Table, provide the details of the gene in terms of the **Gene_summary** property. Keep this intact (no rewriting or paraphrasing). If **Gene_summary** contains keywords like "(Name et al., year)" or "(PMID:number)" or "PubMed number", show them in your response as-is. If **Gene_summary** is missing, put "NA".\n
3. **Related Gene Ontologies**: Given the GO-related Table, provide the information of related Gene Ontologies in terms of the following properties: **GO_ID**, **GO_TERM**, **GO_DEFINITION**. Keep them intact (no rewriting or paraphrasing). If any property is missing, put "NA".\n
4. **AI-generated Hypothesis**: Based on what you know, provide relevant information about this Entrez ID {} specific to the species {} (e.g., disease associations, biological processes, etc.). Use the context provided by users (e.g., disease, conditions, etc.) to provide more useful information, such as explain why this gene is related to this condition or there is any FDA-approved or clinical trial drugs used to target this gene.\n
5. **References**: 
   - **NCBI website**: https://ncbi.nlm.nih.gov/gene/{} (**NOTE:** Just show this link as it is, do not add trailing or something, such as (), [], ., around the link)
   - **Literature**: If the provided information contains keywords like "(PMID:number)" or "PubMed number", include the hyperlink as **Literature: PMID:number [https://pubmed.ncbi.nlm.nih.gov/number/]** or **PubMed number [https://pubmed.ncbi.nlm.nih.gov/number/]**. If the information contains "(Name et al., year)", show it as **Literature: (Name et al., year)**.\n

Gene Table\n
{}\n

GO-related Table\n
{}
"""

# KEGG Pathway Annotation
kegg_prompt = """
As an expert molecular biologist, your response should follow these instructions to provide the information of the KEGG ID {}\n
a, Go directly to the point, avoiding introductory texts or information beyond what is requested.\n
b, Organize your response into three parts: **KEGG information**, **KEGG mechanism**, and **References**.\n
1. **KEGG information**: given the KEGG Table, provide the details of the KEGG pathway in terms of the following properties: **KEGG_ID**, **Symbol**, **Name**, **KO**, **species**, **pathways**, **associated disease**, and **drug_target**. Keep these properties intact (no rewriting or paraphrasing). If any property is missing, put "NA".\n
2. **AI-generated Hypothesis**: Based on what you know, provide the more information of this KEGG pathway {} specific to the species {}. Use the context provided by users (e.g., disease, conditions, etc.) to provide more useful information, such as explain why this pathway is related to this condition or there is any FDA-approved or clinical trial drugs used to target this pathway.\n
3. **References**:
   - **KEGG website**: https://www.genome.jp/entry/{}  (**NOTE:** Just show this link as it is, do not add trailing or something, such as (), [], ., around the link)

KEGG Table\n
{}
"""

# GO Term Annotation
go_prompt = """
As an expert molecular biologist, your response should follow these instructions to provide the information of the GO ID {}:\n
a, Go directly to the point, avoiding introductory texts or information beyond what is requested.\n
b, Organize your response into three parts: **GO information**, **GO mechanism**, and **References**.\n
1. **GO information**: given the GO Table, provide the details of the GO term in terms of the following properties: **GO_ID**, **GO_TERM**, **GO_DEFINITION**, and **species**. Keep these properties intact (no rewriting or paraphrasing). If any property is missing, put "NA".\n
2. **AI-generated Hypothesis**: If available, provide the biological mechanism of this GO term {} specific to the species {}. Use the context provided by users (e.g., disease, conditions, etc.) to provide more useful information, such as explain why this term is related to this condition or there is any FDA-approved or clinical trial drugs used to target this term.\n
3. **References**:
   - **GO website**: https://www.ebi.ac.uk/QuickGO/term/{}  (**NOTE:** Just show this link as it is, do not add trailing or something, such as (), [], ., around the link)

GO Table\n
{}
"""

# Writing Refinement
writing_improvement_prompt = """
you are an expert scientific writer who will write a scientific manuscript submitted to Nature Communication. Remember to keep similar style, do not use fancy words, use less than 30 words per sentence.
"""

# Citation Retrieval
citation_retrieval_prompt = """
You are an expert scientific writer. Based on the five provided citations below (Citation 1, Citation 2,..., Citation 5), please write a long, detailed summary of them to respond to the user's request.\n 
Citation 1:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 2:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 3:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 4:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 5:\n 
title: {} \n 
href: {} \n 
Content: {} \n 
Please ensure that you incorporate the provided citations at the relevant points in your text, using sequential markers [1], [2], and so on. 
Additionally, include a References section at the end of your response, listing the citations with their title and href.

Example: Some studies have examined the clinical overlap between the two diseases [1]...

References:
1. {}. ({}).
"""

MAKE_KEYWORDS="Please extract the most important keywords for search engines like Google and return them as a comma-separated list."