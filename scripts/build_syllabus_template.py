#!/usr/bin/env python3
"""Build SyllabusTemplate.docx at the repo root: a generic, course-independent
syllabus template that any course folder can copy and adapt.

Follows the exact minimal-OOXML pattern already established in this repo for
comp-175/CourseSyllabus175-Fall2026.docx (see CLAUDE.md's "Writing a .docx in
this repo" note): hand-built with stdlib zipfile only, five parts
([Content_Types].xml, _rels/.rels, docProps/core.xml, word/document.xml,
word/styles.xml, word/_rels/document.xml.rels), Title/Heading1/Heading2/
Normal/ListBullet paragraph styles, plain bordered tables, and bullets as a
literal "•  " prefix on the run text (no numbering.xml part needed).
"""
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

OUT_PATH = "SyllabusTemplate.docx"

# ---------------------------------------------------------------------------
# tiny paragraph/table helpers emitting raw <w:p>/<w:tbl> WordprocessingML
# ---------------------------------------------------------------------------

def esc(s):
    return escape(s, {'"': "&quot;"})


def p(text, style=None, bold=False, italic=False):
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'


def bullet(text, italic=False):
    rpr = "<w:rPr><w:i/></w:rPr>" if italic else ""
    return (
        '<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
        f'<w:r>{rpr}<w:t xml:space="preserve">•  {esc(text)}</w:t></w:r></w:p>'
    )


def heading(text, level=1):
    return p(text, style=f"Heading{level}")


def blank():
    return "<w:p/>"


def table(rows, bold_first_col=False):
    ncols = len(rows[0])
    grid = "".join("<w:gridCol/>" for _ in range(ncols))
    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:color="999999"/>'
        '<w:left w:val="single" w:sz="4" w:color="999999"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="999999"/>'
        '<w:right w:val="single" w:sz="4" w:color="999999"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="999999"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="999999"/>'
        "</w:tblBorders>"
    )
    tr_xml = []
    for ri, row in enumerate(rows):
        tcs = []
        for ci, cell in enumerate(row):
            b = ri == 0 or (bold_first_col and ci == 0)
            run = f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(cell)}</w:t></w:r>' if b \
                else f'<w:r><w:t xml:space="preserve">{esc(cell)}</w:t></w:r>'
            tcs.append(f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr><w:p>{run}</w:p></w:tc>')
        tr_xml.append(f'<w:tr>{"".join(tcs)}</w:tr>')
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>{borders}</w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>{"".join(tr_xml)}</w:tbl>'
    )


# ---------------------------------------------------------------------------
# document body
# ---------------------------------------------------------------------------

parts = []
add = parts.append

add(p("[COURSE CODE] – [Course Title]", style="Title"))
add(p("[Semester] [Year] Syllabus – University of the Pacific"))
add(blank())
add(p(
    "How to use this template: replace every bracketed [PLACEHOLDER] with your "
    "course's real details. Sections marked (institutional – keep as-is) "
    "reflect current University of the Pacific standing policy; only edit them "
    "if the actual policy has changed, don't rephrase them per-course. Delete "
    "the Project section entirely if your course has no semester project. Once "
    "adapted, save a copy into the course's own folder (see "
    "comp-175/CourseSyllabus175-Fall2026.docx for a filled-in example) rather "
    "than editing this template file in place.",
    italic=True,
))
add(blank())

add(table([
    ["Course", "[COURSE CODE]-[SECTION], CRN [CRN]"],
    ["Term", "[Semester] [Year] ([Start Date] – [End Date])"],
    ["Meeting Time", "[Days], [Start Time] – [End Time]"],
    ["Location", "[Building, Room]"],
    ["Credits", "[X.XXX]"],
    ["Prerequisites", "[Prerequisites, or “None”]"],
    ["Instructor", "[Instructor Name], [Office]"],
    ["Email", "[username]@pacific.edu"],
    ["Office Hours", "[Days] [Time], [Office], or Zoom (link on Canvas)"],
    ["Canvas", "pacific.instructure.com/courses/[XXXXXX]"],
]))
add(blank())

add(heading("Course Description"))
add(p("[Two to three sentences describing what the course covers and its overall approach.]"))
add(p("[Topics include: list the major topic areas covered, in one sentence.]"))
add(p("[Optional: note on tools/environment, e.g. required software, local VMs vs. cloud, IDE.]", italic=True))
add(blank())

add(heading("Learning Objectives"))
for i in range(1, 6):
    add(bullet(f"[Learning objective {i}]"))
add(blank())

add(heading("Course Topics"))
for i in range(1, 9):
    add(bullet(f"[Topic {i}]"))
add(blank())

add(heading("Teaching Methodology"))
add(p("[Describe the course format: lecture/lab split, required or optional textbook, "
      "how assignments build on lecture material.]"))
add(blank())

add(heading("Grading"))
add(table([
    ["Component", "Weight"],
    ["[Component 1, e.g. Labs]", "[XX]%"],
    ["[Component 2, e.g. Homework]", "[XX]%"],
    ["[Component 3, e.g. Project]", "[XX]%"],
    ["[Component 4, e.g. Midterm Exam]", "[XX]%"],
    ["[Component 5, e.g. Final Exam]", "[XX]%"],
]))
add(p("[Midterm Exam: date/format. Final Exam: date/format, per Registrar exam schedule.]"))
add(blank())
add(table([
    ["Grade", "Range"],
    ["A", "≥ 93"],
    ["A-", "90–93"],
    ["B+", "87–90"],
    ["B", "83–87"],
    ["B-", "80–83"],
    ["C+", "77–80"],
    ["C", "73–77"],
    ["C-", "70–73"],
    ["D+", "67–70"],
    ["D", "60–67"],
    ["F", "< 60"],
]))
add(p("(Standard department grade scale – adjust only if your course uses a different one.)", italic=True))
add(blank())

add(heading("Policies"))
add(heading("Late Work", level=2))
add(bullet("Under 24 hours late: accepted without penalty."))
add(bullet("1–7 days late: accepted with a 10% penalty."))
add(bullet("Beyond 7 days late: not accepted."))
add(p("(Standing default – adjust only if your course uses a different late policy.)", italic=True))
add(heading("Attendance & Materials", level=2))
add(bullet("[Attendance policy – e.g. “Class attendance is necessary. If you miss a "
           "class, you're responsible for keeping up via Canvas.”]"))
add(bullet("[Textbook: required title/edition, or “No textbook is required for this course.”]"))
add(bullet("[Materials/tools needed – e.g. laptop, specific software, lab environment.]"))
add(blank())

add(heading("AI Use in This Course"))
add(p("We recognize the wide availability and access to various types of AI-based tools. "
      "These tools have many useful applications for aiding student learning, and "
      "AI-based applications will be an increasing part of industry, science, business, "
      "and the arts. On the other hand, AI involvement in student work can interfere "
      "with the genuine and authentic assessment of student learning in some "
      "situations. Therefore, it is necessary to place some limits on the use of "
      "AI-based applications in this course."))
add(p("All assignments in the course will have an indication of the level of AI "
      "involvement or use that is allowable, stated clearly as part of each "
      "assignment. AI usage in this course falls into four broad categories:"))
add(bullet("No limitations – AI tools may be used in any way the student sees as "
           "useful or appropriate. AI usage should be noted and cited according to "
           "established citation standards. However, use of any AI tool is not "
           "required."))
add(bullet("Specific limitations – AI tools may be used in some aspects of an "
           "assignment. These specific cases or tasks will be spelled out in the "
           "instructions to the assignment."))
add(bullet("No AI usage in any form – AI tool or application use is prohibited in "
           "this assignment."))
add(bullet("AI use is required – in these assignments, use of AI tools is the focus "
           "of the assignment and their effective use is part of the assignment "
           "objectives. If a specific AI tool or application is required, access "
           "instructions and links will be provided as part of the assignment."))
add(p("Any assignment instructions which prohibit the use of any outside resources or "
      "help shall be understood to include AI resources in that general prohibition. "
      "Unless an assignment says otherwise, working in groups is permitted, but "
      "submitting the assignment confirms that you personally understand the "
      "material. If you use AI, clearly state which parts of your submission used AI "
      "assistance and which parts you completed without it. Violation of any "
      "restriction on AI use, or undisclosed AI use, is treated as a violation of "
      "academic integrity and sanctioned accordingly."))
add(p("This course does not use AI-detection software. Detection tools are not "
      "reliably accurate, and their errors fall disproportionately on students who "
      "can't afford paid AI tools and on non-native speakers of the language they're "
      "writing in — per Center for Teaching and Learning (CTL) guidance, we don't "
      "consider that an acceptable trade-off."))
add(p("Optional resource: the 2026 Student Guide to Artificial Intelligence "
      "(www.studentguidetoai.org), published by Elon University and the AAC&U, is a "
      "short field guide to working with AI tools thoughtfully – curiosity, "
      "critical evaluation of AI output, deep thinking, creativity, ethics, and related "
      "skills."))
add(p("(Institutional – keep as-is. The four-category framework above is the "
      "“Use Permitted Occasionally” option from the Provost's sample syllabus "
      "language; see documentation/Sample Syllabus Language 7-22-2024.pdf (one level "
      "up from any course folder) for three alternative AI-policy templates if this "
      "one doesn't fit your course — “Use To Be Determined” (co-create the "
      "policy with students in class), “Use Encouraged and Permitted” "
      "(broad, low-restriction use), and “Use Not Permitted” (no AI on "
      "graded work at all). For guidance on designing assignments around whichever "
      "policy you pick — promoting AI literacy vs. motivating AI-unassisted human "
      "effort — see documentation/Rethinking Assignments and AI.pdf.)", italic=True))
add(blank())

add(heading("Academic Integrity & Conduct"))
add(bullet("Recordings: live class sessions may be recorded; participating in class "
           "discussion is consent to being recorded. Access is limited to enrolled "
           "students and faculty."))
add(bullet("Honor Code: act with integrity, encourage academic honesty, and report "
           "suspected violations. Violations are handled by the Office of Student "
           "Conduct and Community Standards."))
add(bullet("Names & pronouns: let the instructor know your preferred name/pronoun at "
           "any point in the semester."))
add(p("(Institutional – keep as-is.)", italic=True))
add(blank())

add(heading("Accommodations & Nondiscrimination"))
add(bullet("Disability accommodations: contact the Office of Services for Students with "
           "Disabilities (SSD, McCaffrey Center Rm 116, ssd@pacific.edu) to register, "
           "request accommodations each semester, and share the Accommodation Request "
           "Letter with the instructor."))
add(bullet("Nondiscrimination: the University does not discriminate in any educational "
           "program or activity on the basis of race, color, national/ethnic origin, "
           "disability, sexual orientation, sex, or age."))
add(p("(Institutional – keep as-is.)", italic=True))
add(blank())

add(heading("Program & University Outcomes"))
add(p("This course contributes to [Program name, e.g. BS Computer Science] program "
      "outcomes ([list 3–5 outcomes]) and to the University's core competencies:"))
add(bullet("Critical Thinking"))
add(bullet("Information Literacy"))
add(bullet("Oral Communication"))
add(blank())

add(heading("Project"))
add(p("(Delete this entire section if the course has no semester project.)", italic=True))
add(p("[One-sentence description of the project and its total weight, e.g. "
      "“One semester-long project (20% project + 10% presentations), run as "
      "milestones:”]"))
add(table([
    ["Milestone", "Due"],
    ["[Milestone 1, e.g. Proposal]", "[Week N – Month Day]"],
    ["[Milestone 2]", "[Week N – Month Day]"],
    ["[Milestone 3]", "[Week N – Month Day]"],
    ["[Final Milestone]", "[Week N – Month Day]"],
]))
add(blank())

add(p("This syllabus is subject to change; the version on Canvas is authoritative."))

body_xml = "".join(parts)

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    f'<w:body>{body_xml}</w:body></w:document>'
)

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120"/></w:pPr>
    <w:rPr><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:pPr><w:ind w:left="360" w:hanging="270"/><w:spacing w:after="60"/></w:pPr>
  </w:style>
</w:styles>'''

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''

package_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''

document_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

core_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>Course Syllabus Template</dc:title>
  <dc:creator>University of the Pacific</dc:creator>
</cp:coreProperties>'''

parts_map = {
    "[Content_Types].xml": content_types_xml,
    "_rels/.rels": package_rels_xml,
    "docProps/core.xml": core_xml,
    "word/document.xml": document_xml,
    "word/styles.xml": styles_xml,
    "word/_rels/document.xml.rels": document_rels_xml,
}

with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for name, content in parts_map.items():
        z.writestr(name, content)

print("wrote", OUT_PATH)

# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------
with zipfile.ZipFile(OUT_PATH) as z:
    bad = z.testzip()
    assert bad is None, f"corrupt member: {bad}"
    for name in z.namelist():
        if name.endswith(".xml") or name.endswith(".rels"):
            ET.fromstring(z.read(name))
print("validated: zip OK, all XML/rels parts well-formed")
