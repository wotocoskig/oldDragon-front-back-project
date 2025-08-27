import random
import json
import os

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

    def salvar(self):
        personagens = {}
        if os.path.exists(ARQUIVO_PERSONAGENS):
            with open(ARQUIVO_PERSONAGENS, "r", encoding="utf-8") as f:
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
        with open(ARQUIVO_PERSONAGENS, "w", encoding="utf-8") as f:
            json.dump(personagens, f, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar(nome):
        if not os.path.exists(ARQUIVO_PERSONAGENS):
            return None
        with open(ARQUIVO_PERSONAGENS, "r", encoding="utf-8") as f:
            personagens = json.load(f)
        dados = personagens.get(nome)
        if not dados:
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
        return Personagem(nome, atributos, raca, classe)

    @staticmethod
    def listar_personagens():
        if not os.path.exists(ARQUIVO_PERSONAGENS):
            return []
        with open(ARQUIVO_PERSONAGENS, "r", encoding="utf-8") as f:
            personagens = json.load(f)
        return list(personagens.keys())

# ----------------- DISTRIBUIDOR DE ATRIBUTOS -----------------
class DistribuidorAtributos:
    @staticmethod
    def rolar_3d6():
        return sum(random.randint(1, 6) for _ in range(3))

    @staticmethod
    def estilo_classico():
        return dict(zip(
            ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
            [DistribuidorAtributos.rolar_3d6() for _ in range(6)]
        ))
