# Laboratório DevOps: Ansible, Molecule e Testinfra

Laboratório prático de automação e testes de infraestrutura, desenvolvido como parte das atividades da trilha DevOps do Programa FAP, na Aponti Academy.

## Objetivo

Automatizar a instalação e configuração do servidor web Nginx em um contêiner Ubuntu, utilizando Ansible, Molecule, Docker e Testinfra.

O laboratório demonstra conceitos de Infraestrutura como Código (IaC), automação, testes de infraestrutura e idempotência.

## Tecnologias utilizadas

- **Ansible:** automação da instalação e configuração do Nginx.
- **Molecule:** gerenciamento dos cenários de teste da role Ansible.
- **Docker:** execução do ambiente Ubuntu isolado.
- **Testinfra:** validação automatizada do estado da infraestrutura.
- **Python e pytest:** execução dos testes automatizados.
- **GitHub Codespaces:** ambiente de desenvolvimento.

## Estrutura do projeto

```text
lab-ansible-molecule-testinfra/
├── .gitignore
├── README.md
└── servidor_nginx/
    ├── meta/
    │   └── main.yml
    ├── tasks/
    │   └── main.yml
    └── molecule/
        └── default/
            ├── molecule.yml
            ├── converge.yml
            └── tests/
                └── test_default.py
```

## Funcionamento

A role `servidor_nginx` executa duas tarefas principais:

1. Instalar o pacote Nginx por meio do módulo `ansible.builtin.apt`.
2. Iniciar e habilitar o serviço Nginx utilizando `ansible.builtin.service`.

O Molecule utiliza um contêiner Ubuntu 22.04 com suporte ao systemd para executar a role em um ambiente isolado.

## Preparação do ambiente

Com Python, Docker e um ambiente virtual disponíveis, instalar as dependências:

```bash
pip install ansible molecule molecule-docker pytest-testinfra
```

Em seguida, instalar as coleções Ansible necessárias:

```bash
ansible-galaxy collection install community.docker ansible.posix
```

Em caso de incompatibilidade com condicionais antigas do plugin Molecule Docker, foi utilizada temporariamente a variável:

```bash
export ANSIBLE_ALLOW_BROKEN_CONDITIONALS=true
```

Essa configuração é destinada apenas ao ambiente de laboratório. Não é recomendada como solução permanente para produção.

## Execução

Acessar a pasta da role:

```bash
cd servidor_nginx
```

Criar o ambiente de testes:

```bash
molecule create
```

Aplicar a configuração Ansible:

```bash
molecule converge
```

Executar novamente para verificar a idempotência:

```bash
molecule converge
```

Executar os testes diretamente no contêiner:

```bash
python -m pytest -v --hosts=docker://ubuntu-teste-nginx molecule/default/tests/test_default.py
```

## Validações automatizadas

O Testinfra verifica:

- Instalação do pacote Nginx.
- Serviço Nginx em execução.
- Serviço habilitado para iniciar automaticamente.
- Porta TCP 80 escutando conexões.

## Resultados obtidos

| Validação | Resultado |
|---|---|
| Criação do contêiner | Sucesso |
| Primeira execução Ansible | `ok=4 changed=2 failed=0` |
| Segunda execução Ansible | `ok=4 changed=0 failed=0` |
| Idempotência | Aprovada |
| Testinfra | `1 passed in 1.61s` |

A segunda execução da role não realizou alterações, demonstrando idempotência no cenário testado.

O teste Testinfra também foi aprovado, confirmando as condições verificadas no contêiner.

## Desafios técnicos

Durante a execução, foram identificados dois problemas:

**1. Incompatibilidade de condicionais do Ansible**

O plugin Molecule Docker utilizava uma condição que retornava uma string, incompatível com a validação mais rigorosa do Ansible Core instalado.

Solução temporária utilizada no laboratório:

```bash
export ANSIBLE_ALLOW_BROKEN_CONDITIONALS=true
```

**2. Contêiner interrompido após a retomada do Codespaces**

O contêiner estava encerrado e o Ansible não conseguiu criar o diretório temporário necessário para executar suas tarefas.

Após iniciar novamente o contêiner Docker, o comando `molecule converge` foi executado com sucesso.

## Validação final

A execução do ciclo completo com `molecule test` ainda está pendente. O resultado será documentado após a validação.

## Autoria

Desenvolvido por **Alexsandra Tavares**, como atividade prática de aprendizagem em DevOps e Infraestrutura como Código.
