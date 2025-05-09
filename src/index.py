import docker
import secrets
import string
import argparse

con = docker.from_env()

def gerar_senha():
    secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
    return secure_str

def obter_variavel(lista, chave):

    variaveis = list(filter(lambda x: chave in x, lista))

    if len(variaveis) > 0:
        retorno = variaveis[0]
        return retorno.replace(f"{chave}=","")
    
    return ''

def exibir_banco(container):
    
    lista= container.attrs.get("Config").get("Env")
    root_string = obter_variavel(lista, "MYSQL_ROOT_PASSWORD")
    database_string = obter_variavel(lista, "MYSQL_DATABASE")
    user_string = obter_variavel(lista, "MYSQL_USER")
    password_string = obter_variavel(lista, "MYSQL_PASSWORD")
    porta_acesso = container.ports.get("3306/tcp")[0].get("HostPort")

    print(f"ID: {container.id}")

    if database_string != '':
        print(f"Nome do Banco: {database_string}")
    else:
        print(f"Nome do Banco: ")
    print(f"Porta de Acesso: {porta_acesso}")
    print(f"Senha do Root: {root_string}")
    if user_string != '':
        print(f"Usuário: {user_string}")
    if password_string != '':
        print(f"Senha do Usuário: {password_string}")

def criar_banco(senha_root='', usuario='', senha_usuario='', nome_banco=''):

    print("Criando um novo Banco de Dados.....")
    parametros = []

    if senha_root == '':
        senha_root = gerar_senha()

    parametros.append(f"MYSQL_ROOT_PASSWORD={senha_root}")

    if senha_usuario != '':
        parametros.append(f"MYSQL_PASSWORD={senha_usuario}")

    if usuario != '':
        parametros.append(f"MYSQL_USER={usuario}")

    if nome_banco != '':
        parametros.append(f"MYSQL_DATABASE={nome_banco}")

    container = con.containers.run("mysql", detach = True, publish_all_ports = True, 
        environment = parametros, labels={"gerador.banco": "true"})
    
    container = con.containers.get(container.id)

    print("Banco de Dados criado:")
    print("---------------------------------")
    exibir_banco(container)
    print("---------------------------------")

def listar_bancos():
    lista_containers = con.containers.list(filters={"label": ["gerador.banco=true"]})

    print("Bancos de Dados criados:")
    print("---------------------------------")
    for item in lista_containers:
        exibir_banco(item)
        print("---------------------------------")

def remover_banco(id):
    meu_container = con.containers.get(id)
    meu_container.remove(force=True)
        
parser = argparse.ArgumentParser()
parser.add_argument('operacao', help='O nome do banco de dados.')
parser.add_argument('--banco', default="", help='O nome do banco de dados.')
parser.add_argument('--root-pwd', default="",help='O nome do banco de dados.')
parser.add_argument('--user', default="",help='O nome do banco de dados.')
parser.add_argument('--pwd', default="",help='O nome do banco de dados.')
parser.add_argument('--id', default="",help='O nome do banco de dados.')

args = parser.parse_args()

match args.operacao:
    case "criar":
        criar_banco(nome_banco=args.banco, senha_root=args.root_pwd, usuario=args.user, senha_usuario=args.pwd)
    case "listar":
        listar_bancos()
    case "remover":
        remover_banco(args.id)
