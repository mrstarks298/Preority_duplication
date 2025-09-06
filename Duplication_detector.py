import pandas as pd
import re
import os
import numpy as np
from datetime import datetime

class QuestionProcessor:
    """
    End-to-End Question Deduplication and Priority Mapping Pipeline
    """

    def __init__(self):
        self.priority_labels = {
            1: 'JEE Advanced',
            2: 'JEE Mains',
            3: 'NCERT',
            4: 'Plain/Other'
        }

    def extract_question_id(self, question_text):
        """Extract 24-char Question ID"""
        if pd.isna(question_text):
            return None
        question_str = str(question_text)
        id_match = re.search(r'Question ID[:\s]*([a-f0-9]{24})', question_str, re.IGNORECASE)
        return id_match.group(1) if id_match else None

    def get_priority(self, question_text):
        """Assign priority based on keywords"""
        if pd.isna(question_text):
            return 4
        text = str(question_text).lower()
        if any(p in text for p in ['jee advanced', 'jee adv', 'advanced']):
            return 1
        elif any(p in text for p in ['jee main', 'jee mains', 'mains']):
            return 2
        elif 'ncert' in text:
            return 3
        return 4

    def convert_xlsx_to_csv(self, file_path):
        """Convert Excel to CSV"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.xlsx':
            df = pd.read_excel(file_path)
            csv_path = file_path.replace('.xlsx', '.csv')
            df.to_csv(csv_path, index=False)
            print(f"Converted {file_path} → {csv_path}")
            return df
        elif ext == '.csv':
            return pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format!")

    def process_duplicates(self, file_path):
        """Process duplicate pairs & select final questions"""
        df = self.convert_xlsx_to_csv(file_path)
        print(f"Loaded {len(df)} duplicate pairs")

        results = []
        for _, row in df.iterrows():
            q1_id, q2_id = self.extract_question_id(row['question_1']), self.extract_question_id(row['question_2'])
            q1_p, q2_p = self.get_priority(row['question_1']), self.get_priority(row['question_2'])

            if q1_id and q2_id:
                if q1_p <= q2_p:
                    sel, rej, sp, rp, chosen = q1_id, q2_id, q1_p, q2_p, "question_1"
                else:
                    sel, rej, sp, rp, chosen = q2_id, q1_id, q2_p, q1_p, "question_2"

                results.append({
                    'selected_question_id': sel,
                    'rejected_question_id': rej,
                    'selected_priority': sp,
                    'rejected_priority': rp,
                    'chosen': chosen
                })

        results_df = pd.DataFrame(results).drop_duplicates(subset=['selected_question_id'])
        results_df.to_csv("final_selection_questions.csv", index=False)
        print(f"✓ Created final_selection_questions.csv ({len(results_df)} unique selections)")
        return results_df

    def create_priority_mapping(self, results_df):
        """Create priority mappings"""
        mapping = results_df[['selected_question_id', 'selected_priority']].copy()
        mapping.rename(columns={'selected_question_id': 'question_id', 'selected_priority': 'priority'}, inplace=True)
        mapping['priority_label'] = mapping['priority'].map(self.priority_labels)
        mapping.to_csv("question_id_priority_mapping.csv", index=False)
        print("✓ Created question_id_priority_mapping.csv")
        return mapping

    def validate_and_report(self, results_df):
        """Validate outputs and generate consolidated report"""
        print("\nVALIDATION & SUMMARY")
        print("="*60)

        # Priority distribution
        print("\nPriority Distribution:")
        dist = results_df['selected_priority'].value_counts().sort_index()
        for p, c in dist.items():
            print(f"  {self.priority_labels[p]}: {c} questions")

        # Final consolidated report
        consolidated = results_df.copy()
        consolidated['priority_label'] = consolidated['selected_priority'].map(self.priority_labels)
        consolidated['processing_date'] = datetime.now().strftime("%Y-%m-%d")
        consolidated.to_csv("final_consolidated_question_report.csv", index=False)

        print("\n✓ Created final_consolidated_question_report.csv")
        return consolidated

def main(file_path="Duplicate_Detection_Report.xlsx"):
    qp = QuestionProcessor()
    results = qp.process_duplicates(file_path)
    qp.create_priority_mapping(results)
    qp.validate_and_report(results)
    print("\n✅ All processing completed successfully!")

if __name__ == "__main__":
    main()
