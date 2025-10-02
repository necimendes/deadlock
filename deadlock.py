import threading
import time

# definir recursos compartilhados (locks/semáforos)
lock_A = threading.Lock()
lock_B = threading.Lock()

# ordem de aquisição de recursos definida: sempre lock a, depois lock b.

def thread_1_funcao():
    """mantém a ordem: lock a, depois lock b."""
    print("Thread 1: Tentando adquirir Lock A...")
    lock_A.acquire()  # t1 pega lock a
    print("Thread 1: Lock A adquirido!")
    time.sleep(0.1) # pausa para simular processamento/disputa

    print("Thread 1: Tentando adquirir Lock B...")
    # se t2 já tiver lock b, t1 espera. mas t2 também tentará a primeiro.
    lock_B.acquire() 
    print("Thread 1: Lock B adquirido!")
    
    print("Thread 1: Recursos adquiridos. Trabalhando...")
    time.sleep(0.5)
    
    lock_B.release()
    lock_A.release()
    print("Thread 1: Terminou e liberou os recursos.")

def thread_2_funcao_corrigida():
    """tenta adquirir lock a, depois lock b. (quebrando espera circular)"""
    print("Thread 2: Tentando adquirir Lock A...")
    lock_A.acquire()  # t2 pega lock a (ou espera t1 liberá-lo)
    print("Thread 2: Lock A adquirido!")
    time.sleep(0.1) # pausa para simular processamento/disputa

    print("Thread 2: Tentando adquirir Lock B...")
    # t2 tenta pegar lock b (ou espera t1 liberá-lo)
    lock_B.acquire() 
    print("Thread 2: Lock B adquirido!")
    
    print("Thread 2: Recursos adquiridos. Trabalhando...")
    time.sleep(0.5)
    
    lock_B.release()
    lock_A.release()
    print("Thread 2: Terminou e liberou os recursos.")

# criar e iniciar as threads (usando a função corrigida para t2)
thread_1 = threading.Thread(target=thread_1_funcao)
thread_2 = threading.Thread(target=thread_2_funcao_corrigida)

print("--- Simulação de Prevenção de Deadlock Iniciada ---")
thread_1.start()
thread_2.start()

# esperar que as threads terminem
thread_1.join()
thread_2.join()
print("--- Simulação de Deadlock Encerrada e bem sucedida ---")