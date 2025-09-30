# Simulação de Deadlock e Prevenção em Sistemas Concorrentes

## Objetivo do Trabalho

Este trabalho tem como foco o estudo e a demonstração prática do **Deadlock** (Bloqueio Mútuo) em ambientes de programação concorrente. O trabalho consiste em duas etapas principais:

1.  **Criação do Problema:** Implementar um cenário em onde a disputa por recursos compartilhados por múltiplas *threads* ou *processos* resulte em um Deadlock.
2.  **Aplicação da Solução:** Aplicar uma técnica de **prevenção** de Deadlock, como a **Ordenação de Recursos** ou o uso estruturado de **Semáforos** (*Locks*), para garantir a execução segura e eficiente do programa.

### Competência Adquirida

A principal competência desenvolvida é a capacidade de **identificar as condições de Deadlock** (Exclusão Mútua, Posse e Espera, Não Preempção e Espera Circular) e **aplicar técnicas de sincronização** adequadas para evitar o travamento em sistemas concorrentes.

---

## O Que é Deadlock?

Deadlock é uma condição em que dois ou mais processos (ou *threads*) ficam paralisados, esperando indefinidamente um pelo outro para liberar um recurso. Eles entram em um ciclo vicioso de espera, impedindo que qualquer um prossiga.

Nossa simulação utiliza um modelo simples de **dois recursos** e **duas *threads*** que tentam adquirir esses recursos em ordens conflitantes, forçando o sistema a travar.

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
| :--- | :--- |
| **Python** (módulo `threading`) | Implementação inicial para demonstração clara dos *locks* e *threads*. |
| **C** (biblioteca `pthread`) | (Opcional) Implementação para um estudo mais aprofundado em sistemas operacionais. |
| **Locks/Semáforos** | Ferramentas de sincronização utilizadas como os "recursos" compartilhados. |

---

## Integrantes do Projeto

Este trabalho foi desenvolvido por:

* **Heloisa Rolins**
* **José Lucas**
* **Neci Silva**
* **Vitória Leal**

---

### Próximos Passos (Para futura atualização)

* Detalhar a **Metodologia** de implementação e análise.
* Apresentar os **Resultados** (código, *output* do Deadlock e *output* da Prevenção).
* Incluir a **Discussão** e Conclusão do estudo.
