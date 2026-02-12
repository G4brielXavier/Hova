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

## Filosophy of Examples

The examples here:
- Not represents a specific engine
- Not impose implementation rules
- Focuses only on **world description**

Hova is a descritive DSL, not imperative.
It defines *what exists*, not *how works*.

---

If something look so simple, is intentional. <br>
The examples exists to teech the language, not to display complexity. <br>
If there is complexity, is only to show that the language suport. <br>