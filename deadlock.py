import tkinter as tk
from tkinter import messagebox
import threading
import time

# --- 1. CONFIGURAÇÃO BÁSICA DO TKINTER ---
# O objeto root (janela principal) DEVE ser criado antes das variáveis StringVar
root = tk.Tk()
root.title("Simulação de Deadlock (Tkinter)")

# --- 2. VARIÁVEIS GLOBAIS E RECURSOS (LOCKS) ---

# Recursos Compartilhados
lock_A = threading.Lock()
lock_B = threading.Lock()

# Status para a GUI (StringVar precisa do root criado)
status_t1 = tk.StringVar(value="PRONTA")
status_t2 = tk.StringVar(value="PRONTA")
status_lock_A = tk.StringVar(value="LIVRE")
status_lock_B = tk.StringVar(value="LIVRE")
current_mode = tk.StringVar(value="PROBLEMA (DEADLOCK)")

# --- 3. FUNÇÕES DE ATUALIZAÇÃO DA INTERFACE (GUI) ---

def safe_update(status_var, new_value, lock_owner=None, fg_color='red'):
    """Atualiza o status da GUI de forma segura na thread principal."""
    label = None
    if status_var == status_t1: label = t1_label
    elif status_var == status_t2: label = t2_label
    elif status_var == status_lock_A: label = lock_A_label
    elif status_var == status_lock_B: label = lock_B_label

    if label:
        if "OCUPADO" in new_value or "TRABALHANDO" in new_value:
             fg_color = 'blue'
        elif "LIVRE" in new_value or "PRONTA" in new_value or "SUCESSO" in new_value:
             fg_color = 'green'
        elif "ESPERANDO" in new_value or "DEADLOCK" in new_value:
             fg_color = 'red'

        label.config(fg=fg_color)

    if lock_owner:
        status_var.set(f"OCUPADO ({lock_owner})")
    else:
        status_var.set(new_value)
    
    # Garante que a janela Tkinter seja atualizada
    root.update_idletasks()

# --- 4. LÓGICA DAS THREADS: O PROBLEMA (DEADLOCK) ---

def thread_1_deadlock():
    """Tenta adquirir Lock A, depois Lock B (Ordem CONFLITANTE)."""
    safe_update(status_t1, "SOLICITANDO A...")
    lock_A.acquire()
    safe_update(status_t1, "POSSUI A, SOLICITANDO B...")
    safe_update(status_lock_A, "OCUPADO (T1)", "T1")
    time.sleep(0.1) 

    safe_update(status_t1, "ESPERANDO POR B...")
    # T1 TRAVA AQUI: Espera T2 liberar Lock B
    lock_B.acquire() 
    
    # Se conseguir sair (raro, mas possível), trata-se de sorte do scheduler
    safe_update(status_t1, "FALHA NA SIMULAÇÃO DE DEADLOCK (Continuou)", "T1")
    lock_B.release()
    lock_A.release()
    safe_update(status_t1, "TERMINOU")

def thread_2_deadlock():
    """Tenta adquirir Lock B, depois Lock A (Ordem CONFLITANTE)."""
    safe_update(status_t2, "SOLICITANDO B...")
    lock_B.acquire()
    safe_update(status_t2, "POSSUI B, SOLICITANDO A...")
    safe_update(status_lock_B, "OCUPADO (T2)", "T2")
    time.sleep(0.1)

    safe_update(status_t2, "ESPERANDO POR A...")
    # T2 TRAVA AQUI: Espera T1 liberar Lock A
    lock_A.acquire()
    
    # Se conseguir sair (raro, mas possível)
    safe_update(status_t2, "FALHA NA SIMULAÇÃO DE DEADLOCK (Continuou)", "T2")
    lock_A.release()
    lock_B.release()
    safe_update(status_t2, "TERMINOU")

# --- 5. LÓGICA DAS THREADS: A SOLUÇÃO (PREVENÇÃO) ---

def thread_1_solucao():
    """Tenta adquirir Lock A, depois Lock B (Ordem CORRETA)."""
    safe_update(status_t1, "SOLICITANDO A...")
    lock_A.acquire()
    safe_update(status_t1, "POSSUI A, SOLICITANDO B...")
    safe_update(status_lock_A, "OCUPADO (T1)", "T1")
    time.sleep(0.1)

    lock_B.acquire()
    safe_update(status_t1, "TRABALHANDO (POSSUI A e B)")
    safe_update(status_lock_B, "OCUPADO (T1)", "T1")
    time.sleep(1.0) # Simula trabalho

    lock_B.release()
    safe_update(status_lock_B, "LIVRE")
    lock_A.release()
    safe_update(status_lock_A, "LIVRE")
    safe_update(status_t1, "TERMINOU (SUCESSO)")

def thread_2_solucao():
    """Tenta adquirir Lock A, depois Lock B (Ordem CORRETA)."""
    safe_update(status_t2, "SOLICITANDO A...")
    lock_A.acquire()
    safe_update(status_t2, "POSSUI A, SOLICITANDO B...")
    safe_update(status_lock_A, "OCUPADO (T2)", "T2")
    time.sleep(0.1)

    lock_B.acquire()
    safe_update(status_t2, "TRABALHANDO (POSSUI A e B)")
    safe_update(status_lock_B, "OCUPADO (T2)", "T2")
    time.sleep(1.0) # Simula trabalho

    lock_B.release()
    safe_update(status_lock_B, "LIVRE")
    lock_A.release()
    safe_update(status_lock_A, "LIVRE")
    safe_update(status_t2, "TERMINOU (SUCESSO)")

# --- 6. CONTROLE DA SIMULAÇÃO ---

def reset_gui():
    """Reinicia os status para uma nova simulação."""
    status_t1.set("PRONTA")
    status_t2.set("PRONTA")
    status_lock_A.set("LIVRE")
    status_lock_B.set("LIVRE")

def start_simulation():
    """Função principal para iniciar as threads baseada no modo atual."""
    # Tenta liberar locks caso o modo Deadlock tenha sido interrompido
    try:
        if lock_A.locked(): lock_A.release()
        if lock_B.locked(): lock_B.release()
    except RuntimeError:
        # Se um lock for liberado por uma thread que não o possui (Tkinter main thread), ignora
        pass 
        
    reset_gui()
    
    mode = current_mode.get()
    
    if "PROBLEMA" in mode:
        threading.Thread(target=thread_1_deadlock).start()
        threading.Thread(target=thread_2_deadlock).start()
    else: # MODO SOLUÇÃO
        threading.Thread(target=thread_1_solucao).start()
        threading.Thread(target=thread_2_solucao).start()

def toggle_mode():
    """Alterna entre os modos Problema e Solução."""
    if "PROBLEMA" in current_mode.get():
        current_mode.set("SOLUÇÃO (PREVENÇÃO)")
        messagebox.showinfo("Modo Alternado", "Modo Solução ativado: O programa deverá executar até o fim.")
    else:
        current_mode.set("PROBLEMA (DEADLOCK)")
        messagebox.showinfo("Modo Alternado", "Modo Deadlock ativado: O programa deverá travar (Deadlock).")
    
    reset_gui()

# --- 7. LAYOUT DA INTERFACE GRÁFICA ---

# Estilos
PAD_Y = 10
FONT_HEADER = ('Arial', 14, 'bold')
FONT_STATUS = ('Courier', 12)

# Cabeçalho do Modo
mode_label = tk.Label(root, textvariable=current_mode, font=('Arial', 16, 'bold'), fg='blue')
mode_label.pack(pady=PAD_Y)

# FRAME PRINCIPAL
main_frame = tk.Frame(root, padx=20, pady=20, borderwidth=2, relief="groove")
main_frame.pack(pady=PAD_Y)

# --- STATUS DAS THREADS ---
tk.Label(main_frame, text="STATUS DAS THREADS", font=FONT_HEADER).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(main_frame, text="Thread 1:", font=FONT_STATUS).grid(row=1, column=0, sticky='w')
t1_label = tk.Label(main_frame, textvariable=status_t1, font=FONT_STATUS, fg='green')
t1_label.grid(row=1, column=1, sticky='w')

tk.Label(main_frame, text="Thread 2:", font=FONT_STATUS).grid(row=2, column=0, sticky='w')
t2_label = tk.Label(main_frame, textvariable=status_t2, font=FONT_STATUS, fg='green')
t2_label.grid(row=2, column=1, sticky='w')

# --- STATUS DOS RECURSOS (LOCKS) ---
tk.Label(main_frame, text="STATUS DOS RECURSOS", font=FONT_HEADER).grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(main_frame, text="Lock A (Recurso 1):", font=FONT_STATUS).grid(row=4, column=0, sticky='w')
lock_A_label = tk.Label(main_frame, textvariable=status_lock_A, font=FONT_STATUS, fg='green')
lock_A_label.grid(row=4, column=1, sticky='w')

tk.Label(main_frame, text="Lock B (Recurso 2):", font=FONT_STATUS).grid(row=5, column=0, sticky='w')
lock_B_label = tk.Label(main_frame, textvariable=status_lock_B, font=FONT_STATUS, fg='green')
lock_B_label.grid(row=5, column=1, sticky='w')

# --- BOTÕES DE CONTROLE ---
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="INICIAR SIMULAÇÃO", command=start_simulation, bg='#4CAF50', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Alternar Modo", command=toggle_mode, bg='#FF9800', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=10)

# Iniciar o loop principal da GUI
root.mainloop()