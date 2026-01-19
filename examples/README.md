# Hova - Examples

This folder has practices examples of **Hova** DSL and your respective converted outputs to **JSON**.

The goals of this examples is shows **How Hova describe worlds, entities and game structures**, and how this description become in a neutral format and consumible by external engines/tools.

## How read the examples

Each example follows a pattern:

example_name.hova -> hovabuild/example_name.json

- **`.hova`**: source code writted in Hova (input)
- **`.json`/`.yaml`/`.toml`**: conversion result (output)

The JSON is not executable by itself:
It exists to be consumed by:
- game engines (Godot, Unity, etc)
- own pipelines
- intermediate tools
- specific conversors

The validation and final interpretation **not is responsibility of Hova**, but for who consumes it.

---

## Filosofia dos exemplos

Os exemplos aqui:
- não representam uma engine específica
- não impõem regras de execução
- focam apenas em **descrição de mundo**

Hova é uma DSL **descritiva**, não imperativa.
Ela define *o que existe*, não *como rodar*.

---

Se algo parecer simples demais, é intencional. <br>
Os exemplos existem para ensinar a linguagem, não para exibir complexidade.<br>
Se houver complexidade, é apenas para mostrar que a linguagem suporta.<br>