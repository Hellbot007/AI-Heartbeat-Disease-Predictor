import pandas as pd
from docx import Document

def update_document(doc_path, csv_path, out_path):
    df = pd.read_csv(csv_path)
    
    # Create a dictionary for easy lookup
    models_data = {}
    for _, row in df.iterrows():
        models_data[row['Model']] = row

    doc = Document(doc_path)
    
    for table in doc.tables:
        # Some tables might not have headers or might be empty
        if not table.rows:
            continue
            
        header = [cell.text.strip() for cell in table.rows[0].cells]
        
        for row in table.rows[1:]:
            cell_texts = [cell.text.strip() for cell in row.cells]
            if not cell_texts:
                continue
                
            first_col = cell_texts[0]
            
            # Find which model this row is about
            matched_model = None
            for csv_model, df_row in models_data.items():
                if csv_model in first_col or first_col in csv_model:
                    matched_model = csv_model
                    break
            
            if matched_model:
                data = models_data[matched_model]
                
                # Check header to know what to update
                if "Train Acc." in header or "Train Acc" in header:
                    # Likely Table 3 or 5
                    train_acc_idx = header.index("Train Acc.") if "Train Acc." in header else header.index("Train Acc")
                    test_acc_idx = header.index("Test Acc.") if "Test Acc." in header else header.index("Test Acc")
                    
                    # F1 Macro
                    f1_macro_idx = None
                    if "F1 Macro" in header:
                        f1_macro_idx = header.index("F1 Macro")
                        
                    # F1 Weighted
                    f1_wt_idx = None
                    if "F1 Weighted" in header:
                        f1_wt_idx = header.index("F1 Weighted")
                    elif "F1 Wt." in header:
                        f1_wt_idx = header.index("F1 Wt.")

                    # Update cells
                    row.cells[train_acc_idx].text = f"{data['Train Acc']*100:.2f}%"
                    row.cells[test_acc_idx].text = f"{data['Test Acc']*100:.2f}%"
                    if f1_macro_idx is not None: row.cells[f1_macro_idx].text = f"{data['F1 Macro']:.4f}"
                    if f1_wt_idx is not None: row.cells[f1_wt_idx].text = f"{data['F1 Wt']:.4f}"
                    
                    # Specific to Table 5
                    if "TP" in header and "FP / FN" in header:
                        tp_idx = header.index("TP")
                        fp_fn_idx = header.index("FP / FN")
                        row.cells[tp_idx].text = f"{int(data['TP']):,}"
                        row.cells[fp_fn_idx].text = f"{int(data['FP'])} FP / {int(data['FN'])} FN"
                        
                    if "Time (s)" in header:
                        time_idx = header.index("Time (s)")
                        row.cells[time_idx].text = f"{data['Train Time']:.4f}s"
                        
                elif "TN (Healthy→Healthy)" in header:
                    # Table 6
                    tn_idx = header.index("TN (Healthy→Healthy)")
                    fp_idx = header.index("FP (Healthy→Disease)")
                    fn_idx = header.index("FN (Disease→Healthy)")
                    tp_idx = header.index("TP (Disease→Disease)")
                    
                    row.cells[tn_idx].text = f"{int(data['TN'])}"
                    row.cells[fp_idx].text = f"{int(data['FP'])}"
                    row.cells[fn_idx].text = f"{int(data['FN'])}"
                    row.cells[tp_idx].text = f"{int(data['TP']):,}"
                    
                elif "P (C0)" in header:
                    # Table 7
                    row.cells[header.index("P (C0)")].text = f"{data['P (C0)']:.2f}"
                    row.cells[header.index("R (C0)")].text = f"{data['R (C0)']:.2f}"
                    row.cells[header.index("F1 (C0)")].text = f"{data['F1 (C0)']:.2f}"
                    row.cells[header.index("P (C1)")].text = f"{data['P (C1)']:.2f}"
                    row.cells[header.index("R (C1)")].text = f"{data['R (C1)']:.2f}"
                    row.cells[header.index("F1 (C1)")].text = f"{data['F1 (C1)']:.2f}"
                    row.cells[header.index("Macro F1")].text = f"{data['F1 Macro']:.4f}"
                    row.cells[header.index("Wt. F1")].text = f"{data['F1 Wt']:.4f}"
                    
                elif "Training Time" in header and "Inference Speed" in header:
                    # Table 8
                    time_idx = header.index("Training Time")
                    row.cells[time_idx].text = f"{data['Train Time']:.4f} seconds"

    doc.save(out_path)
    print("Successfully updated document at", out_path)

if __name__ == "__main__":
    update_document("AI_Heartbeat_Disease_Predictor_Report (1).docx", "tmp/model_results.csv", "AI_Heartbeat_Disease_Predictor_Report_Updated.docx")
