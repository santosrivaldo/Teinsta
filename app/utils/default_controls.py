"""
Controles padrão da ISO 27001
"""

def get_default_controls():
    """Retorna lista de controles padrão da ISO 27001"""
    return [
        # A.5 - Política de Segurança
        ('A.5.1.1', 'Políticas para segurança da informação', 'Políticas devem ser definidas, documentadas e revisadas em intervalos planejados ou quando houver mudanças significativas', 'A.5 - Política de Segurança'),
        ('A.5.1.2', 'Revisão das políticas para segurança da informação', 'As políticas devem ser aprovadas pela direção e publicadas e comunicadas a todos os funcionários e partes interessadas relevantes', 'A.5 - Política de Segurança'),
        
        # A.6 - Organização da Segurança da Informação
        ('A.6.1.1', 'Funções e responsabilidades de segurança', 'Todas as responsabilidades de segurança devem ser definidas e alocadas', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.2', 'Separação de funções', 'Deveres e áreas de responsabilidade conflitantes devem ser segregados para reduzir oportunidades de modificação não autorizada ou uso indevido de ativos da organização', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.3', 'Contato com autoridades', 'Deve ser mantido contato apropriado com autoridades relevantes', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.4', 'Contato com grupos especiais', 'Deve ser mantido contato apropriado com grupos ou associações especializadas em segurança', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.5', 'Segurança da informação em gestão de projetos', 'A segurança da informação deve ser tratada em gestão de projetos, independentemente do tipo de projeto', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.2.1', 'Políticas de trabalho móvel e teletrabalho', 'As políticas de segurança e medidas de apoio devem ser implementadas para proteger informações acessadas, processadas ou armazenadas em locais de trabalho móvel', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.2.2', 'Dispositivos móveis', 'Deve ser estabelecida uma política e medidas de apoio para gerenciamento do uso de dispositivos móveis', 'A.6 - Organização da Segurança da Informação'),
        
        # A.7 - Segurança em Recursos Humanos
        ('A.7.1.1', 'Screenings', 'Screenings devem ser realizados para todos os candidatos a emprego, contratados e terceiros', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.1.2', 'Termos e condições de emprego', 'Termos e condições de emprego devem estabelecer as responsabilidades do funcionário pela segurança da informação', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.2.1', 'Conscientização e treinamento em segurança', 'O pessoal da organização e pessoas relevantes terceirizadas devem receber conscientização e treinamento em segurança apropriados e atualizados regularmente', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.2.2', 'Processo disciplinar', 'Deve haver um processo disciplinar formal e comunicado que tome ação contra funcionários que tenham comprometido a segurança da informação', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.3.1', 'Processo de término ou mudança de responsabilidades', 'Responsabilidades e deveres de emprego que permanecem válidos após término ou mudança de emprego devem ser definidos, comunicados ao funcionário ou terceirizado e aplicados', 'A.7 - Segurança em Recursos Humanos'),
        
        # A.8 - Gestão de Ativos
        ('A.8.1.1', 'Inventário de ativos', 'Todos os ativos devem ser identificados e inventariados', 'A.8 - Gestão de Ativos'),
        ('A.8.1.2', 'Proprietário dos ativos', 'Ativos mantidos no inventário devem ter proprietário designado', 'A.8 - Gestão de Ativos'),
        ('A.8.1.3', 'Uso aceitável de ativos', 'Regras para uso aceitável de informações e ativos associados com recursos de processamento de informação devem ser identificadas, documentadas e implementadas', 'A.8 - Gestão de Ativos'),
        ('A.8.1.4', 'Retorno de ativos', 'Todos os ativos devem ser retornados quando o emprego, contratos ou acordos são encerrados', 'A.8 - Gestão de Ativos'),
        ('A.8.2.1', 'Classificação da informação', 'Informação deve ser classificada de acordo com requisitos legais, valor, criticidade e sensibilidade para divulgação não autorizada', 'A.8 - Gestão de Ativos'),
        ('A.8.2.2', 'Rótulos de informação', 'Um conjunto apropriado de procedimentos para rotulagem de informação deve ser desenvolvido e implementado de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.2.3', 'Tratamento de ativos', 'Procedimentos para tratamento de ativos devem ser desenvolvidos e implementados de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.3.1', 'Gestão de mídia removível', 'Procedimentos devem ser implementados para o uso de mídia removível de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.3.2', 'Descarte de mídia', 'Mídia deve ser descartada de forma segura quando não for mais necessária, usando procedimentos formais', 'A.8 - Gestão de Ativos'),
        ('A.8.3.3', 'Mídia física em trânsito', 'Mídia física contendo informação deve ser protegida contra acesso não autorizado, uso indevido ou corrupção durante o transporte além dos limites físicos', 'A.8 - Gestão de Ativos'),
        
        # A.9 - Controle de Acesso
        ('A.9.1.1', 'Política de controle de acesso', 'Política de controle de acesso deve ser estabelecida, documentada e revisada com base em requisitos de negócio e segurança', 'A.9 - Controle de Acesso'),
        ('A.9.1.2', 'Acesso a redes e serviços de rede', 'Usuários devem ser fornecidos apenas com acesso a rede e serviços de rede que tenham sido explicitamente autorizados', 'A.9 - Controle de Acesso'),
        ('A.9.2.1', 'Registro e cancelamento de usuário', 'Formal processo de registro e cancelamento deve ser implementado para permitir e revogar acesso a sistemas de informação e serviços', 'A.9 - Controle de Acesso'),
        ('A.9.2.2', 'Provisionamento de acesso de usuário', 'Deve ser estabelecido um processo formal de provisionamento de acesso de usuário para atribuir ou revogar direitos de acesso para todos os tipos de usuários para todos os sistemas e serviços', 'A.9 - Controle de Acesso'),
        ('A.9.2.3', 'Gestão de direitos de acesso privilegiado', 'O uso e alocação de direitos de acesso privilegiado deve ser restrito e controlado', 'A.9 - Controle de Acesso'),
        ('A.9.2.4', 'Gestão de informações de autenticação secretas', 'Procedimentos de gestão de informações de autenticação secretas devem ser implementados através de todo o ciclo de vida', 'A.9 - Controle de Acesso'),
        ('A.9.2.5', 'Revisão dos direitos de acesso de usuário', 'Proprietários de ativos devem revisar os direitos de acesso de usuários regularmente', 'A.9 - Controle de Acesso'),
        ('A.9.2.6', 'Remoção ou ajuste dos direitos de acesso', 'Rights of access de todos os funcionários e terceirizados externos para informações e instalações de processamento devem ser removidos após término de emprego ou ajustados após mudança', 'A.9 - Controle de Acesso'),
        ('A.9.3.1', 'Uso de segredos para autenticação', 'Sistemas devem usar métodos seguros de autenticação de usuários, adequados para o método de acesso usado', 'A.9 - Controle de Acesso'),
        ('A.9.4.1', 'Política de informação e restrição de acesso', 'Acesso a informação e funções de aplicação deve ser restrito de acordo com a política de controle de acesso', 'A.9 - Controle de Acesso'),
        ('A.9.4.2', 'Procedimento de logon seguro', 'Onde exigido por política de controle de acesso, procedimento de logon seguro deve ser estabelecido e operado para sistemas de informação e aplicações', 'A.9 - Controle de Acesso'),
        ('A.9.4.3', 'Sistema de gestão de senhas', 'Sistema de gestão de senhas deve ser interativo e deve garantir qualidade de senha', 'A.9 - Controle de Acesso'),
        ('A.9.4.4', 'Uso de utilitários de privilégios do sistema', 'O uso de utilitários que podem ser capazes de sobrescrever sistema e controles de aplicação deve ser restrito e rigorosamente controlado', 'A.9 - Controle de Acesso'),
        ('A.9.4.5', 'Segregação em aplicações', 'Aplicações devem ser segregadas para limitar o risco', 'A.9 - Controle de Acesso'),
        ('A.9.4.6', 'Informações limitadas sobre políticas e procedimentos de acesso', 'Informações sobre políticas e procedimentos de controle de acesso deve estar disponível apenas para usuários que tenham direito a ela', 'A.9 - Controle de Acesso'),
        
        # A.10 - Criptografia
        ('A.10.1.1', 'Política de uso de controles criptográficos', 'Políticas sobre uso de controles criptográficos devem ser desenvolvidas e implementadas', 'A.10 - Criptografia'),
        ('A.10.1.2', 'Gestão de chaves', 'Gestão de chaves deve ser implementada através de todo o ciclo de vida da criptografia', 'A.10 - Criptografia'),
        
        # A.11 - Segurança Física e do Ambiente
        ('A.11.1.1', 'Perímetros físicos e controles de segurança', 'Perímetros físicos devem ser definidos e usados para proteger áreas que contêm informações e sistemas de processamento de informação', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.2', 'Controles físicos de entrada', 'Áreas seguras devem ser protegidas por controles apropriados de entrada para assegurar que apenas pessoas autorizadas têm acesso', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.3', 'Salas seguras e câmaras fortificadas', 'Salas seguras e câmaras fortificadas devem ser projetadas e implementadas', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.4', 'Perímetros físicos monitorados e de segurança', 'Perímetros físicos devem ser monitorados e revisados', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.5', 'Proteção contra ameaças físicas e ambientais', 'Proteção física contra desastres naturais, acidentes, ataques maliciosos e deliberados deve ser projetada e aplicada', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.6', 'Áreas de trabalho seguras', 'Áreas de trabalho seguras devem ser projetadas e protegidas', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.1', 'Equipamento de localização e proteção', 'Equipamento deve ser posicionado e protegido para reduzir riscos de ameaças ambientais e perigos e oportunidades de acesso não autorizado', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.2', 'Serviços de suporte', 'Equipamento deve ser protegido de falhas de energia e outros interrupções causadas por falhas nos serviços de suporte', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.3', 'Segurança de cablagem', 'Cablagem de energia e telecomunicações carregando dados ou suportando serviços de informação deve ser protegida contra interceptação ou dano', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.4', 'Manutenção de equipamento', 'Equipamento deve ser mantido corretamente para assegurar sua disponibilidade e integridade continuada', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.5', 'Remoção de ativos', 'Equipamento, informação ou software não devem ser retirados de instalações sem autorização', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.6', 'Segurança de equipamento e ativos fora das instalações', 'Segurança deve ser aplicada a ativos fora das instalações da organização, levando em conta diferentes riscos de trabalhar fora das instalações', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.7', 'Reutilização ou descarte seguro de equipamento', 'Todos os itens de equipamento contendo mídia de armazenamento devem ser verificados para garantir que qualquer informação sensível e licenciado software tenha sido removido ou sobrescrito de forma segura antes do descarte', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.8', 'Equipamento não utilizado', 'Equipamento não utilizado deve ser removido ou o uso de recursos de mídia removível e interface de rede deve ser desabilitado ou removido fisicamente', 'A.11 - Segurança Física e do Ambiente'),
        
        # A.12 - Segurança nas Operações
        ('A.12.1.1', 'Documentação de procedimentos operacionais', 'Procedimentos operacionais devem ser documentados e disponibilizados para todos os usuários que precisem deles', 'A.12 - Segurança nas Operações'),
        ('A.12.1.2', 'Gestão de mudanças', 'Mudanças em organização, processos de negócio, sistemas de informação e instalações devem ser controladas', 'A.12 - Segurança nas Operações'),
        ('A.12.1.3', 'Gestão de capacidade', 'Uso de recursos deve ser monitorado, ajustado e projeções futuras de requisitos de capacidade devem ser feitas para assegurar capacidade de sistema requerida', 'A.12 - Segurança nas Operações'),
        ('A.12.1.4', 'Separação de ambientes de desenvolvimento, teste e produção', 'Ambientes de desenvolvimento, teste e produção devem ser separados para reduzir riscos de acesso não autorizado ou mudanças aos sistemas de informação operacionais', 'A.12 - Segurança nas Operações'),
        ('A.12.2.1', 'Controles contra malware', 'Controles de detecção, prevenção e recuperação devem ser implementados, combinados com conscientização apropriada do usuário', 'A.12 - Segurança nas Operações'),
        ('A.12.3.1', 'Backup de informação', 'Backups de informações, software e imagens de sistema devem ser tomadas regularmente e testadas de acordo com o acordo de nível de serviço acordado', 'A.12 - Segurança nas Operações'),
        ('A.12.4.1', 'Registros de eventos', 'Logs de eventos que registram exceções, falhas e outros eventos relevantes devem ser produzidos, mantidos e revisados regularmente', 'A.12 - Segurança nas Operações'),
        ('A.12.4.2', 'Proteção de informação de log', 'Logging facilities and log information must be protected against tampering and unauthorized access', 'A.12 - Segurança nas Operações'),
        ('A.12.4.3', 'Logs de administrador e operador', 'Atividades de administradores de sistema e operadores devem ser registradas e logs protegidos e revisados regularmente', 'A.12 - Segurança nas Operações'),
        ('A.12.4.4', 'Sincronização de relógio', 'Relógios de todos os sistemas de informação relevantes devem ser sincronizados com uma fonte de tempo preciso e acordado', 'A.12 - Segurança nas Operações'),
        ('A.12.5.1', 'Instalação de software em sistemas operacionais', 'Procedimentos devem ser estabelecidos para controlar instalação de software em sistemas operacionais', 'A.12 - Segurança nas Operações'),
        ('A.12.6.1', 'Gestão de vulnerabilidades técnicas', 'Informação sobre vulnerabilidades técnicas de sistemas de informação em uso deve ser obtida, avaliada em termos de negócio e medidas apropriadas tomadas para tratar os riscos associados', 'A.12 - Segurança nas Operações'),
        ('A.12.6.2', 'Restrições em instalação de software', 'Regras que governam instalação de software por usuários devem ser estabelecidas e implementadas', 'A.12 - Segurança nas Operações'),
        ('A.12.7.1', 'Políticas e procedimentos de segurança de informação em uso de sistemas de informação', 'Regras, medidas e controles de segurança de informação devem ser estabelecidos e implementados quando sistemas de informação são utilizados', 'A.12 - Segurança nas Operações'),
        
        # A.13 - Segurança nas Comunicações
        ('A.13.1.1', 'Controles de rede', 'Redes devem ser gerenciadas e controladas para proteger informações em sistemas e aplicações', 'A.13 - Segurança nas Comunicações'),
        ('A.13.1.2', 'Política de transferência de informação', 'Políticas e procedimentos de transferência de informação devem ser estabelecidos para proteger transferência de informação através de todos os tipos de facilidades de comunicação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.1.3', 'Mensagens eletrônicas', 'Informações contidas em mensagens eletrônicas devem ser adequadamente protegidas', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.1', 'Política de desenvolvimento de informação', 'Políticas e procedimentos devem ser estabelecidos para proteger informações aplicadas a desenvolvimento de sistemas de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.2', 'Acordos de não divulgação', 'Acordos de não divulgação devem ser identificados, revisados regularmente e documentados para refletir necessidades atuais da organização para proteção de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.3', 'Armazenamento de informação', 'Regras para armazenamento de informação, incluindo período de retenção e descarte, devem ser estabelecidas para aplicar proteção adequada de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.4', 'Política de desenvolvimento de informação', 'Políticas e procedimentos devem ser estabelecidos para proteger informações aplicadas a desenvolvimento de sistemas de informação', 'A.13 - Segurança nas Comunicações'),
        
        # A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas
        ('A.14.1.1', 'Análise e especificação de requisitos de segurança', 'Requisitos de segurança de informação devem ser incluídos em requisitos para novos sistemas de informação ou melhorias em sistemas existentes', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.1.2', 'Segurança em aplicações em uso público', 'Informações envolvidas em aplicações públicas devem ser protegidas contra atividades fraudulentas, disputas contratuais e divulgação não autorizada e modificação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.1.3', 'Proteção de serviços de transações online', 'Informações envolvidas em serviços de transações online devem ser protegidas para prevenir atividade incompleta, transmissão incorreta, roteamento incorreto, alteração não autorizada de mensagens, divulgação, duplicação ou replay de mensagens', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.1', 'Política de desenvolvimento seguro', 'Regras para desenvolvimento de software e sistemas devem ser estabelecidas e aplicadas em desenvolvimentos dentro da organização', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.2', 'Gestão de mudanças em sistemas de segurança', 'Mudanças em sistemas durante todo o ciclo de vida de desenvolvimento devem ser controladas pelo uso de gestão formal de controle de mudanças, incluindo mudanças em sistemas de informação, políticas de negócio, processos e procedimentos de segurança e controle', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.3', 'Revisão técnica de aplicações após mudanças em plataformas operacionais', 'Quando plataformas operacionais mudam, aplicações de negócio críticas devem ser revisadas e testadas para assegurar que não haja impacto adverso na segurança de informação organizacional ou operações', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.4', 'Restrições em mudanças em pacotes de software', 'Modificações a pacotes de software devem ser desencorajadas, limitadas a mudanças necessárias e todas as mudanças devem ser estritamente controladas', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.5', 'Princípios de engenharia de sistemas seguros', 'Princípios de engenharia devem ser estabelecidos, documentados, mantidos e aplicados a qualquer iniciativa de engenharia de sistemas de informação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.6', 'Ambiente de desenvolvimento seguro', 'Organizações devem estabelecer e documentar adequadamente ambientes de desenvolvimento seguro para desenvolvimento e integração de componentes de sistema de informação em toda o ciclo de vida', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.7', 'Subcontratação de desenvolvimento', 'Organizações devem supervisionar e monitorar atividade de subcontratação de desenvolvimento de sistema', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.8', 'Teste de segurança em desenvolvimento', 'Testes de segurança devem ser conduzidos durante desenvolvimento', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.9', 'Teste de aceitação de sistema', 'Critérios de teste e planos de aceitação para novos sistemas de informação, atualizações e novas versões devem ser estabelecidos para sistemas de informação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.3.1', 'Proteção de dados de teste', 'Dados de teste devem ser selecionados, protegidos e controlados cuidadosamente', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        
        # A.15 - Relacionamento na Cadeia de Suprimento
        ('A.15.1.1', 'Política de segurança da informação na cadeia de suprimento', 'Políticas de segurança da informação devem ser estabelecidas e aplicadas na cadeia de suprimento de acordo com o tipo de acordos de negócio', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.1.2', 'Controles de segurança em acordos de cadeia de suprimento', 'Acordos com fornecedores devem incluir requisitos para abordar os riscos de segurança da informação e dos serviços de segurança associados', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.1.3', 'Processo de gestão de cadeia de suprimento de tecnologia de informação e comunicação', 'Processos e procedimentos devem ser estabelecidos e aplicados para gerenciar segurança da informação e riscos de serviços de segurança associados com uso de serviços de tecnologia de informação e comunicação que são acessados, processados, gerenciados ou comunicados por fornecedores externos', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.2.1', 'Monitoramento e revisão de serviços de fornecedores', 'Organizações devem monitorar, revisar e auditar regularmente prestação de serviços de fornecedores', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.2.2', 'Gestão de mudanças em fornecimento de serviços', 'Mudanças nos fornecimentos de serviços, incluindo manutenção e melhorias de sistemas, processos e procedimentos existentes, devem ser gerenciadas, levando em conta a criticidade dos processos de negócio, sistemas de informação e segurança envolvidos e re-reavaliação de riscos', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        
        # A.16 - Gestão de Incidente de Segurança da Informação
        ('A.16.1.1', 'Responsabilidades e procedimentos', 'Funcionalidades de gestão e responsabilidades de gestão de incidentes de segurança da informação devem ser estabelecidas e aplicadas de acordo com políticas de segurança da informação da organização', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.2', 'Reportar eventos de segurança da informação', 'Eventos de segurança da informação devem ser reportados através de canais de comunicação apropriados da gestão o mais rapidamente possível', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.3', 'Reportar fraquezas de segurança da informação', 'Fraquezas de segurança da informação devem ser reportadas e corrigidas', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.4', 'Análise e decisão sobre eventos de segurança da informação', 'Eventos de segurança da informação devem ser avaliados e decididos se devem ser classificados como incidentes de segurança da informação', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.5', 'Resposta a incidentes de segurança da informação', 'Respostas a incidentes de segurança da informação devem ser coordenadas de acordo com procedimentos documentados', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.6', 'Aprendizado com incidentes de segurança da informação', 'Conhecimento obtido de análise e resolução de incidentes de segurança da informação deve ser usado para reduzir a probabilidade ou impacto de futuros incidentes', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.7', 'Coleção de evidências', 'Organizações devem definir e aplicar procedimentos para identificação, coleta, aquisição e preservação de informações que podem servir como evidências', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        
        # A.17 - Aspectos da Segurança da Informação na Gestão de Continuidade de Negócio
        ('A.17.1.1', 'Planejamento de continuidade de segurança da informação', 'A organização deve determinar seus requisitos de continuidade de segurança da informação considerando requisitos de continuidade de negócio', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.1.2', 'Implementação de continuidade de segurança da informação', 'A organização deve estabelecer, documentar, implementar e manter processos, procedimentos e controles para garantir o nível requerido de continuidade de segurança da informação durante uma situação adversa', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.1.3', 'Verificar, revisar e avaliar continuidade de segurança da informação', 'A organização deve verificar regularmente os controles de continuidade de segurança da informação estabelecidos e implementados para garantir que são válidos e eficazes durante uma situação adversa', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.2.1', 'Disponibilidade de instalações de processamento de informação', 'Instalações de processamento de informação devem ser implementadas com redundância suficiente para atender requisitos de disponibilidade', 'A.17 - Gestão de Continuidade de Negócio'),
        
        # A.18 - Conformidade / Compliance
        ('A.18.1.1', 'Identificação de legislação e requisitos contratuais aplicáveis', 'Todas as legislações estatutárias, regulamentares e requisitos contratuais relevantes e abordagem da organização para atender a esses requisitos devem ser explicitamente identificados, documentados e mantidos atualizados para cada sistema de informação e organização', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.2', 'Propriedade intelectual', 'Propriedade intelectual adequada deve ser implementada', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.3', 'Proteção de registros organizacionais', 'Registros devem ser protegidos contra perda, destruição, falsificação, acesso não autorizado e liberação não autorizada, em conformidade com requisitos legislativos, regulamentares, contratuais e de negócios', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.4', 'Privacidade e proteção de informações pessoais identificáveis', 'Privacidade e proteção de informações pessoais identificáveis devem ser asseguradas conforme exigido em legislação e regulamentação relevantes quando aplicável', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.5', 'Regulamentação sobre controles criptográficos', 'Controles criptográficos devem ser usados em conformidade com todas as leis, regulamentos e acordos relevantes', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.1', 'Revisão independente de segurança da informação', 'A abordagem da organização para gerenciar segurança da informação e sua implementação devem ser revisadas independentemente em intervalos planejados ou quando mudanças significativas ocorrerem', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.2', 'Conformidade com políticas de segurança e padrões', 'A conformidade com políticas, regras e padrões de segurança da informação deve ser verificada regularmente', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.3', 'Análise técnica de conformidade', 'Sistemas de informação devem ser verificados regularmente para conformidade com políticas e padrões de segurança da informação da organização', 'A.18 - Conformidade / Compliance'),
    ]

