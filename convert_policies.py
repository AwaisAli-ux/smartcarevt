import zipfile
import xml.etree.ElementTree as ET
import re
import json

docx_path = r"C:\Users\hp\Downloads\PRIVACY POLICY ETC.docx"

with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read("word/document.xml")
    tree = ET.fromstring(xml_content)
    texts = []
    for p in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        p_text = "".join(node.text for node in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text)
        if p_text.strip():
            texts.append(p_text.strip())

full_text = "\n\n".join(texts)

# Replace placeholders
full_text = full_text.replace("[YOUR SUPPORT EMAIL]", "support@smartcarevt.com")
full_text = full_text.replace("[YOUR WEBSITE URL]", "www.smartcarevt.com")
full_text = full_text.replace("[YOUR BUSINESS ADDRESS]", "Smart Care Tower, Blue Area")

# Split sections
part1 = re.search(r"Part 1: Terms of Service(.*?)(?=Part 2: Refund Policy)", full_text, re.S)
part2 = re.search(r"Part 2: Refund Policy(.*?)(?=Part 3: Delivery Policy)", full_text, re.S)
part3 = re.search(r"Part 3: Delivery Policy(.*?)(?=Part 4: Privacy Policy)", full_text, re.S)
part4 = re.search(r"Part 4: Privacy Policy(.*?)(?=Part 5: Disclaimer)", full_text, re.S)
part5 = re.search(r"Part 5: Disclaimer(.*?)(?=Contact Us)", full_text, re.S)
contact = re.search(r"Contact Us(.*)", full_text, re.S)

def format_section_html(text_block):
    if not text_block:
        return ""
    paragraphs = [p.strip() for p in text_block.strip().split("\n\n") if p.strip()]
    html_parts = []
    for p in paragraphs:
        if re.match(r"^\d+\.", p) or p.startswith("Last updated:"):
            html_parts.append(f"<h4 class='policy-section-subtitle'>{p}</h4>")
        elif p.startswith("•") or p.startswith("·") or p.startswith("- "):
            html_parts.append(f"<li class='policy-list-item'>{p.lstrip('•·- ')}</li>")
        else:
            html_parts.append(f"<p class='policy-paragraph'>{p}</p>")
    return "\n".join(html_parts)

policies = {
    "Terms of Service": format_section_html(part1.group(1)) if part1 else "",
    "Refund Policy": format_section_html(part2.group(1)) if part2 else "",
    "Delivery Policy": format_section_html(part3.group(1)) if part3 else "",
    "Privacy Policy": format_section_html(part4.group(1)) if part4 else "",
    "Disclaimer": format_section_html(part5.group(1)) if part5 else "",
    "Contact Us Details": format_section_html(contact.group(1)) if contact else ""
}

with open(r"d:\smartcaresites\SMARTCAREVT\policies_data.js", "w", encoding="utf-8") as f:
    f.write("const STORE_POLICIES = " + json.dumps(policies, ensure_ascii=False, indent=2) + ";\n")

print("Created policies_data.js successfully!")
