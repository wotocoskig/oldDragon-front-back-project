import random
import json
import os
import unicodedata

ARQUIVO_PERSONAGENS = "personagens.json"

# ----------------- RAÇAS -----------------
class Raca:
    def __init__(self, nome, bonus_atributos, movimento, infravisao, alinhamento, habilidades):
        self.nome = nome
        self.bonus_atributos = bonus_atributos
        self.movimento = movimento
        self.infravisao = infravisao
        self.alinhamento = alinhamento
        self.habilidades = habilidades

    def aplicar_bonus(self, atributos):
        for attr, bonus in self.bonus_atributos.items():
            if attr in atributos:
                atributos[attr] += bonus
        return atributos

RAÇAS = {
    "Humano": Raca("Humano", {}, 6, 0, "Variável", ["Adaptabilidade"]),
    "Elfo": Raca("Elfo", {"Destreza": 2, "Inteligência": 1}, 6, 3, "Neutro", ["Visão aguçada", "Resistência a sono mágico"]),
    "Anão": Raca("Anão", {"Constituição": 2, "Força": 1}, 5, 3, "Leal", ["Resistência a venenos", "Habilidade com armas pesadas"]),
    "Halfling": Raca("Halfling", {"Destreza": 2, "Carisma": 1}, 5, 0, "Bom", ["Sorte", "Furtividade"])
}

# ----------------- CLASSES -----------------
class Classe:
    def __init__(self, nome, atributos_principais, habilidades):
        self.nome = nome
        self.atributos_principais = atributos_principais
        self.habilidades = habilidades

CLASSES = {
    "Guerreiro": Classe("Guerreiro", ["Força", "Constituição"], ["Ataque físico", "Uso de armas pesadas"]),
    "Ladrão": Classe("Ladrão", ["Destreza"], ["Furtividade", "Abrir fechaduras"]),
    "Mago": Classe("Mago", ["Inteligência"], ["Magias", "Conjuração"])
}

# ----------------- MAPA DE ATRIBUTOS (aceita sem acento) -----------------
def normalizar_texto(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt.lower()) if unicodedata.category(c) != 'Mn')

mapa_atributos = {
    normalizar_texto("Força"): "Força",
    normalizar_texto("Destreza"): "Destreza",
    normalizar_texto("Constituição"): "Constituição",
    normalizar_texto("Inteligência"): "Inteligência",
    normalizar_texto("Sabedoria"): "Sabedoria",
    normalizar_texto("Carisma"): "Carisma"
}

# ----------------- PERSONAGEM -----------------
class Personagem:
    def __init__(self, nome, atributos, raca=None, classe=None):
        self.nome = nome
        self.forca = atributos.get("Força", 0)
        self.destreza = atributos.get("Destreza", 0)
        self.constituicao = atributos.get("Constituição", 0)
        self.inteligencia = atributos.get("Inteligência", 0)
        self.sabedoria = atributos.get("Sabedoria", 0)
        self.carisma = atributos.get("Carisma", 0)
        self.raca = raca
        self.classe = classe
        if self.raca:
            self.aplicar_bonus_raca()

    def aplicar_bonus_raca(self):
        attrs = {
            "Força": self.forca,
            "Destreza": self.destreza,
            "Constituição": self.constituicao,
            "Inteligência": self.inteligencia,
            "Sabedoria": self.sabedoria,
            "Carisma": self.carisma
        }
        attrs = self.raca.aplicar_bonus(attrs)
        self.forca = attrs["Força"]
        self.destreza = attrs["Destreza"]
        self.constituicao = attrs["Constituição"]
        self.inteligencia = attrs["Inteligência"]
        self.sabedoria = attrs["Sabedoria"]
        self.carisma = attrs["Carisma"]

    def mostrar_atributos(self):
        print(f"\n--- Personagem: {self.nome} ---")
        print(f"Raça: {self.raca.nome if self.raca else 'Nenhuma'}")
        print(f"Classe: {self.classe.nome if self.classe else 'Nenhuma'}")
        print(f"Força: {self.forca}")
        print(f"Destreza: {self.destreza}")
        print(f"Constituição: {self.constituicao}")
        print(f"Inteligência: {self.inteligencia}")
        print(f"Sabedoria: {self.sabedoria}")
        print(f"Carisma: {self.carisma}")
        if self.raca:
            print(f"Habilidades da raça: {', '.join(self.raca.habilidades)}")
        if self.classe:
            print(f"Habilidades da classe: {', '.join(self.classe.habilidades)}")
        print("-------------------------------")

    def salvar(self):
        personagens = {}
        if os.path.exists(ARQUIVO_PERSONAGENS):
            with open(ARQUIVO_PERSONAGENS, "r") as f:
                personagens = json.load(f)
        personagens[self.nome] = {
            "forca": self.forca,
            "destreza": self.destreza,
            "constituicao": self.constituicao,
            "inteligencia": self.inteligencia,
            "sabedoria": self.sabedoria,
            "carisma": self.carisma,
            "raca": self.raca.nome if self.raca else None,
            "classe": self.classe.nome if self.classe else None
        }
        with open(ARQUIVO_PERSONAGENS, "w") as f:
            json.dump(personagens, f, indent=4)
        print(f"\nPersonagem '{self.nome}' salvo com sucesso!")

    @staticmethod
    def carregar(nome):
        if not os.path.exists(ARQUIVO_PERSONAGENS):
            print("\nNenhum personagem salvo ainda!")
            return None
        with open(ARQUIVO_PERSONAGENS, "r") as f:
            personagens = json.load(f)
        dados = personagens.get(nome)
        if not dados:
            print(f"\nPersonagem '{nome}' não encontrado!")
            return None
        raca = RAÇAS.get(dados.get("raca"))
        classe = CLASSES.get(dados.get("classe"))
        atributos = {
            "Força": dados["forca"],
            "Destreza": dados["destreza"],
            "Constituição": dados["constituicao"],
            "Inteligência": dados["inteligencia"],
            "Sabedoria": dados["sabedoria"],
            "Carisma": dados["carisma"]
        }
        personagem = Personagem(nome, atributos, raca, classe)
        print(f"\nPersonagem '{nome}' carregado com sucesso!")
        return personagem

    @staticmethod
    def listar_personagens():
        if not os.path.exists(ARQUIVO_PERSONAGENS):
            print("\nNenhum personagem salvo ainda!")
            return []
        with open(ARQUIVO_PERSONAGENS, "r") as f:
            personagens = json.load(f)
        if not personagens:
            print("\nNenhum personagem salvo ainda!")
            return []
        print("\nPersonagens salvos:")
        for nome in personagens:
            print(f"- {nome}")
        return list(personagens.keys())

# ----------------- DISTRIBUIDOR DE ATRIBUTOS -----------------
class DistribuidorAtributos:
    @staticmethod
    def rolar_3d6():
        return sum(random.randint(1, 6) for _ in range(3))

    @staticmethod
    def rolar_4d6_descarta_menor():
        dados = [random.randint(1, 6) for _ in range(4)]
        dados.remove(min(dados))
        return sum(dados)

    @staticmethod
    def estilo_classico():
        return dict(zip(
            ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
            [DistribuidorAtributos.rolar_3d6() for _ in range(6)]
        ))

    @staticmethod
    def escolher_atributo(valor, atributos, distribuicao):
        while True:
            escolha = input(f"Em qual atributo deseja colocar o valor {valor}? ").strip()
            chave = normalizar_texto(escolha)
            if chave in mapa_atributos:
                atributo_real = mapa_atributos[chave]
                if atributo_real not in distribuicao:
                    return atributo_real
            print("Escolha inválida ou atributo já preenchido. Tente novamente.")

    @staticmethod
    def estilo_aventureiro():
        valores = [DistribuidorAtributos.rolar_3d6() for _ in range(6)]
        atributos = ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"]
        distribuicao = {}
        while valores:
            print(f"\nValores restantes: {valores}")
            print("Atributos disponíveis:", [a for a in atributos if a not in distribuicao])
            valor = valores[0]
            atributo_escolhido = DistribuidorAtributos.escolher_atributo(valor, atributos, distribuicao)
            distribuicao[atributo_escolhido] = valor
            valores.pop(0)
        return distribuicao

    @staticmethod
    def estilo_heroico():
        atributos = ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"]
        valores = []
        print("\nRolar 4d6 descartando o menor para cada valor:")
        for i in range(6):
            input(f"\nPressione Enter para rolar os 4 dados para o valor {i+1}...")
            valor = DistribuidorAtributos.rolar_4d6_descarta_menor()
            print(f"Valor obtido: {valor}")
            valores.append(valor)
        distribuicao = {}
        while valores:
            print(f"\nValores restantes: {valores}")
            print("Atributos disponíveis:", [a for a in atributos if a not in distribuicao])
            valor = valores[0]
            atributo_escolhido = DistribuidorAtributos.escolher_atributo(valor, atributos, distribuicao)
            distribuicao[atributo_escolhido] = valor
            valores.pop(0)
        return distribuicao

# ----------------- FUNÇÕES AUXILIARES -----------------
def selecionar_opcao_com_lista(lista, tipo):
    while True:
        print(f"\nEscolha a {tipo} do personagem:")
        for i, item in enumerate(lista, 1):
            print(f"{i} - {item}")
        try:
            escolha = int(input(f"Digite sua escolha: "))
            if 1 <= escolha <= len(lista):
                return lista[escolha - 1]
        except ValueError:
            pass
        print("Opção inválida! Tente novamente.")

# ----------------- MENU PRINCIPAL -----------------
def main():
    print("Bem-vindo ao criador de personagem OldDragon!")
    while True:
        print("\nEscolha uma opção:")
        print("1 - Criar novo personagem")
        print("2 - Listar personagens salvos")
        print("3 - Carregar personagem existente")
        print("4 - Sair")

        try:
            opcao = int(input("Digite sua escolha: "))
        except ValueError:
            print("Opção inválida! Digite um número.")
            continue

        if opcao == 1:
            nome = input("Digite o nome do seu personagem: ")

            raca_nome = selecionar_opcao_com_lista(list(RAÇAS.keys()), "raça")
            raca = RAÇAS[raca_nome]

            classe_nome = selecionar_opcao_com_lista(list(CLASSES.keys()), "classe")
            classe = CLASSES[classe_nome]

            print("\nEscolha o estilo de distribuição de atributos:")
            print("1 - Estilo Clássico")
            print("2 - Estilo Aventureiro")
            print("3 - Estilo Heróico")
            try:
                escolha_atributos = int(input("Digite sua escolha: "))
            except ValueError:
                print("Opção inválida! Usando estilo clássico por padrão.")
                escolha_atributos = 1

            if escolha_atributos == 1:
                atributos = DistribuidorAtributos.estilo_classico()
            elif escolha_atributos == 2:
                atributos = DistribuidorAtributos.estilo_aventureiro()
            elif escolha_atributos == 3:
                atributos = DistribuidorAtributos.estilo_heroico()
            else:
                print("Opção inválida! Usando estilo clássico por padrão.")
                atributos = DistribuidorAtributos.estilo_classico()

            personagem = Personagem(nome, atributos, raca, classe)
            personagem.mostrar_atributos()
            personagem.salvar()

        elif opcao == 2:
            Personagem.listar_personagens()

        elif opcao == 3:
            nomes = Personagem.listar_personagens()
            if not nomes:
                continue
            escolha = input("Digite o nome do personagem que deseja carregar: ")
            if escolha in nomes:
                personagem = Personagem.carregar(escolha)
                if personagem:
                    personagem.mostrar_atributos()
            else:
                print("Nome inválido!")

        elif opcao == 4:
            print("Saindo do criador de personagens. Até mais!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()