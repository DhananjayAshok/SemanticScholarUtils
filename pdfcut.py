doc_path="C:/Users/blued/Desktop/Paper Cache/Language Model in Game Playing"

import pymupdf
import string
import os


def maketitle(title, max_length=50):
    if title is None:
        return None
    for item in string.punctuation:
        title = title.replace(item, "")
    title = title.replace(" ", "_")
    title = title.lower()
    title = title[:max_length]
    title_parts = title.split("_")
    if len(title_parts) < 2:
        return title
    title = "_".join(title_parts[:-1])
    return title

def get_title(doc):
    text = doc.load_page(0).get_text()
    candidates = text.split("\n")[:5]
    kill_terms = ["Proceedings of ", ": Long Papers", ": Short Papers", "Association for Computational Linguistics", "Accepted at "]
    working_candidate = None
    for candidate in candidates:
        flag = False
        if len(candidate.split()) < 3:
            continue
        for kill_term in kill_terms:
            if kill_term in candidate:
                flag = True
                continue
        if flag:
            continue
        else:
            working_candidate = candidate
            break
    return maketitle(working_candidate)


def do_cut(in_path, out_folder, quit_default=9):
    doc = pymupdf.open(in_path)
    contents = doc.get_toc()
    conclusion_page = None
    for content in contents:
        if "Conclusion" in content[1].lower():
            conclusion_page = content[2]
            break 
    if not conclusion_page:
        if doc.page_count >= quit_default:
            conclusion_page = quit_default
        elif doc.page_count >= 5:
            conclusion_page = 5
        else:
            conclusion_page = doc.page_count - 1

    doc_title = get_title(doc)
    doc.select(range(conclusion_page))
    if doc_title is None:
        doc_title = os.path.basename(in_path).replace(".pdf", "")
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    doc.save(f"{out_folder}/{doc_title}.pdf")
    doc.close()

def cut_all(doc_path):
    for file in os.listdir(doc_path):
        if file.endswith(".pdf"):
            print(f"Doing: {file}")
            do_cut(f"{doc_path}/{file}", doc_path+"/cut/")

if __name__ == "__main__":
    cut_all(doc_path)


