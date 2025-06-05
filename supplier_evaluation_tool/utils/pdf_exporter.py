from fpdf import FPDF
import os
import io
import matplotlib.pyplot as plt

def create_pdf(text_content, selected_criteria, chart_fig=None):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Add text content to PDF
        for line in text_content.split('\n'):
            try:
                pdf.multi_cell(0, 10, line.encode('latin-1', 'ignore').decode('latin-1'))
            except UnicodeEncodeError:
                continue
        
        # Add chart if available
        if chart_fig is not None:
            temp_chart_path = "temp_chart.png"
            chart_fig.savefig(temp_chart_path, dpi=200, bbox_inches='tight')
            
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            
            if selected_criteria:
                pdf.cell(0, 10, "Supplier Comparison Chart", ln=True, align='C')
            else:
                pdf.cell(0, 10, "Primary Attribute Comparison", ln=True, align='C')
            
            pdf.ln(5)
            available_width = pdf.w - 20
            pdf.image(temp_chart_path, x=10, y=pdf.get_y(), w=available_width)
            
            # Clean up temporary file
            if os.path.exists(temp_chart_path):
                os.remove(temp_chart_path)
        
        # Save PDF to buffer
        pdf_buffer = io.BytesIO()
        temp_pdf_path = "temp_report.pdf"
        pdf.output(temp_pdf_path)
        
        with open(temp_pdf_path, "rb") as f:
            pdf_buffer.write(f.read())
        
        # Clean up temporary PDF
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        
        pdf_buffer.seek(0)
        return pdf_buffer
    
    except Exception as e:
        return None
