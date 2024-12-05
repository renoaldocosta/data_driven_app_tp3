# Assistente Virtual da Câmara Municipal de Pinhão/SE

## **Descrição do Projeto**

### **Problema**

A Câmara Municipal de Pinhão/SE enfrenta desafios na disseminação eficiente de informações financeiras e de transparência para os cidadãos. As consultas manuais a esses dados são demoradas e propensas a erros, dificultando o acesso rápido e preciso às informações públicas.

### **Solução**

Foi desenvolvido um assistente virtual baseado em chatbot que permite aos servidores consultar informações financeiras e de transparência de forma rápida e eficiente. Este assistente facilita o acesso a dados como elementos e subelementos de despesa, valores empenhados a pessoas físicas e jurídicas, CPF/CNPJ dos credores, e atualizações de atos legais e infralegais. Além disso, automatiza processos que anteriormente exigiam consultas manuais no site da Câmara, melhorando a experiência do usuário interno e aumentando a eficiência operacional.

## **Casos de Uso Testados e Resultados Observados**

### **1. Atualização de Projetos e Atos Legais**

**Descrição:** O assistente auxilia na recuperação de informações atualizadas sobre projetos e atos legais da Câmara Municipal.

**Processo Manual:**
1. Acessar o site da Câmara: [Leis e Atos Infralegais](https://camaradepinhao.se.gov.br/leis-e-atos-infralegais/).
2. Filtrar por cada tipo de matéria.
3. Anotar a última lei mencionada.
4. Repetir para cada tipo de matéria para compilar uma lista completa.

**Processo com o Assistente:**
- O usuário solicita "atualizações recentes dos atos legais" ou "projetos de atos legais atualizados recentemente".
- O assistente recupera e apresenta as informações de forma estruturada e consolidada.

**Resultado:** Redução significativa no tempo necessário para obter as informações, com menor possibilidade de erro humano na coleta de dados.

### **2. Consulta de Valores Empenhados por Subelemento**

**Descrição:** O assistente permite a consulta do total empenhado para subelementos específicos, como fretes, em períodos acumulados.

**Processo Manual:**
1. Acessar o sistema de geração de relatórios.
2. Preencher campos como tipo de relatório, grupo, subelemento e período (ano).
3. Gerar o relatório e anotar o valor.
4. Repetir para cada ano (2021, 2022, 2023) e somar os resultados.

**Processo com o Assistente:**
- O usuário solicita, por exemplo, "Qual o total empenhado para o subelemento fretes?".
- O assistente processa a solicitação, consulta o sistema e retorna o valor acumulado automaticamente.

**Resultado:** Simplificação do processo de consulta, eliminando a necessidade de múltiplas interações manuais e cálculos adicionais.

## **Instruções para Execução do Código**

### **Passo a Passo**

1. **Clone o Repositório Interno:**
   ```bash
   git clone https://git.camarapinhao.se.gov.br/seu-usuario/assistente-virtual-camara-pinhao.git
   cd assistente-virtual-camara-pinhao
   ```

2. **Crie e Ative um Ambiente Virtual (Opcional, mas Recomendado):**
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Unix ou MacOS
   source venv/bin/activate
   ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a Aplicação:**
   ```bash
   streamlit run ./app.py
   ```

5. **Acesse o Assistente Virtual:**
   - Abra o navegador e vá para [http://localhost:8501](http://localhost:8501) para interagir com o assistente.

## **Reflexão sobre a Eficiência do Assistente Virtual**

A implementação do assistente virtual proporcionou uma melhoria significativa na acessibilidade e eficiência na obtenção de informações financeiras e de transparência da Câmara Municipal de Pinhão/SE. Comparado ao método manual, o assistente:

- **Reduziu o Tempo de Resposta:** Consultas que antes levavam vários minutos podem ser realizadas em segundos.
- **Minimizou Erros Humanos:** A automação das consultas elimina a possibilidade de erros na coleta e compilação de dados.
- **Melhorou a Experiência do Usuário Interno:** Interações simplificadas e respostas claras aumentam a produtividade dos servidores.
- **Aumentou a Transparência Interna:** Facilita o acesso a informações públicas, promovendo uma gestão mais transparente e responsável dentro da administração.

Em suma, o assistente virtual não apenas agiliza processos internos, mas também fortalece a eficiência operacional da Câmara Municipal, promovendo maior engajamento e confiança na gestão pública.

## **Contato e Suporte**

Caso encontre dificuldades ou tenha dúvidas adicionais, entre em contato com a equipe de TI da Câmara Municipal de Pinhão/SE através do canal interno de suporte ou pelo e-mail suporte@camarapinhao.se.gov.br.

---

**Desenvolvido por:** Renoaldo Costa Silva Junior

**Licença:** Interna - Uso Restrito à Câmara Municipal de Pinhão/SE

---

## **Notas Adicionais**

- **Repositório Privado:** Este projeto será hospedado em um repositório privado para garantir a segurança e confidencialidade das informações. Acesso restrito aos membros autorizados da equipe.
- **Atualizações:** Para atualizações do projeto, seguir o fluxo de trabalho definido pela equipe de desenvolvimento interna.
- **Contribuições:** Qualquer contribuição deve ser revisada e aprovada pela liderança do projeto antes de ser integrada ao repositório principal.
