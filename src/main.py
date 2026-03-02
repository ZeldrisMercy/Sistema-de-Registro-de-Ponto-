import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime, time
import re
import os
import sys
from fpdf import FPDF

# --- UI DESIGN SYSTEM ---
ctk.set_appearance_mode("Dark")
COR_FUNDO = "#0B0E14"
COR_CARD = "#161B22"
COR_ACCENT = "#58A6FF"
COR_SUCCESS = "#238636"
COR_DANGER = "#DA3633"

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def formatar_tempo(minutos_totais):
    if pd.isna(minutos_totais) or minutos_totais <= 0: return "00:00"
    h = int(minutos_totais // 60)
    m = int(minutos_totais % 60)
    return f"{h:02d}:{m:02d}"

def extrair_minutos(val):
    if isinstance(val, (time, datetime)): return val.hour * 60 + val.minute
    val_str = str(val).strip()
    match = re.search(r'\b([0-1]?[0-9]|2[0-3]):([0-5][0-9])\b', val_str)
    if match: return int(match.group(1)) * 60 + int(match.group(2))
    return None

class AppPonto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ponto AMAN - Leitor ZKTeco/Henry")
        self.geometry("1300x850")
        self.configure(fg_color=COR_FUNDO)
        
        self.caminho_arquivo = ""
        self.dados_finais = pd.DataFrame()
        self.regras_semana = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR (CONFIGURAÇÃO DOS 7 DIAS) =================
        self.sidebar = ctk.CTkFrame(self, width=420, corner_radius=0, fg_color=COR_CARD)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="REGRAS DA SEMANA", font=("Inter", 20, "bold"), text_color=COR_ACCENT).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self.sidebar, label_text="CONFIGURAÇÃO POR DIA", fg_color="transparent")
        self.scroll.pack(expand=True, fill="both", padx=10, pady=5)

        self.dias_ui = {}
        nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
        # Pré-configurando com os horários oficiais da AMAN
        for i, n in enumerate(nomes_dias):
            padrao_in, padrao_out = "07:00", "17:00"
            aberto = True
            if i == 4: # Sexta-feira
                padrao_out = "16:00"
            elif i >= 5: # Sábado e Domingo
                aberto = False
                
            self.criar_card_dia(n, i, aberto, padrao_in, padrao_out)

        ctk.CTkButton(self.sidebar, text="SALVAR REGRAS DE CÁLCULO", height=40, fg_color=COR_SUCCESS, text_color="white", font=("Inter", 13, "bold"), command=self.salvar_configs).pack(pady=20, padx=40, fill="x")

        # ================= MAIN PANEL =================
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self.main, fg_color=COR_CARD, corner_radius=12)
        header.pack(fill="x", pady=(0, 20))
        
        self.btn_sel = ctk.CTkButton(header, text="📁 ABRIR RELATÓRIO DO SISTEMA", height=45, fg_color=COR_ACCENT, text_color="black", font=("Inter", 13, "bold"), command=self.selecionar)
        self.btn_sel.pack(side="left", padx=20, pady=20)
        
        self.btn_calc = ctk.CTkButton(header, text="⚡ CALCULAR PONTO", height=45, fg_color=COR_SUCCESS, text_color="white", font=("Inter", 13, "bold"), state="disabled", command=self.processar_aman)
        self.btn_calc.pack(side="right", padx=20, pady=20)

        # TABS E TABELA
        self.tabs = ctk.CTkTabview(self.main, fg_color=COR_CARD)
        self.tabs.pack(expand=True, fill="both")
        self.tabs.add("Relatório")
        self.tabs.add("Tabela")

        self.txt = ctk.CTkTextbox(self.tabs.tab("Relatório"), font=("Consolas", 14), fg_color="#0D1117", text_color="#A5D6FF")
        self.txt.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree = ttk.Treeview(self.tabs.tab("Tabela"), columns=("N", "T", "HN", "HE"), show="headings")
        for c, h in zip(("N", "T", "HN", "HE"), ("FUNCIONÁRIO", "TOTAL", "NORMAIS", "EXTRAS")):
            self.tree.heading(c, text=h); self.tree.column(c, anchor="center")
        self.tree.pack(expand=True, fill="both")

        self.btn_xls = ctk.CTkButton(self.main, text="EXPORTAR EXCEL", height=40, fg_color="transparent", border_width=2, border_color=COR_ACCENT, state="disabled", command=self.export_excel)
        self.btn_xls.pack(pady=(15,0), side="right")

    def add_field(self, master, label, default, side):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(side=side, expand=True, fill="x", padx=5)
        ctk.CTkLabel(f, text=label, font=("Inter", 11)).pack(anchor="w")
        e = ctk.CTkEntry(f, height=35); e.insert(0, default); e.pack(fill="x")
        return e

    def criar_card_dia(self, nome, idx, aberto, h_in, h_out):
        f = ctk.CTkFrame(self.scroll, fg_color="#1C2128", corner_radius=8)
        f.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(f, text=nome.upper(), font=("Inter", 11, "bold"), text_color=COR_ACCENT).grid(row=0, column=0, padx=10, sticky="w")
        
        v_on = ctk.BooleanVar(value=aberto)
        cb_on = ctk.CTkCheckBox(f, text="Aberto", variable=v_on, font=("Inter", 11))
        cb_on.grid(row=1, column=0, padx=10, pady=5)
        
        f_exc = ctk.CTkFrame(f, fg_color="transparent")
        e_in = self.add_field(f_exc, "Início:", h_in, "left")
        e_out = self.add_field(f_exc, "Fim:", h_out, "right")
        
        def up():
            if v_on.get(): f_exc.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            else: f_exc.grid_remove()
            
        cb_on.configure(command=up); up()
        self.dias_ui[idx] = {"on": v_on, "in": e_in, "out": e_out}

    def salvar_configs(self):
        for i in range(7):
            cfg = self.dias_ui[i]
            self.regras_semana[i] = {
                "aberto": cfg["on"].get(), 
                "ref_inicio": extrair_minutos(cfg["in"].get()), 
                "ref_fim": extrair_minutos(cfg["out"].get())
            }
        messagebox.showinfo("Sucesso", "Regras da semana salvas e prontas para cálculo!")

    def selecionar(self):
        p = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if p: 
            self.caminho_arquivo = p
            self.btn_calc.configure(state="normal")

    def processar_aman(self):
        if not self.regras_semana: self.salvar_configs()
        
        try:
            xls = pd.ExcelFile(self.caminho_arquivo)
            
            # 1. Procura especificamente pela aba de Estatísticas
            nome_aba = None
            for aba in xls.sheet_names:
                if 'anomalia' in aba.lower() or 'anomaly' in aba.lower():
                    nome_aba = aba; break
            
            # Fallback caso o nome mude: tenta a 3ª aba
            if not nome_aba and len(xls.sheet_names) >= 3: nome_aba = xls.sheet_names[2]
            elif not nome_aba: nome_aba = xls.sheet_names[0]

            # Lendo a planilha (Ignorando o cabeçalho do sistema ZKTeco)
            df = pd.read_excel(xls, sheet_name=nome_aba, skiprows=3)
            
            # Remapeando colunas
            colunas = list(df.columns)
            if len(colunas) < 8:
                raise ValueError("O formato não é o padrão de Estatísticas de Anomalia (faltam colunas).")
            colunas[0:8] = ['ID', 'Nome', 'Dept', 'Data', 'P1_In', 'P1_Out', 'P2_In', 'P2_Out']
            df.columns = colunas
            
            # Filtro de funcionários reais
            df = df[pd.to_numeric(df['ID'], errors='coerce').notnull()]
            resultados = []

            for _, row in df.iterrows():
                try:
                    data_dt = pd.to_datetime(row['Data'], dayfirst=True)
                    dia_idx = data_dt.weekday()
                except: continue

                # Captura P1_In, P1_Out, P2_In, P2_Out
                batidas = []
                for col in ['P1_In', 'P1_Out', 'P2_In', 'P2_Out']:
                    m = extrair_minutos(row[col])
                    if m is not None: batidas.append(m)

                if not batidas: continue

                # MATEMÁTICA CIRÚRGICA DE INTERSECÇÃO (O que salvou o sistema)
                entrada = min(batidas)
                saida = max(batidas)
                total_dia = saida - entrada

                regra_dia = self.regras_semana.get(dia_idx)
                
                if not regra_dia["aberto"]:
                    normais, extras = 0, total_dia
                else:
                    ref_inicio = regra_dia["ref_inicio"]
                    ref_fim = regra_dia["ref_fim"]
                    
                    inicio_normal = max(entrada, ref_inicio)
                    fim_normal = min(saida, ref_fim)
                    
                    normais = max(0, fim_normal - inicio_normal)
                    extras = total_dia - normais

                resultados.append({"Nome": str(row['Nome']).strip(), "Tot": total_dia, "Norm": normais, "Ext": extras})

            if not resultados:
                raise ValueError("Nenhum ponto válido encontrado nesta aba.")

            # Consolidando o Mês
            df_res = pd.DataFrame(resultados).groupby('Nome').sum().reset_index()
            
            self.tree.delete(*self.tree.get_children())
            txt_rel = f"RELATÓRIO MENSAL - AMAN LOCAÇÕES E REMOÇÕES\nData de Geração: {datetime.now().strftime('%d/%m/%Y')}\n" + "="*55 + "\n"
            
            for _, r in df_res.iterrows():
                v = (r['Nome'].upper(), formatar_tempo(r['Tot']), formatar_tempo(r['Norm']), formatar_tempo(r['Ext']))
                self.tree.insert("", "end", values=v)
                txt_rel += f"👤 {v[0]}\n   TOTAL TRABALHADO: {v[1]} | NORMAIS: {v[2]} | EXTRAS: {v[3]}\n" + "-"*55 + "\n"
            
            self.dados_finais = df_res
            self.txt.configure(state="normal"); self.txt.delete("0.0", "end"); self.txt.insert("0.0", txt_rel); self.txt.configure(state="disabled")
            self.btn_xls.configure(state="normal"); self.tabs.set("Relatório")

        except Exception as e:
            messagebox.showerror("Erro Estrutural", f"Erro na leitura da planilha:\n{str(e)}\n\nCertifique-se de exportar o arquivo contendo a aba 'Estatísticas de anomalia'.")

    def export_excel(self):
        c = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="Resumo_Mensal_AMAN.xlsx")
        if c:
            df_export = self.dados_finais.copy()
            df_export['Total_Formatado'] = df_export['Tot'].apply(formatar_tempo)
            df_export['Normais_Formatado'] = df_export['Norm'].apply(formatar_tempo)
            df_export['Extras_Formatado'] = df_export['Ext'].apply(formatar_tempo)
            df_export[['Nome', 'Total_Formatado', 'Normais_Formatado', 'Extras_Formatado']].rename(columns={'Total_Formatado': 'Total', 'Normais_Formatado': 'Normais', 'Extras_Formatado': 'Extras'}).to_excel(c, index=False)
            messagebox.showinfo("Sucesso", "Planilha exportada com sucesso!")

if __name__ == "__main__":
    AppPonto().mainloop()
