import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import json
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from PyPDF2 import PdfReader

# .env datei laden damit der api key funktioniert
load_dotenv()

PROFILE_DIR = "profiles"

class ApplicationGenerator(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Bewerbungsgenerator Pro")
        
        # hier speichere ich alle felder die ich später brauche
        self.profile_var = tk.StringVar()
        self.eigener_name_var = tk.StringVar()
        self.eigene_strasse_var = tk.StringVar()
        self.eigene_plz_ort_var = tk.StringVar()
        self.eigene_email_var = tk.StringVar()
        self.eigene_telefonnummer_var = tk.StringVar()
        self.firmenname_var = tk.StringVar()
        self.job_titel_var = tk.StringVar()
        self.ansprechpartner_var = tk.StringVar()
        self.quelle_var = tk.StringVar()
        self.firmen_strasse_var = tk.StringVar()
        self.firmen_plz_ort_var = tk.StringVar()
        self.style_prompt_var = tk.StringVar(value="Schreibe professionell und überzeugend.")
        self.salutation_var = tk.StringVar(value="Herr")
        self.signature_path_var = tk.StringVar(value="")
        self.cv_path_var = tk.StringVar(value="")
        self.cv_text = tk.StringVar(value="")

        self.create_widgets()
        self.update_profile_list()
        self.load_placeholders()

    def create_widgets(self):
        main_frame = tb.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # jetzt kommen die ganzen buttons und felder
        tb.Label(main_frame, text="Profil:").grid(row=0, column=0, sticky="w", pady=5)
        self.profile_menu = tb.OptionMenu(main_frame, self.profile_var, "Profil auswählen...", *[], command=self.load_profile)
        self.profile_menu.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        tb.Button(main_frame, text="Neues Profil", command=self.create_new_profile, bootstyle="info-outline").grid(row=0, column=2, padx=5)
        
        user_data_frame = tb.Labelframe(main_frame, text="Ihre Daten", padding=10)
        user_data_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)
        tb.Label(user_data_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(user_data_frame, textvariable=self.eigener_name_var, width=50).grid(row=0, column=1)
        tb.Label(user_data_frame, text="Straße:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(user_data_frame, textvariable=self.eigene_strasse_var).grid(row=1, column=1)
        tb.Label(user_data_frame, text="PLZ & Ort:").grid(row=2, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(user_data_frame, textvariable=self.eigene_plz_ort_var).grid(row=2, column=1)
        tb.Label(user_data_frame, text="E-Mail:").grid(row=3, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(user_data_frame, textvariable=self.eigene_email_var).grid(row=3, column=1)
        tb.Label(user_data_frame, text="Telefon:").grid(row=4, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(user_data_frame, textvariable=self.eigene_telefonnummer_var).grid(row=4, column=1)
        
        company_data_frame = tb.Labelframe(main_frame, text="Firmendaten & Position", padding=10)
        company_data_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        tb.Label(company_data_frame, text="Anrede:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
        salutation_options = ["Frau", "Herr", "Divers/Keine Angabe"]
        tb.OptionMenu(company_data_frame, self.salutation_var, salutation_options[1], *salutation_options).grid(row=0, column=1, sticky="w")
        tb.Label(company_data_frame, text="Nachname Ansprechpartner:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.ansprechpartner_var).grid(row=1, column=1)
        tb.Label(company_data_frame, text="Firma:").grid(row=2, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.firmenname_var, width=50).grid(row=2, column=1)
        tb.Label(company_data_frame, text="Jobtitel:").grid(row=3, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.job_titel_var).grid(row=3, column=1)
        tb.Label(company_data_frame, text="Quelle:").grid(row=4, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.quelle_var).grid(row=4, column=1)
        tb.Label(company_data_frame, text="Straße der Firma:").grid(row=5, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.firmen_strasse_var).grid(row=5, column=1)
        tb.Label(company_data_frame, text="PLZ & Ort der Firma:").grid(row=6, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(company_data_frame, textvariable=self.firmen_plz_ort_var).grid(row=6, column=1)
        
        extras_frame = tb.Labelframe(main_frame, text="Extras", padding=10)
        extras_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        tb.Label(extras_frame, text="KI-Stil Anweisung:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
        tb.Entry(extras_frame, textvariable=self.style_prompt_var, width=60).grid(row=0, column=1, sticky="ew")
        tb.Button(extras_frame, text="Unterschrift hochladen", command=self.upload_signature, bootstyle="secondary").grid(row=1, column=0, pady=5, padx=5)
        self.signature_label = tb.Label(extras_frame, text="Keine Datei ausgewählt")
        self.signature_label.grid(row=1, column=1, sticky="w")
        tb.Button(extras_frame, text="Lebenslauf hochladen", command=self.upload_cv, bootstyle="info").grid(row=2, column=0, pady=5, padx=5)
        self.cv_label = tb.Label(extras_frame, text="Kein Lebenslauf ausgewählt")
        self.cv_label.grid(row=2, column=1, sticky="w")
        
        tb.Button(main_frame, text="Bewerbung generieren & speichern", command=self.generate_application, bootstyle="success").grid(row=4, column=0, columnspan=3, pady=20)
        main_frame.columnconfigure(1, weight=1)

    def load_placeholders(self):
        self.eigener_name_var.set("Nassim Soultana")
        self.eigene_strasse_var.set("Höxterstr. 8")
        self.eigene_plz_ort_var.set("58135 Hagen")
        self.eigene_email_var.set("nassimsoultana72@gmail.com")
        self.eigene_telefonnummer_var.set("01520 9031969")
        self.firmenname_var.set("Trinkgut GmbH")
        self.job_titel_var.set("Kassierer")
        self.ansprechpartner_var.set("Essert")
        self.salutation_var.set("Herr")
        self.quelle_var.set("Ihre Karriereseite")
        self.firmen_strasse_var.set("Poststraße 13")
        self.firmen_plz_ort_var.set("58099 Hagen")

    def upload_signature(self):
        file_path = filedialog.askopenfilename(title="Unterschrift auswählen", filetypes=[("Bilddateien", "*.png *.jpg *.jpeg"), ("Alle Dateien", "*.*")])
        if file_path:
            self.signature_path_var.set(file_path)
            self.signature_label.config(text=os.path.basename(file_path))

    def upload_cv(self):
        file_path = filedialog.askopenfilename(title="Lebenslauf auswählen", filetypes=[("PDF Dateien", "*.pdf"), ("Textdateien", "*.txt"), ("Alle Dateien", "*.*")])
        if not file_path: return
        
        self.cv_path_var.set(file_path)
        self.cv_label.config(text=os.path.basename(file_path))
        
        try:
            text = ""
            if file_path.lower().endswith(".pdf"):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text: text += page_text + "\n"
            elif file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f: text = f.read()
            
            self.cv_text.set(text)
            if text: messagebox.showinfo("Erfolg", "Lebenslauf wurde erfolgreich eingelesen.")
            else: messagebox.showwarning("Warnung", "Dokument gelesen, aber kein Text gefunden. (Möglicherweise ein reines Bild-PDF)")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Lesen des Lebenslaufs: {e}")
            self.cv_text.set("")

    def create_pdf(self, filename, text_content):
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2.5*cm, leftMargin=2.5*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Bold', fontName='Helvetica-Bold'))
        story = []
        parts = text_content.split('---')
        sender_block_str, recipient_block_str, date_str, subject_str, body_str = parts
        story.append(Paragraph(sender_block_str.strip().replace('\n', '<br/>'), styles['RightAlign']))
        story.append(Spacer(1, 1.5*cm))
        story.append(Paragraph(recipient_block_str.strip().replace('\n', '<br/>'), styles['Normal']))
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(date_str.strip(), styles['RightAlign']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(subject_str.strip(), styles['Bold']))
        story.append(Spacer(1, 1*cm))
        main_body = body_str.split("Mit freundlichen Grüßen,")[0].strip().replace('\n\n', '<br/><br/>')
        story.append(Paragraph(main_body, styles['Normal']))
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("Mit freundlichen Grüßen,", styles["Normal"]))
        story.append(Spacer(1, 0.5*cm))
        signature_path = self.signature_path_var.get()
        if signature_path and os.path.exists(signature_path):
            try:
                img = Image(signature_path, width=4*cm, height=1.5*cm, kind='proportional')
                img.hAlign = 'LEFT'
                story.append(img)
            except Exception as e:
                print(f"Fehler beim Laden des Bildes: {e}")
                story.append(Spacer(1, 2*cm)) 
        else:
            story.append(Spacer(1, 2.5*cm))
        doc.build(story)

    def create_cover_letter_text(self):
        salutation_choice = self.salutation_var.get()
        ansprechpartner_name = self.ansprechpartner_var.get().strip()
        
        anrede = ""
        if ansprechpartner_name:
            if salutation_choice == "Frau": anrede = f"Sehr geehrte Frau {ansprechpartner_name},"
            elif salutation_choice == "Herr": anrede = f"Sehr geehrter Herr {ansprechpartner_name},"
            else: anrede = f"Guten Tag {ansprechpartner_name},"
        else: anrede = "Sehr geehrte Damen und Herren,"
        
        heute = datetime.date.today().strftime("%d. %B %Y")
        ort = self.eigene_plz_ort_var.get().split(" ", 1)[-1] if " " in self.eigene_plz_ort_var.get() else "Ihre Stadt"
        
        sender_block = (f"{self.eigener_name_var.get()}\n{self.eigene_plz_ort_var.get()}\n{self.eigene_strasse_var.get()}\n"
                        f"{self.eigene_email_var.get()}\n{self.eigene_telefonnummer_var.get()}")
        
        recipient_lines = [self.firmenname_var.get()]
        if ansprechpartner_name:
            if salutation_choice in ["Frau", "Herr"]: recipient_lines.append(f"z.H. {salutation_choice} {ansprechpartner_name}")
            else: recipient_lines.append(f"z.H. {ansprechpartner_name}")
        recipient_lines.append(self.firmen_strasse_var.get())
        recipient_lines.append(self.firmen_plz_ort_var.get())
        recipient_block = "\n".join(recipient_lines)
        
        date_block = f"{ort}, den {heute}"
        subject_block = f"Bewerbung als {self.job_titel_var.get()}"
        body_block = (f"{anrede}\n\nmit großem Interesse habe ich auf {self.quelle_var.get()} Ihre Stellenanzeige gelesen und bewerbe mich hiermit auf die ausgeschriebene Position.\n\n"
                      f"[PLATZHALTER_KI_TEXT]\n\n"
                      "Ich bin überzeugt, dass meine Fähigkeiten und meine Motivation eine wertvolle Ergänzung für Ihr Team wären.\n\n"
                      "Gerne überzeuge ich Sie in einem persönlichen Gespräch von meinen Stärken. Über eine Einladung zu einem Vorstellungsgespräch würde ich mich sehr freuen.\n\n"
                      "Mit freundlichen Grüßen,")
        return f"{sender_block}---{recipient_block}---{date_block}---{subject_block}---{body_block}"

    def generate_gpt_text(self, job_titel, firmenname, custom_style, cv_content):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            if not client.api_key: raise ValueError("OpenAI API key not found. Please check your .env file.")
            
            if not cv_content:
                prompt = (f"Schreibe einen kurzen, überzeugenden Absatz für ein deutsches Bewerbungsschreiben. Position: '{job_titel}', Firma: '{firmenname}'. Stil-Anweisung: '{custom_style}'. Betone die Motivation und Flexibilität eines Studenten. Schreibe nur den Absatz, ohne Anrede oder Grußformel.")
            else:
                prompt = f"""Erstelle einen überzeugenden Absatz für ein deutsches Bewerbungsschreiben. Rolle des Bewerbers: Student. Position: '{job_titel}'. Firma: '{firmenname}'. Gewünschter Stil: '{custom_style}'. Hier ist der Lebenslauf des Bewerbers zur Analyse: --- {cv_content} --- Deine Aufgabe: Nutze die Informationen aus dem Lebenslauf, um den Absatz maximal zu personalisieren. Gehe auf 1-2 relevante Fähigkeiten oder Erfahrungen aus dem Lebenslauf ein, die besonders gut zur Position '{job_titel}' passen. Verknüpfe diese mit der Motivation, bei '{firmenname}' zu arbeiten. Schreibe nur den finalen Absatz, ohne Anrede, Grußformel oder Erklärungen."""

            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=300)
            return response.choices[0].message.content.strip()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Generieren des Textes: {e}")
            return "[Fehler bei der KI-Textgenerierung]"

    def sanitize_filename(self, name):
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n']
        for char in invalid_chars: name = name.replace(char, '')
        return name

    def generate_application(self):
        firmenname = self.firmenname_var.get().strip()
        job_titel = self.job_titel_var.get().strip()
        
        if not firmenname or not job_titel:
            messagebox.showwarning("Warnung", "Bitte Firmenname und Jobtitel ausfüllen.")
            return
        
        cv_content = self.cv_text.get()
        if not cv_content: messagebox.showwarning("Hinweis", "Kein Lebenslauf hochgeladen. Text wird ohne Personalisierung erstellt.")

        raw_text_with_separator = self.create_cover_letter_text()
        custom_style = self.style_prompt_var.get()
        gpt_text = self.generate_gpt_text(job_titel, firmenname, custom_style, cv_content)
        
        if gpt_text is None: # falls irgendwas schiefgelaufen ist
            messagebox.showerror("Fehler", "Die KI konnte keinen Text generieren.")
            return

        final_text = raw_text_with_separator.replace("[PLATZHALTER_KI_TEXT]", gpt_text)
        
        try:
            sanitized_firmenname = self.sanitize_filename(firmenname.replace(' ', '_'))
            sanitized_job_titel = self.sanitize_filename(job_titel.replace(' ', '_'))
            base_filename = f"Bewerbung_{sanitized_firmenname}_{sanitized_job_titel}"
            
            final_text_for_txt = final_text.replace('---', '\n\n')
            txt_filename = f"{base_filename}.txt"
            with open(txt_filename, "w", encoding="utf-8") as f: f.write(final_text_for_txt)
            
            pdf_filename = f"{base_filename}.pdf"
            self.create_pdf(pdf_filename, final_text)
            
            messagebox.showinfo("Erfolg", f"Bewerbung wurde als '{txt_filename}' und '{pdf_filename}' gespeichert.")
        except Exception as e: messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def save_profile(self, profile_name):
        if not os.path.exists(PROFILE_DIR): os.makedirs(PROFILE_DIR)
        user_data = {
            "eigener_name": self.eigener_name_var.get(),
            "eigene_strasse": self.eigene_strasse_var.get(),
            "eigene_plz_ort": self.eigene_plz_ort_var.get(),
            "eigene_email": self.eigene_email_var.get(),
            "eigene_telefonnummer": self.eigene_telefonnummer_var.get()
        }
        profile_path = os.path.join(PROFILE_DIR, f"{profile_name}.json")
        try:
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4)
            messagebox.showinfo("Erfolg", f"Profil '{profile_name}' wurde gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Profils: {e}")

    def load_profile(self, profile_name):
        profile_path = os.path.join(PROFILE_DIR, f"{profile_name}.json")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                self.eigener_name_var.set(user_data.get("eigener_name", ""))
                self.eigene_strasse_var.set(user_data.get("eigene_strasse", ""))
                self.eigene_plz_ort_var.set(user_data.get("eigene_plz_ort", ""))
                self.eigene_email_var.set(user_data.get("eigene_email", ""))
                self.eigene_telefonnummer_var.set(user_data.get("eigene_telefonnummer", ""))
            self.profile_var.set(profile_name)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden des Profils: {e}")

    def update_profile_list(self):
        if not os.path.exists(PROFILE_DIR): os.makedirs(PROFILE_DIR)
        profiles = [f.split(".json")[0] for f in os.listdir(PROFILE_DIR) if f.endswith(".json")]
        menu = self.profile_menu["menu"]
        menu.delete(0, "end")
        for profile in profiles:
            menu.add_command(label=profile, command=lambda p=profile: self.load_profile(p))
        if not profiles:
            menu.add_command(label="Keine Profile gefunden", state="disabled")

    def create_new_profile(self):
        profile_name = simpledialog.askstring("Neues Profil", "Geben Sie einen Namen für das neue Profil ein:")
        if profile_name:
            self.save_profile(profile_name)
            self.update_profile_list()
            self.profile_var.set(profile_name)

if __name__ == "__main__":
    app = ApplicationGenerator()
    app.mainloop()