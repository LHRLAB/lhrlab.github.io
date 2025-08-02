import re

def convert_html_like_str_to_latex(text):
    # Decode minimal HTML entities
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")

    # Convert <sup>†</sup> to \textsuperscript{†}
    text = re.sub(r"<sup>(.*?)</sup>", r"\\textsuperscript{\1}", text)

    # Convert <strong>...</strong> to \textbf{...}
    text = re.sub(r"<strong>(.*?)</strong>", r"\\textbf{\1}", text)

    # Convert <em>...</em> to \emph{...}
    text = re.sub(r"<em>(.*?)</em>", r"\\emph{\1}", text)

    # Convert <a href="URL">[text]</a> to \href{URL}{[text]}
    text = re.sub(r'<a href="(.*?)">\[(.*?)\]</a>', r'\\href{\1}{[\2]}', text)

    # Remove any other remaining HTML-like tags (just in case)
    text = re.sub(r"<[^>]+>", "", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def convert_markdown_to_latex(md_text):
    str_list = []
    
    
    # Split into sections like 'Preprint', '2025', etc.
    sections = md_text.split("<h2>")[1:]
    for cnt, sec in enumerate(sections):
        # year = sec.split("</h2>")[0].strip()
        content = sec.split("</h2>")[0].strip()
        str_list.append(r"\vspace{0.5mm}")
        str_list.append(r"\textbf{"+content+r"}")
        if content == "Preprint":
            str_list.append(r"\begin{itemize}[itemsep=0mm, topsep=2mm, leftmargin=*]")
        elif cnt == 1:
            str_list.append(r"\begin{enumerate}[series=resumeCounter, itemsep=0mm, topsep=2mm, leftmargin=*]")
        else:
            str_list.append(r"\begin{enumerate}[resume*=resumeCounter, itemsep=0mm, topsep=2mm, leftmargin=*]")

        # 将content分出不同的部分<li>...</li>
        papers = sec.split("<li>")[1:]
        for p in papers:
            p_str = p.split("</li>")[0].strip()
            str = convert_html_like_str_to_latex(p_str)
            str_list.append(r"\item "+str)
        str_list.append(r"\end{itemize}" if content == "Preprint" else r"\end{enumerate}")
        str_list.append("")
        
    output_str = "\n".join(str_list)

    return output_str


md_text = """
- *Conference Area Chair*: NeurIPS 2025, KDD 2025, KDD 2026
- *Conference PC Member/Reviewer*: NeurIPS 2024, NeurIPS 2025, ICLR 2025, ICML 2025, ACL 2023, ACL 2024, ACL 2025, AAAI 2023, AAAI 2024, AAAI 2025, AAAI 2026, KDD 2025, WWW 2025, ACM MM 2025, EMNLP 2022, EMNLP 2023, EMNLP 2024, EMNLP 2025, NAACL 2024, NAACL 2025, COLING 2025, CIKM 2024, AISTATS 2025, NLPCC 2024, NLPCC 2025, CCKS 2025, IEEE ICKG 2025
- *Journal Reviewer*: IEEE Transactions on Knowledge and Data Engineering (IEEE TKDE), IEEE Transactions on Dependable and Secure Computing (IEEE TDSC), Information Processing & Management (IPM), Pattern Recognition (PR), Knowledge-Based Systems (KBS), Neurocomputing, Geo-spatial Information Science (TGSI)
"""

def convert_services(md_text):
    lines = md_text.strip().splitlines()
    latex_items = []

    for line in lines:
        if line.startswith("- *") and "*:" in line:
            # 拆分粗体标题与内容
            part = line[3:]  # 去掉 - *
            title, content = part.split("*:", 1)
            title = title.strip()
            content = content.strip().replace("&", r"\&")  # 转义 &
            latex_line = f"\\item \\textbf{{{title}}}: {content}"
            latex_items.append(latex_line)

    # 输出 LaTeX 格式
    latex_output = "\n".join(latex_items)
    return latex_output

with open("resume/template/resume_template.tex", "r") as f:
    resume_template = f.read()

with open("_pages/includes/pub_short.md", "r", encoding="utf-8") as f:
    md_text = f.read()
pub_str = convert_markdown_to_latex(md_text)
resume_template = resume_template.replace("##PUB_STR##", pub_str)

with open("_pages/includes/services.md", "r", encoding="utf-8") as f:
    md_text = f.read()
services_str = convert_services(md_text)
resume_template = resume_template.replace("##SERVICES_STR##", services_str)


with open("resume/HaoranLuo.CV.tex", "w") as f:
    f.write(resume_template)