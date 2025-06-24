📚 Site_Comunidade_Flask

Este projeto é uma aplicação web desenvolvida com Flask (framework Python) que permite aos usuários criar uma conta em um site blog, autenticar-se e publicar conteúdos relacionados a áreas de conhecimento específicas.

⚙️ Funcionalidades Principais
  * Autenticação de Usuário
    - Registro com validação de e-mail único
    - Login e logout seguros
    - Armazenamento de senhas com hash (criptografia)
    Proteção de rotas: páginas restritas a usuários autenticados

  * Gerenciamento de Perfil
    - Upload e atualização de imagem de perfil (com tratamento de arquivos)
    - Página de perfil personalizada
    - Listagem de cursos já realizados pelo usuário
  
  * Sistema de Postagens
    - Criação, edição e exclusão de postagens
    - Apenas o autor pode editar ou excluir seus próprios posts
    - Exibição de posts de todos os usuários (somente leitura)
  
  * Temas das Postagens
    - As publicações devem abordar temas relacionados a áreas de conhecimento específicas

  * Tratamento de Erros e Validações
    - Bloqueio de acesso a páginas protegidas para usuários não logados
    - Validação de formulário para evitar e-mails duplicados
    - Restrição de edição/exclusão de postagens por usuários não-autores
    - Mensagens de erro e feedback ao usuário (flash messages)

