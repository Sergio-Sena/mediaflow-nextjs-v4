Uma empresa está criando um aplicativo de jogos que será implantado em dispositivos móveis. O aplicativo enviará dados para uma API RESTful baseada em funções Lambda. O aplicativo atribuirá a cada requisição da API um identificador único. O volume de requisições da API pode variar aleatoriamente a qualquer momento do dia. Durante o throttling das requisições, o aplicativo pode precisar reenviar requisições. A API deve ser capaz de lidar com requisições duplicadas sem inconsistências ou perda de dados.

Qual das seguintes abordagens você recomendaria para atender a esses requisitos?

Alternativas
Persistir o identificador único de cada requisição em um cache ElastiCache com Memcached. Modificar a função Lambda para verificar o cache em busca do identificador antes de processar a requisição.

Persistir o identificador único de cada requisição em uma tabela DynamoDB. Modificar a função Lambda para verificar a tabela em busca do identificador antes de processar a requisição.

Persistir o identificador único de cada requisição em uma tabela MySQL no RDS. Modificar a função Lambda para verificar a tabela em busca do identificador antes de processar a requisição.

Persistir o identificador único de cada requisição em uma tabela DynamoDB. Modificar a função Lambda para enviar uma resposta de erro ao cliente quando receber uma requisição duplicada.

Resposta Correta
A alternativa correta é a 2ª alternativa:

Persistir o identificador único de cada requisição em uma tabela DynamoDB. Modificar a função Lambda para verificar a tabela em busca do identificador antes de processar a requisição.

Explicação da Resposta Correta (Idempotência com DynamoDB)
Essa solução é a abordagem arquitetural recomendada pela AWS para implementar Idempotência em funções Lambda.

Idempotência: O requisito de lidar com "requisições duplicadas sem inconsistências" é resolvido pela idempotência, que garante que a operação seja executada apenas uma vez, mesmo que invocada várias vezes.

Amazon DynamoDB: É a melhor escolha para armazenar o identificador único (a chave de idempotência) porque é um banco de dados Serverless de altíssima performance. Ele oferece:

Escalabilidade Elástica: Lida com o volume de requisições que pode variar aleatoriamente sem a necessidade de provisionar ou gerenciar instâncias.

Latência Baixa: Crucial para verificar rapidamente se o identificador já existe antes de processar a lógica do jogo.

Operações Condicionais: A Lambda pode usar operações condicionais do DynamoDB (como PutItem com uma ConditionExpression) para tentar criar o registro da chave. Se a operação falhar porque o item já existe, a Lambda sabe que é uma requisição duplicada e evita o reprocessamento.

Por que as Outras Alternativas Estão Incorretas?
Alternativa 1 (ElastiCache): Caches (como Memcached) não são duráveis. Os dados podem ser perdidos (por expiração ou despejo), permitindo que requisições duplicadas sejam processadas, violando o requisito de consistência.

Alternativa 3 (MySQL/RDS): O RDS não é serverless e tem limitações de escalabilidade elástica para lidar com picos de tráfego imprevisíveis (o scalability on-demand do DynamoDB é muito superior). Além disso, as conexões Lambda-RDS são mais complexas de gerenciar.

Alternativa 4 (Erro no DynamoDB): Embora use o DynamoDB corretamente para armazenamento, retornar um erro para uma requisição duplicada é incorreto. Se o cliente está re-tentando (devido a throttling), ele espera uma resposta de sucesso (o resultado da operação original) para confirmar que a ação foi concluída. Retornar um erro incentivaria o cliente a tentar novamente, possivelmente em loop.