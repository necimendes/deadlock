import threading
import time

# definir os recursos compartilhados (locks)
lock_A = threading.Lock()
lock_B = threading.Lock()

def thread_1_funcao():
    print("Thread 1: Tentando adquirir Lock A...")
    lock_A.acquire()  # t1 pega lock a
    print("Thread 1: Lock A adquirido! (Possuindo Lock A)")
    time.sleep(0.1) # pausa pra tread 2 comecar e pegar lock b

    print("Thread 1: Tentando adquirir Lock B...")
    # t1 trava, espera q t2 libere lock b
    lock_B.acquire() 
    print("Thread 1: Lock B adquirido! (Deadlock evitado, mas não neste caso)")
    
    # simulação da conclusão do trabalho (nunca alcançado no deadlock)
    lock_B.release()
    lock_A.release()
    print("Thread 1: Terminou.")

def thread_2_funcao():
    """tenta pegar lock b, depois lock a."""
    print("Thread 2: Tentando adquirir Lock B...")
    lock_B.acquire()  # t2 pega lock b
    print("Thread 2: Lock B adquirido! (Possuindo Lock B)")
    time.sleep(0.1) # pausa pra thread 1 pegar lock a

    print("Thread 2: Tentando adquirir Lock A...")
    # t2 trava, esperando q t1 libere lock a
    lock_A.acquire() 
    print("Thread 2: Lock A adquirido! (Deadlock evitado, mas não neste caso)")
    
    # simulação da conclusão do trabalho (nunca alcançado no deadlock)
    lock_A.release()
    lock_B.release()
    print("Thread 2: Terminou.")

# criar e iniciar as threads
thread_1 = threading.Thread(target=thread_1_funcao)
thread_2 = threading.Thread(target=thread_2_funcao)

print("--- Simulação de Deadlock Iniciada ---")
thread_1.start()
thread_2.start()

# esperar que as threads terminem (o que não acontecerá em caso de deadlock)
thread_1.join()
thread_2.join()
print("--- Simulação de Deadlock Encerrada ---")