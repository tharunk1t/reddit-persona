from fpdf import FPDF
import markdown

class PDF(FPDF):
    def write_html(self, html_text):
        for line in html_text.split("<br />"):
            self.multi_cell(0, 10, line.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", ""))

def export_persona_to_pdf(persona_md, filename="persona_output.pdf"):
    html = markdown.markdown(persona_md)
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.write_html(html)
    pdf.output(filename)
    return filename
