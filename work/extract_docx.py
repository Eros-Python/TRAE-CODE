import docx
from docx.document import Document as DocObj
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

doc = docx.Document('/workspace/.uploads/54e08fdf-6e8c-48fe-a805-a2f4b61832f1_1.PV数据库市场调研.docx')

def iter_block_items(parent):
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

idx = 0
for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        style = block.style.name if block.style else ''
        text = block.text.strip()
        if text:
            print(f"[P:{style}] {text}")
    else:
        print(f"=== TABLE {idx} ({len(block.rows)} rows x {len(block.columns)} cols) ===")
        for r in block.rows[:40]:
            cells = [c.text.strip().replace('\n',' / ')[:60] for c in r.cells]
            print(" | ".join(cells))
        if len(block.rows) > 40:
            print(f"... ({len(block.rows)-40} more rows)")
        idx += 1
