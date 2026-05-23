# ⚡ CyberScan - Matheus Rangel

Este projeto consiste em uma ferramenta de auditoria de segurança defensiva (Port Scanner) desenvolvida em Python 3 com uma interface gráfica (GUI) moderna e intuitiva utilizando a biblioteca `CustomTkinter`. O software foi projetado para mapear portas TCP ativas em ativos de rede, auxiliando na identificação de serviços expostos e conformidade de segurança.

---

## 📺 Vídeo Demonstrativo do Projeto

Abaixo está o vídeo com a apresentação completa do código-fonte, teste prático de varredura (portas abertas e fechadas) e exportação do relatório consolidado:

https://github.com/user-attachments/assets/f7528fc4-f368-4d47-82b6-12fb87f2a736

Aqui no código, usei a biblioteca socket com o método connect_ex(). Como pedido na Fase 1, tratei o timeout explicitamente em 2 segundos para o programa não travar. Na Fase 2, criei a estrutura de loops para varrer múltiplos ranges e o contador de tempo. E na Fase 3, adicionei a identificação automática dos serviços das portas e a exportação para CSV.

https://github.com/user-attachments/assets/9caa208a-3249-4822-9aa6-f69df23a068d

Iniciei o teste ligando os serviços de SSH e Apache na minha VM. Como pode ver, o scanner detectou na hora a porta 22 como SSH aberta e a porta 80 como HTTP aberta, atualizando os cards de métricas e a barra de progresso em tempo real.

https://github.com/user-attachments/assets/771401bb-d929-49e4-9c63-252f30bfd5ab

Com o fim do scan, o botão verde 'Exportar CSV' foi liberado. Ao clicar, ele gera o relatório estruturado com os resultados da auditoria de rede. Esse é o fim da demonstração, muito obrigado!







---

## 📄 Relato Técnico do Desenvolvimento

Durante o desenvolvimento do Port Scanner, a principal dificuldade encontrada foi integrar o loop de varredura de sockets com a biblioteca CustomTkinter sem travar a interface gráfica (GUI), o que foi solucionado através da atualização manual de tarefas pendentes (`update_idletasks`). 

Com o projeto, aprendi na prática conceitos fundamentais de redes de computadores, como o handshake TCP de três vias através do método `connect_ex()`, além de manipulação de ponteiros de arquivos e exportação de dados em formato estruturado CSV. 

Como limitação do scanner atual, destaca-se que a varredura é síncrona/sequencial, fazendo com que ranges muito extensos demorem mais tempo caso encontrem firewalls; uma melhoria futura ideal seria a aplicação total de concorrência com Threads (Multithreading) para otimização massiva de velocidade.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base)
* **Socket** (Comunicação de rede de baixo nível e timeout de 1.0s)
* **CustomTkinter** (Interface gráfica ultra moderna com Dark Mode nativo)
* **Time** (Métricas de performance temporal)
* **Tkinter Filedialog** (Persistência e exportação de relatórios .csv)

---
*Desenvolvido por Matheus Rangel para fins acadêmicos e auditoria de infraestrutura.*
