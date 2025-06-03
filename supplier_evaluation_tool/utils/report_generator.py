import google.generativeai as genai
from config.secrets import GEMINI_API_KEY
import pandas as pd
genai.configure(api_key=GEMINI_API_KEY)

def generate_supplier_report(ranked_suppliers, selected_criteria, top_n=3):
    """Generate an AI-powered report analyzing the top suppliers"""
    try:
        # Create Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Get top suppliers
        selected_suppliers = ranked_suppliers.head(top_n)
        
        # Prepare supplier summaries
        supplier_summaries = []
        for idx, row in selected_suppliers.iterrows():
            supplier_info = [f"• {col}: {val}" for col, val in row.items() 
                             if pd.notna(val) and col != 'Supplier_Score']
            supplier_summary = f"Supplier {idx+1}:\n\n" + "\n".join(supplier_info)
            supplier_summaries.append(supplier_summary)
        
        # Join all supplier summaries
        supplier_block = '\n\n'.join(supplier_summaries)
        
        # Format criteria text
        criteria_text = ', '.join(selected_criteria) if selected_criteria else "None (Using AI-powered evaluation)"
        
        # Create Gemini-compatible prompt
        gemini_prompt = f"""**Role**: You are a senior analyst specializing in supplier evaluation and strategic sourcing.
**Evaluation Criteria**: {criteria_text}
**Supplier Data**:
{supplier_block}
---
**Task**:
1. **Comparison Table**:
   - Create a markdown table comparing suppliers against each criterion
   - Use 1-5 rating scale
   - Include weighted/average score
2. **Bar Chart Visualization**:
   - Use text-based bar charts for scores (e.g., '5/5`)
3. **Decision & Justification**:
   - Recommend the best supplier with reasoning
   - Highlight trade-offs and strategic alignment
4. **Pros and Cons**:
   - List exactly 3 pros and 3 cons per supplier
5. **Final Recommendation**:
   - Professional summary with benefits and risks
Format the response using markdown with clear section headings."""
        
        # Generate content with Gemini
        response = model.generate_content(gemini_prompt)
        ai_response = response.text.strip()
        
        # Format final report
        report_lines = []
        for supplier_summary in supplier_summaries:
            report_lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{supplier_summary}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        final_report = "\n".join(report_lines) + "\n\n🏆 GenAI Evaluation:\n" + ai_response
        return final_report
    
    except Exception as e:
        return f"⚠️ Error generating report: {str(e)}"