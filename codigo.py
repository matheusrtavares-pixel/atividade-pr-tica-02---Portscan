import socket
import time
import customtkinter as ctk
from tkinter import messagebox, filedialog

# Configuração de Aparência Avançada
ctk.set_appearance_mode("Dark")

class CyberScanPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações de Janela Elegante
        self.title("⚡ CYBERSCAN - matheusrangel")
        self.geometry("850x600")
        self.resizable(False, False)
        
        self.resultados_salvar = []

        # Configuração do Layout de Grid (Painel Lateral + Painel Principal)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =================================================================
        # 1. PAINEL LATERAL (SIDEBAR - CONTROLES DE CONFIGURAÇÃO)
        # =================================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#111217")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="⚡ CYBERSCAN", font=ctk.CTkFont(family="Courier", size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        self.subtitle_label = ctk.CTkLabel(self.sidebar_frame, text="Auditoria de Rede v3.0", font=ctk.CTkFont(size=11), text_color="gray")
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # Inputs dentro do Painel Lateral
        self.ip_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="IP do Alvo (Ex: 127.0.0.1)", width=220, height=35, font=ctk.CTkFont(family="Courier"))
        self.ip_entry.grid(row=2, column=0, padx=20, pady=10)

        # Range de portas compacto
        self.port_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.port_frame.grid(row=3, column=0, padx=20, pady=10)
        
        self.port_start = ctk.CTkEntry(self.port_frame, placeholder_text="Porta Inicial", width=105, height=35, font=ctk.CTkFont(family="Courier"))
        self.port_start.grid(row=0, column=0, padx=(0, 5))
        
        self.port_end = ctk.CTkEntry(self.port_frame, placeholder_text="Porta Final", width=105, height=35, font=ctk.CTkFont(family="Courier"))
        self.port_end.grid(row=0, column=1, padx=(5, 0))

        # Botões de Ação no rodapé do menu lateral
        self.btn_scan = ctk.CTkButton(self.sidebar_frame, text="INICIAR SCAN", font=ctk.CTkFont(weight="bold"), fg_color="#1a73e8", hover_color="#155cb4", height=40, command=self.start_scan)
        self.btn_scan.grid(row=5, column=0, padx=20, pady=10)

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="EXPORTAR CSV", font=ctk.CTkFont(weight="bold"), fg_color="#2da755", hover_color="#217e3f", height=40, state="disabled", command=self.save_to_file)
        self.btn_save.grid(row=6, column=0, padx=20, pady=(10, 30))

        # =================================================================
        # 2. PAINEL PRINCIPAL (CONSOLA DE SAÍDA E MÉTRICAS)
        # =================================================================
        self.main_frame = ctk.CTkFrame(self, fg_color="#161920", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Barra de Progresso Ultra Moderna (Indica atividade)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=4, fg_color="#202533", progress_color="#1a73e8")
        self.progress_bar.pack(fill="x", side="top")
        self.progress_bar.set(0)

        # Monitor de Métricas (Cards em Grid na parte superior)
        self.metrics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.metrics_frame.pack(fill="x", padx=25, pady=25)

        # Card: Abertas
        self.card_open = ctk.CTkFrame(self.metrics_frame, fg_color="#1e2924", height=80, width=170)
        self.card_open.pack_propagate(False)
        self.card_open.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.card_open, text="PORTAS ABERTAS", font=ctk.CTkFont(size=10, weight="bold"), text_color="#4ade80").pack(pady=(12, 0))
        self.lbl_abertas = ctk.CTkLabel(self.card_open, text="0", font=ctk.CTkFont(family="Courier", size=24, weight="bold"), text_color="#4ade80")
        self.lbl_abertas.pack()

        # Card: Fechadas
        self.card_closed = ctk.CTkFrame(self.metrics_frame, fg_color="#2d1f22", height=80, width=170)
        self.card_closed.pack_propagate(False)
        self.card_closed.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.card_closed, text="PORTAS FECHADAS", font=ctk.CTkFont(size=10, weight="bold"), text_color="#f87171").pack(pady=(12, 0))
        self.lbl_fechadas = ctk.CTkLabel(self.card_closed, text="0", font=ctk.CTkFont(family="Courier", size=24, weight="bold"), text_color="#f87171")
        self.lbl_fechadas.pack()

        # Card: Tempo
        self.card_time = ctk.CTkFrame(self.metrics_frame, fg_color="#1f2430", height=80, width=170)
        self.card_time.pack_propagate(False)
        self.card_time.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.card_time, text="TEMPO DE EXECUÇÃO", font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8").pack(pady=(12, 0))
        self.lbl_tempo = ctk.CTkLabel(self.card_time, text="0.00s", font=ctk.CTkFont(family="Courier", size=22, weight="bold"), text_color="#cbd5e1")
        self.lbl_tempo.pack()

        # Console Terminal Estilizado
        self.console_label = ctk.CTkLabel(self.main_frame, text="CONSOLE OUTPUT", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray")
        self.console_label.pack(anchor="w", padx=25, pady=(10, 5))

        self.txt_console = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Courier", size=12), fg_color="#0b0d13", text_color="#68d391", border_width=1, border_color="#1e222b")
        self.txt_console.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        self.txt_console.configure(state="disabled")

    def log(self, message, clean=False):
        self.txt_console.configure(state="normal")
        if clean:
            self.txt_console.delete("1.0", "end")
        self.txt_console.insert("end", message + "\n")
        self.txt_console.configure(state="disabled")
        self.txt_console.see("end")
        self.update_idletasks()

    def check_port(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0) # Otimizado para varreduras mais rápidas
            result = s.connect_ex((host, port))
            
            if result == 0:
                try:
                    servico = socket.getservbyport(port, "tcp").upper()
                except:
                    servico = "UNKNOWN"
                s.close()
                return True, servico
            s.close()
            return False, ""
        except:
            return False, ""

    def start_scan(self):
        host = self.ip_entry.get().strip()
        p_start = self.port_start.get().strip()
        p_end = self.port_end.get().strip()

        if not host or not p_start or not p_end:
            messagebox.showerror("Erro de Entrada", "Todos os parâmetros do Scanner precisam ser informados.")
            return

        try:
            start_p = int(p_start)
            end_p = int(p_end)
        except ValueError:
            messagebox.showerror("Erro de Tipo", "As portas precisam ser valores inteiros válidos.")
            return

        # Configurações iniciais e Reset de Dados
        self.resultados_salvar = []
        self.btn_save.configure(state="disabled")
        self.log(f"[//] ESTABELECENDO CONEXÃO COM O ALVO: {host}...", clean=True)
        self.log(f"[//] MAPEANDO RANGES DE PORTA: {start_p} -> {end_p}\n")
        
        open_ports = 0
        closed_ports = 0
        total_ports = (end_p - start_p) + 1
        
        start_time = time.time()

        for idx, port in enumerate(range(start_p, end_p + 1), start=1):
            # Atualiza barra de progresso dinamicamente
            self.progress_bar.set(idx / total_ports)
            
            is_open, service = self.check_port(host, port)
            if is_open:
                self.log(f" >> [PORTA ABERTA] -> ID: {port} | SERVICE: {service}")
                self.resultados_salvar.append(f"Porta {port};ABERTA;{service}")
                open_ports += 1
            else:
                self.resultados_salvar.append(f"Porta {port};FECHADA;-")
                closed_ports += 1
                
            # Atualiza os Cards Instantaneamente
            self.lbl_abertas.configure(text=str(open_ports))
            self.lbl_fechadas.configure(text=str(closed_ports))
            self.lbl_tempo.configure(text=f"{time.time() - start_time:.2f}s")

        end_time = time.time()
        
        self.log(f"\n[✔] AUDITORIA FINALIZADA COM SUCESSO EM {end_time - start_time:.2f} SEGUNDOS.")
        if open_ports > 0:
            self.btn_save.configure(state="normal")

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Relatório CSV", "*.csv")],
            title="Exportar Dados de Auditoria"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("Porta;Status;Servico\n")
                    for line in self.resultados_salvar:
                        f.write(line + "\n")
                messagebox.showinfo("Exportação Concluída", "Os dados foram consolidados no arquivo com sucesso!")
            except Exception as e:
                messagebox.showerror("Falha Crítica", f"Erro ao acessar diretório: {str(e)}")

if __name__ == "__main__":
    app = CyberScanPro()
    app.mainloop()
