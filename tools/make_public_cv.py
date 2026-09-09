#!/usr/bin/env python3
"""Build the public copy of the CV from the corrected private one.

    python3 make_public_cv.py defazio_cv_2026b.docx out/

The names to remove are NOT in this file. They are read from
public_cv_redactions.json in the same directory as the .docx -- td-resume/cv/,
which is private. This repository is public, and a list of the names the public
copy withholds would undo the withholding.

Removes the names of students -- 7 graduate mentees, 6 undergraduate mentees and
2 dissertation-committee members -- and replaces each block with a count and the
institutions. Adds a "full CV on request" line under the header.

WHAT IT DELIBERATELY DOES NOT TOUCH: students who are also co-authors in the
publication list. Those citations stay, and which ones are guarded is private. A
co-authorship is a published bibliographic fact they hold credit for; stripping it
would falsify the citation. The redaction removes the *mentee relationship*, not
the person from the document.

Rows are matched by name, and the script fails loudly if a name is missing --
so a regenerated CV that renumbers or reorders rows stops the build instead of
silently publishing a name.
"""
import re, sys, io, os, json, shutil, subprocess, zipfile, tempfile

# The names are NOT in this file. This repository is public, and a list of the people the
# public copy withholds would undo the withholding. They live beside the private source, in
# public_cv_redactions.json in the same directory as the .docx (td-resume/cv/), and
# load_redactions() fills these in. Without that file the script refuses to run.
GRAD = UNDER = COMM = COAUTHOR_CITATIONS = None
REDACTIONS = 'public_cv_redactions.json'
COUNTS = {"GRAD": 7, "UNDER": 6, "COMM": 2}   # must match the counts REPL states in prose

def load_redactions(src):
    global GRAD, UNDER, COMM, COAUTHOR_CITATIONS
    p = os.path.join(os.path.dirname(os.path.abspath(src)), REDACTIONS)
    if not os.path.exists(p):
        raise SystemExit(f"FAIL: {p} not found. The names to redact are kept beside the private "
                         "source, never in this public repository -- see README section 3.")
    d = json.load(io.open(p, encoding='utf-8'))
    for key, n in COUNTS.items():
        if len(d[key]) != n:
            raise SystemExit(f"FAIL: {key} lists {len(d[key])} names but REPL says {n}. "
                             "Change the replacement text and COUNTS together.")
    GRAD, UNDER, COMM = d["GRAD"], d["UNDER"], d["COMM"]
    COAUTHOR_CITATIONS = d["COAUTHOR_CITATIONS"]

REPL = {
 "GRAD": ("2009 - 2018",
   "7 graduate students mentored - University of Michigan (4), University of Miami (1, MD/PhD), "
   "Florida International University (1), University College Dublin (1). Names withheld on this "
   "public copy; full CV on request."),
 "UNDER": ("2009 - 2011",
   "6 undergraduate students mentored - University of Miami (5), Miami-Dade Community College (1). "
   "Names withheld on this public copy; full CV on request."),
 "COMM": ("2008 - Present",
   "2 dissertation committees, Committee Member - University of Miami, Department of Chemistry (2). "
   "Names and dissertation titles withheld on this public copy; full CV on request."),
}
NOTE = ("Public copy: student names are withheld and shown as counts. "
        "Full CV on request — tony@tonydefazio.com")

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def rowtext(x): return "".join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', x))

def redact(xml):
    def rows(s): return [(m.start(), m.end(), m.group(0))
                         for m in re.finditer(r'<w:tr\b[\s\S]*?</w:tr>', s)]
    def find_block(s, names):
        rs = rows(s); idx = []
        for n in names:
            hit = [i for i,(a,b,x) in enumerate(rs) if n in rowtext(x)]
            if len(hit) != 1:
                raise SystemExit(f"FAIL: {n!r} matched {len(hit)} rows, expected 1. "
                                 "The CV changed shape -- fix this script before publishing.")
            idx.append(hit[0])
        idx.sort()
        if idx != list(range(idx[0], idx[0]+len(idx))):
            raise SystemExit(f"FAIL: rows for {names[0]!r} block are not contiguous: {idx}")
        return rs, idx[0], idx[-1]

    def build(template, date, body):
        cells = list(re.finditer(r'<w:tc>[\s\S]*?</w:tc>', template))
        assert len(cells) == 2, f"expected 2 cells, got {len(cells)}"
        out = []
        for ci, c in enumerate(cells):
            seg = c.group(0); new = date if ci == 0 else body
            ts = list(re.finditer(r'(<w:t[^>]*>)([^<]*)(</w:t>)', seg))
            assert ts, "no w:t in cell"
            ns = ""; l = 0
            for k, t in enumerate(ts):
                ns += seg[l:t.start()] + t.group(1) + (esc(new) if k == 0 else "") + t.group(3)
                l = t.end()
            out.append((c.start(), c.end(), ns + seg[l:]))
        res = ""; l = 0
        for a, b, seg in out: res += template[l:a] + seg; l = b
        return res + template[l:]

    for key, names in (("COMM", COMM), ("UNDER", UNDER), ("GRAD", GRAD)):
        rs, i0, i1 = find_block(xml, names)
        date, body = REPL[key]
        xml = xml[:rs[i0][0]] + build(rs[i0][2], date, body) + xml[rs[i1][1]:]

    anchor = '<w:br/><w:t>defazio@umich.edu</w:t></w:r>'
    if xml.count(anchor) != 1:
        raise SystemExit("FAIL: header email anchor not found exactly once.")
    rpr = ('<w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
           '<w:i/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr>')
    return xml.replace(anchor,
        anchor + f'<w:r>{rpr}<w:br/><w:t xml:space="preserve">{esc(NOTE)}</w:t></w:r>', 1)

def main(src, outdir):
    load_redactions(src)
    os.makedirs(outdir, exist_ok=True)
    work = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z: z.extractall(work)
    p = os.path.join(work, 'word', 'document.xml')
    # Read fully BEFORE opening for write -- open(...,'w') truncates immediately, and as an
    # argument-position call it would hand redact() an empty file.
    xml = io.open(p, encoding='utf-8').read()
    io.open(p, 'w', encoding='utf-8').write(redact(xml))
    docx = os.path.join(outdir, 'cv_public.docx')
    if os.path.exists(docx): os.remove(docx)
    with zipfile.ZipFile(docx, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(work):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, work))
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless',
                    '--convert-to', 'pdf', '--outdir', outdir, docx], check=True)

    pdf = os.path.join(outdir, 'cv_public.pdf')
    raw = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                         capture_output=True, text=True).stdout

    # pdftotext breaks lines mid-token, so a name can be split by a newline (or by a
    # hyphen + newline) and a naive substring search reports it ABSENT while it is on
    # the page. That is the dangerous direction for a leak check, so normalise first:
    # rejoin hyphenated breaks, then collapse all whitespace to single spaces.
    # Credit to td-resume-08, who hit the same artifact on a chapter DOI.
    def norm(t):
        return re.sub(r'\s+', ' ', re.sub(r'-\s*\n\s*', '-', t.replace('\u00ad', '')))
    txt = norm(raw)

    # Belt and braces: also check the XML the PDF was rendered from. Text extraction can
    # drop or mangle glyphs; the XML is what the document actually says.
    with zipfile.ZipFile(docx) as z:
        xml_text = norm("".join(re.findall(
            r'<w:t[^>]*>([^<]*)</w:t>', z.read('word/document.xml').decode('utf-8'))))

    leaked = sorted({n for n in GRAD + UNDER + COMM
                     if norm(n) in txt or norm(n) in xml_text})
    if leaked: raise SystemExit(f"FAIL: names still present: {leaked}")
    for cite in COAUTHOR_CITATIONS:
        if norm(cite) not in txt:
            raise SystemExit(f"FAIL: co-author citation {cite!r} was lost -- it must survive.")

    # The published header line is load-bearing OUTSIDE this repo: td-resume's claims.yml
    # greps the served PDF for it, so that its checker fails rather than a reader finding
    # out if the un-redacted CV is ever served in its place. Changing NOTE breaks that.
    if "Public copy: student names are withheld" not in txt:
        raise SystemExit("FAIL: the public-copy header line is missing. td-resume's "
                         "cv.published claim greps for it -- do not reword it lightly.")
    print(f"OK  {pdf}  (no student names; co-author citations intact; header line present)")
    shutil.rmtree(work)

if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
