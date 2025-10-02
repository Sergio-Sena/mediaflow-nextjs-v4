Guia Completo de Engenharia de Prompt para Devs e Automação

1. Fundamentos: A Estrutura de um Prompt Poderoso:

Um prompt eficaz para desenvolvimento e automação deve ser estruturado de forma a orientar o Modelo de Linguagem Grande (LLM) de maneira precisa.
A estrutura ideal possui quatro componentes essenciais:

A. Papel (Role Prompting)
Define a persona do modelo para orientar o tom e o nível técnico.
• Exemplo: Aja como um Desenvolvedor Full-Stack sênior com foco em código limpo.
• Melhoria: Garante que a saída (código, script, documentação) seja profissional e utilize as melhores práticas do setor.

B. Tarefa (Task)
Define o que deve ser feito de forma única, clara e objetiva.
• Exemplo: Crie um script Python que automatize a leitura de um arquivo CSV.
• Melhoria: Evita respostas vagas e direciona o esforço do modelo para um resultado específico.

C. Contexto (Context)
Fornece o pano de fundo, dados de entrada e requisitos técnicos necessários para a execução.
• Exemplo: O projeto utiliza React 18 e o endpoint de autenticação é /api/auth. O CSV de entrada possui as colunas 'ID', 'Data' e 'Status'.
• Melhoria: Aumenta drasticamente a relevância e a precisão técnica da saída.

D. Restrições e Formato (Constraints & Format)
Estabelece regras de qualidade e o formato da entrega. Crucial para que o resultado possa ser usado diretamente em seu fluxo de trabalho.
• Exemplo: O código deve vir em um único bloco de código Markdown. Não inclua explicações. Adicione comentários em Português.
• Melhoria: Garante que o output seja consumível por outras ferramentas ou que siga seu padrão de codificação.

---

2. Técnicas Avançadas para Qualidade e Robustez

Para elevar a qualidade do código ou da lógica de automação, integre estas técnicas na sua seção de Tarefa Detalhada ou Restrições:
Técnica Descrição Aplicação em Desenvolvimento/Automação
Chain-of-Thought (CoT) Instruir o modelo a raciocinar passo a passo antes de entregar a solução.

Peça ao modelo para "pensar" na lógica do algoritmo ou na estrutura do componente antes de gerar o código.

Few-Shot Prompting Fornecer exemplos de entrada e a saída esperada para estabelecer um padrão. Mostrar um trecho de código "ruim" e a refatoração "boa" para garantir que o modelo siga seu estilo.
Delimitadores Usar caracteres (""", ---, <tags>) para separar dados de entrada das instruções. Isolar grandes blocos de código ou JSON complexo a ser analisado, reduzindo a confusão do modelo.
Self-Correction Pedir ao modelo para revisar e criticar a própria resposta após gerá-la. Instruir: "Após gerar a função, revise-a em busca de vulnerabilidades de segurança ou otimizações de performance".
Exportar para as Planilhas

---

3. Guia Mestre de Engenharia de Prompt (Template C.E.R.T.O)
   Use este modelo como o esqueleto para qualquer prompt que envolva tarefas técnicas. Preencha os campos [COLCHETES] para adaptá-lo:
   Markdown

# 1. PAPEL E OBJETIVO (O P de C.E.R.T.O)

Você é um(a) [DEFINA A PERSONA: Ex: Desenvolvedor Full-Stack Sênior, Especialista em Automação Python, Engenheiro de DevOps].

Seu objetivo principal é [DESCREVA O RESULTADO FINAL: Ex: Gerar o código HTML/CSS/JS completo de uma página; Criar um script Python funcional que integra duas APIs; Documentar uma função complexa].

# 2. CONTEXTO E INFORMAÇÃO (O C de C.E.R.T.O)

## 2.1. Conhecimento Base (Informação de Entrada)

[INSIRA O CONTEÚDO QUE O MODELO PRECISA ANALISAR: Código existente, JSON de entrada da API, requisitos do usuário, etc.]

## 2.2. Ambiente e Escopo

[ESPECIFIQUE O AMBIENTE/TECNOLOGIAS: Ex: Linguagem: TypeScript; Framework: Next.js 14; Estilização: CSS Modules. OU Ambiente: Automação de E-mails com Zapier/Integromat; Bibliotecas Python: `requests` e `json`.]

# 3. TAREFA DETALHADA E EXPECTATIVA (O T de C.E.R.T.O)

Siga estas etapas de raciocínio para executar a tarefa:

## 3.1. Raciocínio (Chain-of-Thought - CoT)

**Pense passo a passo** antes de gerar a resposta final.

1. Analise o [2.1. Conhecimento Base].
2. [DESCREVA O PRIMEIRO PASSO LÓGICO: Ex: Definir a estrutura do componente React ou Mapear os campos do JSON de entrada].
3. [DESCREVA O SEGUNDO PASSO: Ex: Implementar a lógica de validação do formulário ou Escrever a função de tratamento de erros].
4. [DESCREVA O TERCEIRO PASSO/CHECK FINAL: Ex: Garantir que o código seja modular e que todas as Regras (4.) foram seguidas].

## 3.2. Ação Principal

[REITERAR A TAREFA FINAL QUE DEVE SER ENTREGUE: Ex: Gere o código completo do componente `ContactForm.js`.]

# 4. REGRAS E RESTRIÇÕES DE SAÍDA (O R de C.E.R.T.O)

O resultado DEVE aderir estritamente às seguintes regras:

1. **Estilo:** [Ex: Use arrow functions (=>) e sintaxe ES6. OU Use *snake_case* para variáveis em Python.]
2. **Formato:** [Ex: O código deve vir em **um único bloco de código Markdown** com a linguagem especificada. OU A resposta deve ser uma tabela HTML sem tags `<style>`.]
3. **Restrição Técnica:** [Ex: **Não use** bibliotecas externas além de React e Tailwind. OU **Não inclua** comentários, a menos que sejam JSDoc.]
4. **Idioma:** [Ex: A saída (código e explicações) deve estar em **Português do Brasil**.]

# 5. ENTREGA (O E de C.E.R.T.O)

Após a etapa de **Raciocínio**, forneça APENAS o resultado final da Ação Principal, seguindo todas as Regras.
